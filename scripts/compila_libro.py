#!/usr/bin/env python3
"""Libro SSSUP modulare da sorgenti canonici, senza liste manuali.

Dalla radice del progetto:
  python3 scripts/compila_libro.py
  python3 scripts/compila_libro.py --campi Testo,Aiutino --anni 1996,2025
  python3 scripts/compila_libro.py --campi Testo --anni 1996-1998,2026
  python3 scripts/compila_libro.py --campi Testo --sito https://example.org/index.html

Il catalogo viene generato in build/, non modifica i problemi o il sito.
Usa latex -> dvips -> ps2pdf (per compatibilita' PSTricks). Tre passaggi
LaTeX risolvono i rimandi dell'indice e dei riferimenti incrociati.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'contenuti' / 'problemi'
BOOK = ROOT / 'latex' / 'SA_Book.tex'
BUILD = ROOT / 'build'
CATALOG = BUILD / 'SA_Book_catalogo.tex'
FIELDS = ('Testo', 'Risposta', 'Aiutino', 'Soluzioni', 'SoluzioniAlternative', 'Osservazioni', 'Commenti')
TITLES = {
    'Testo': 'Testi', 'Risposta': 'Risposte', 'Aiutino': 'Aiutini',
    'Soluzioni': 'Soluzioni', 'SoluzioniAlternative': 'Soluzioni alternative',
    'Osservazioni': 'Osservazioni', 'Commenti': 'Commenti',
}
TEX_MACRO = {
    'Testo': 'Testo', 'Risposta': 'Risposta', 'Aiutino': 'Aiutino',
    'SoluzioniAlternative': 'SoluzioniAlternative',
    'Osservazioni': 'Osservazioni', 'Commenti': 'Commenti',
}


def extract_macro(text: str, name: str) -> str | None:
    """Estrae una macro con graffe bilanciate, senza interpretare TeX."""
    pat = re.compile(r'\\renewcommand\s*\{\\'+re.escape(name)+r'\}\s*\{')
    found = list(pat.finditer(text))
    if not found:
        return None
    if len(found) != 1:
        raise ValueError(f'{name}: definizione ambigua ({len(found)} occorrenze)')
    i = found[0].end()
    start = i
    depth = 1
    while i < len(text):
        if text[i] == '%':
            k = i - 1
            while k >= 0 and text[k] == '\\':
                k -= 1
            if (i-1-k) % 2 == 0:
                nl = text.find('\n', i)
                i = nl + 1 if nl >= 0 else len(text)
                continue
        if text[i] == '\\':
            i += 2
            continue
        if text[i] == '{':
            depth += 1
        if text[i] == '}':
            depth -= 1
            if depth == 0:
                return text[start:i]
        i += 1
    raise ValueError(f'{name}: graffe non bilanciate')


def has_content(value: str | None) -> bool:
    if value is None:
        return False
    value = re.sub(r'(?m)(?<!\\)%[^\n]*', '', value)
    # Non scartare un campo costituito da richiami a macro grafiche.
    if re.search(r'\\(?:pspicture|begin\{pspicture|IniziaSudoku|domino|AreaIntPre|AreaIntPost)', value):
        return True
    value = re.sub(r'\\(?:ldots|dots|qquad|quad|par|medskip|smallskip|bigskip)\b', '', value)
    value = re.sub(r'\\[A-Za-z@]+\*?(?:\[[^]]*\])?', '', value)
    return bool(re.sub(r'[{}\s~.\\]', '', value))


def inventory() -> dict[tuple[int,int], dict]:
    result = {}
    for path in sorted(SOURCES.glob('SA_????_*.tex')):
        match = re.fullmatch(r'SA_(\d{4})_([1-9]\d*)\.tex', path.name)
        if not match:
            raise ValueError(f'Nome sorgente imprevisto: {path.name}')
        y, n = map(int, match.groups())
        text = path.read_text(encoding='utf-8')
        fields = {}
        for macro in (*TEX_MACRO.values(), 'SoluzioneUfficiale', 'SoluzioneRedazionale'):
            fields[macro] = extract_macro(text, macro)
        if not has_content(fields['Testo']):
            raise ValueError(f'{path.name}: campo Testo mancante o vuoto')
        result[y,n] = {
            'fields': fields,
            'ai': {
                macro: bool(re.search(r'SSSUP-BOZZA-AI:\s*'+macro+r'\b', fields[macro] or ''))
                for macro in ('Risposta','Aiutino','SoluzioneRedazionale')
            }
        }
    if not result:
        raise ValueError('Nessun problema trovato')
    return result


def parse_years(value: str, years: set[int]) -> set[int]:
    if value.lower() in ('tutti', 'all', '*'):
        return set(years)
    selected = set()
    for token in value.split(','):
        token = token.strip()
        m = re.fullmatch(r'(\d{4})(?:-(\d{4}))?', token)
        if not m:
            raise ValueError(f'Anno o intervallo non valido: {token!r}')
        lo = int(m.group(1)); hi = int(m.group(2) or lo)
        if hi < lo:
            raise ValueError(f'Intervallo inverso: {token}')
        selected.update(range(lo,hi+1))
    # Gli intervalli possono attraversare anni di cui mancano i testi.
    # Si includono soltanto gli anni realmente presenti nel repository.
    selected &= years
    if not selected:
        raise ValueError('Nessun problema canonico negli anni richiesti')
    return selected


def parse_fields(value: str) -> list[str]:
    if value.lower() in ('tutti', 'all', '*'):
        return list(FIELDS)
    fields = [part.strip() for part in value.split(',')]
    if not fields or any(x not in FIELDS for x in fields):
        raise ValueError('Campi validi: '+','.join(FIELDS))
    if len(fields) != len(set(fields)):
        raise ValueError('Un campo compare due volte')
    return [name for name in FIELDS if name in fields]


def validate_url(url: str) -> str:
    if not url:
        return ''
    parsed = urlsplit(url)
    if parsed.scheme not in ('https', 'http') or not parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError('--sito richiede una URL base http(s) senza parametri o frammenti')
    if not re.fullmatch(r'https?://[A-Za-z0-9./_~:-]+', url):
        raise ValueError('--sito contiene caratteri non compatibili con la URL LaTeX semplice')
    return url


def render_catalog(data: dict, years: set[int], fields: list[str], url: str) -> tuple[str,dict]:
    lines = [r'% Catalogo generato automaticamente: non modificare.',
             r'% Gli elenchi vengono dalle directory contenuti/problemi/.']
    if url:
        lines += [r'\BookWebtrue', r'\def\BookBaseURL{\detokenize{' + url + r'}}']
    counts = {}
    for field in fields:
        entries = defaultdict(list)
        for y,n in sorted(data):
            if y not in years:
                continue
            src = data[y,n]
            body = src['fields']
            if field == 'Soluzioni':
                old = has_content(body['SoluzioneUfficiale'])
                ai = has_content(body['SoluzioneRedazionale'])
                if old and ai:
                    raise ValueError(f'{y}.{n}: ha entrambe le soluzioni; da decidere la precedenza')
                command = 'BookSoluzioneArchivio' if old else ('BookSoluzioneAI' if ai else '')
            elif has_content(body[TEX_MACRO[field]]):
                command = 'Book' + field
                if field in ('Risposta','Aiutino') and src['ai'][field]:
                    command += 'AI'
                if field == 'SoluzioniAlternative':
                    command = 'BookAlternativa'
            else:
                command = ''
            if command:
                entries[y].append('\\'+command+'{'+str(y)+'}{'+str(n)+'}')
        if not entries:
            continue
        lines.append(r'\BookCapitolo{'+TITLES[field]+'}')
        if field == 'Risposta':
            lines.append(r'\BookIniziaRisposte')
        for y in sorted(entries):
            if field == 'Testo':
                lines.append(r'\BookAnnoTesto{'+str(y)+'}')
                lines.append(r'\BookIniziaTesti')
            elif field in ('Soluzioni', 'SoluzioniAlternative'):
                lines.append(r'\BookAnnoDaInserire{'+str(y)+'}')
            else:
                lines.append(r'\BookAnnoIndice{'+str(y)+'}')
            lines.extend(entries[y])
            if field == 'Testo':
                lines.append(r'\BookFinisciTesti')
            lines.append('')
        if field == 'Risposta':
            lines.append(r'\BookFinisciRisposte')
        counts[field] = sum(map(len, entries.values()))
    return '\n'.join(lines)+'\n', counts


def run(args: list[str], *, cwd: Path) -> None:
    print('ESEGUO:', ' '.join(args), flush=True)
    with (BUILD / 'SA_Book_compilazione.log').open('a', encoding='utf-8') as log:
        proc = subprocess.run(args, cwd=cwd, stdout=log, stderr=subprocess.STDOUT)
    if proc.returncode:
        raise RuntimeError(f'Compilazione interrotta ({proc.returncode}): vedi build/SA_Book_compilazione.log')


def compile_pdf() -> None:
    for cmd in ('latex','dvips','ps2pdf'):
        if not shutil.which(cmd):
            raise RuntimeError(f'Comando non trovato: {cmd}')
    log = BUILD / 'SA_Book_compilazione.log'
    log.write_text('', encoding='utf-8')
    for _ in range(3):
        run(['latex','-interaction=nonstopmode','-halt-on-error','-file-line-error',
             '-output-directory=../build','SA_Book.tex'],cwd=ROOT/'latex')
    run(['dvips','-o',str(BUILD/'SA_Book.ps'),str(BUILD/'SA_Book.dvi')],cwd=ROOT/'latex')
    run(['ps2pdf',str(BUILD/'SA_Book.ps'),str(BUILD/'SA_Book.pdf')],cwd=ROOT/'latex')
    # Il risultato stabile e' il PDF: eliminare i file di lavoro del libro.
    for suffix in ('.aux','.toc','.out','.dvi','.ps','.log'):
        (BUILD/('SA_Book'+suffix)).unlink(missing_ok=True)
    CATALOG.unlink(missing_ok=True)
    log.unlink(missing_ok=True)
    print('LIBRO:',BUILD/'SA_Book.pdf')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--campi',default='tutti',help='lista di sezioni; default=tutti')
    parser.add_argument('--anni',default='tutti',help='anni e intervalli; default=tutti')
    parser.add_argument('--sito',default='',help='URL di base del sito, fino a index.html')
    parser.add_argument('--solo-catalogo',action='store_true',help='genera il catalogo ma non compila')
    args=parser.parse_args()
    try:
        if not BOOK.exists():
            raise ValueError(f'Sorgente del libro non trovato: {BOOK}')
        data=inventory()
        years=parse_years(args.anni,{year for year,_ in data})
        fields=parse_fields(args.campi)
        url=validate_url(args.sito)
        content,counts=render_catalog(data,years,fields,url)
        BUILD.mkdir(exist_ok=True)
        CATALOG.write_text(content,encoding='utf-8')
        print(f'Catalogo: {len(data)} sorgenti trovati; {len(years)} anni selezionati.')
        for field in fields:
            print(f'  {field}: {counts.get(field,0)} problemi')
        print('Link web:',url or '(disattivati: usare --sito URL)')
        if not args.solo_catalogo:
            compile_pdf()
    except (ValueError,OSError,RuntimeError) as exc:
        print('ERRORE:',exc,file=sys.stderr)
        return 1
    return 0


if __name__=='__main__':
    sys.exit(main())
