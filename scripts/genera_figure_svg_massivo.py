#!/usr/bin/env python3
"""Inventario e conversione sperimentale PSTricks -> SVG per ProblemiSSSUP.

Dalla radice del repository, senza modificare i sorgenti o il sito:
    python3 ~/Downloads/genera_figure_svg_massivo.py --solo-inventario
    python3 ~/Downloads/genera_figure_svg_massivo.py --anno 2004 --problema 4 --limite 3
    python3 ~/Downloads/genera_figure_svg_massivo.py

Ogni disegno e' una lavorazione isolata con timeout: gli errori non
interrompono il lotto. I risultati sono in build/figure-svg (ignorato da Git).
Un report HTML permette di vedere gli SVG e i candidati a tabelle HTML.
I 31 Sudoku e i 53 domino gia' resi dal sito sono contati separatamente.

ATTENZIONE: conversione sperimentale. Nessuna immagine viene inserita nel sito
senza revisione. Il riconoscimento 'tabella' e' una proposta euristica.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import importlib.util
import json
import os
import signal
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

FIELDS = ('Testo', 'Risposta', 'Aiutino', 'SoluzioneUfficiale',
          'SoluzioneRedazionale', 'SoluzioniAlternative', 'Osservazioni', 'Commenti')
PICTURE_CMD = re.compile(
    r'\\(?:begin\{pspicture\*?\}|end\{pspicture\*?\}|'
    r'endpspicture(?![A-Za-z@])|pspicture\*?(?![A-Za-z@]))'
)
PSSET = re.compile(r'\\psset\s*\{[^{}]*\}')
COLOR_DEF = re.compile(
    r'\\(?:newrgbcolor|newgray|newcmykcolor|newhsbcolor)\s*\{([^{}]*)\}\s*\{[^{}]*\}'
    r'|\\definecolor\s*\{([^{}]*)\}\s*\{[^{}]*\}\s*\{[^{}]*\}'
)
AREA = re.compile(r'\\AreaInt(?:Pre|Post)\s*\{[^{}]*\}')
LOCAL_SUDOKU = re.compile(r'\\IniziaSudoku\s*\{')
LOCAL_DOMINO = re.compile(r'\\domino\s*\{')
COMPLEX_GEO = re.compile(r'\\(?:pscircle|psarc|psellipse|pscurve|psbezier|'
                         r'psplot|parametricplot|pspolygon|pst|pnode|cnode|'
                         r'psgrid|pswedge|psdots|psdot)\b', re.I)

@dataclass
class Figure:
    file: Path
    field: str
    index: int
    kind: str
    fragment: str
    pssets: str
    category: str
    reason: str
    source_hash: str

    @property
    def ident(self) -> str:
        return f'{self.file.stem}__{self.field}__{self.index:02d}'


def read_generator(root: Path):
    """Riutilizza l'estrattore e il conteggio di produzione del sito."""
    path = root / 'scripts' / 'genera_dati_sito.py'
    if not path.is_file():
        raise RuntimeError(f'Manca il convertitore web: {path}')
    spec = importlib.util.spec_from_file_location('sssup_web_generator_for_svg_scan', path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'Impossibile leggere {path}')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def mask_comments_keep_offsets(s: str) -> str:
    """Maschera i commenti TeX, lasciando invariati tutti gli offset."""
    pieces = []
    for line in s.splitlines(keepends=True):
        cut = None
        for i, char in enumerate(line):
            if char != '%':
                continue
            k = i - 1
            while k >= 0 and line[k] == '\\':
                k -= 1
            if (i - 1 - k) % 2 == 0:
                cut = i
                break
        if cut is None:
            pieces.append(line)
        else:
            tail = line[cut:]
            pieces.append(line[:cut] + ''.join(c if c in '\r\n' else ' ' for c in tail))
    return ''.join(pieces)


def classification(fragment: str, kind: str) -> tuple[str, str]:
    if kind == 'area':
        return 'svg', 'macro AreaInt: figura con informazione geometrica/aree'
    if 'linecolor=scacchiera' in fragment:
        return 'tabella-candidata', 'scacchiera 8x8: facile rappresentazione HTML/CSS'
    if re.search(r'\\(?:aula|aulagialla)\b', fragment):
        return 'tabella-candidata', 'aule/caselle: possibile tabella HTML'
    # Un ritaglio geometrico con rotazioni e rettangoli NON e' una tabella.
    has_complex = bool(COMPLEX_GEO.search(fragment) or
                       re.search(r'\\(?:psclip|pscustom|SpecialCoor|rotate|pstGeonode)\b',fragment))
    frames = len(re.findall(r'\\psframe\*?\b', fragment))
    lines = len(re.findall(r'\\psline\b', fragment))
    labels = len(re.findall(r'\\rput\b', fragment))
    multips = bool(re.search(r'\\multips\b',fragment))
    if not has_complex and frames >= 2 and lines <= 2 and not multips:
        return 'tabella-candidata', f'{frames} rettangoli e {labels} etichette: possibile tabella semplice'
    if not has_complex and (frames >= 2 or (multips and frames > 0)):
        return 'griglia-da-valutare', 'caselle/riquadri: possibile griglia HTML, da valutare visivamente'
    return 'svg', 'figura geometrica/grafico o schema non classificato come tabella'


def figures_in_field(src: Path, field: str, source: str, digest: str) -> list[Figure]:
    masked = mask_comments_keep_offsets(source)
    items: list[tuple[int, str, str]] = []
    depth = 0
    start = None
    for m in PICTURE_CMD.finditer(masked):
        closing = m.group().startswith((r'\endpspicture', r'\end{pspicture'))
        if not closing:
            if depth == 0:
                start = m.start()
            depth += 1
        else:
            if depth <= 0:
                raise ValueError(f'{src.name}/{field}: chiusura PSTricks senza apertura')
            depth -= 1
            if depth == 0:
                assert start is not None
                items.append((start, 'picture', source[start:m.end()]))
                start = None
    if depth != 0:
        raise ValueError(f'{src.name}/{field}: figura PSTricks non chiusa')
    for m in AREA.finditer(masked):
        items.append((m.start(), 'area', source[m.start():m.end()]))
    items.sort(key=lambda item: item[0])
    result = []
    for number, (start, kind, fragment) in enumerate(items, 1):
        # Le impostazioni esterne \psset possono essere necessarie.
        # Recupera anche le definizioni di colori *esterne* al disegno
        # (es. scacchiera nel problema 1997.3). L'ultima vince.
        colors = {}
        for match in COLOR_DEF.finditer(masked[:start]):
            colors[match.group(1) or match.group(2)] = match.group(0)
        settings = '\n'.join([*colors.values(), *(s.group(0) for s in PSSET.finditer(masked[:start]))])
        category, reason = classification(fragment, kind)
        result.append(Figure(src, field, number, kind, fragment,
                             settings, category, reason, digest))
    return result


def inventory(root: Path, gen, year: int | None = None,
              problem: int | None = None) -> tuple[list[Figure], list[str], Counter]:
    srcdir = root / 'contenuti/problemi'
    if not srcdir.is_dir():
        raise RuntimeError(f'Manca la cartella {srcdir}; eseguire dalla radice del progetto')
    figures: list[Figure] = []
    errors: list[str] = []
    already_html: Counter = Counter()
    for f in sorted(srcdir.glob('SA_????_*.tex')):
        m = re.fullmatch(r'SA_(\d{4})_(\d+)\.tex', f.name)
        if not m:
            continue
        if year is not None and int(m[1]) != year:
            continue
        if problem is not None and int(m[2]) != problem:
            continue
        try:
            text = f.read_text(encoding='utf-8')
            digest = hashlib.sha256(f.read_bytes()).hexdigest()
            for field in FIELDS:
                value = gen.extract_macro(text, field)
                if value is None:
                    continue
                already_html['sudoku'] += len(LOCAL_SUDOKU.findall(gen.no_comments(value)))
                already_html['domino'] += len(LOCAL_DOMINO.findall(gen.no_comments(value)))
                got = figures_in_field(f, field, value, digest)
                # Compatibilita' dei numeri con i segnaposto del sito.
                _, expected, _ = gen.preprocess(value)
                if len(got) != expected:
                    raise ValueError(f'{f.name}/{field}: inventario {len(got)} != sito {expected}')
                figures.extend(got)
        except Exception as exc:
            errors.append(f'{f.name}: {type(exc).__name__}: {exc}')
    return figures, errors, already_html


def tex_source(fig: Figure) -> str:
    definitions = '\n'.join('\\newcommand{\\' + name + '}{}' for name in
                            ('Anno', 'NumeroProblema', *FIELDS))
    common = r'''
\providecommand{\TitoloSoluzione}{}
\providecommand{\TitoloSoluzioneAlternativaA}{}
\providecommand{\TitoloSoluzioneAlternativaB}{}
\providecommand{\TitoloOsservazione}{}
\providecommand{\TitoloCommenti}{}
\providecommand{\TitoloOss}[1]{}
\providecommand{\DomandaA}{}
\providecommand{\DomandaB}{}
\providecommand{\DomandaC}{}
\providecommand{\DomandaD}{}
\providecommand{\re}{\mathbb{R}}
\providecommand{\z}{\mathbb{Z}}
\providecommand{\q}{\mathbb{Q}}
'''
    return (r'\documentclass[12pt]{article}' + '\n'
            + r'\usepackage{amsmath,amsfonts,latexsym,graphicx,pstricks,multido,pst-eucl,pst-plot}' + '\n'
            + r'\usepackage[active,tightpage]{preview}' + '\n'
            + r'\pagestyle{empty}' + '\n'
            + definitions + '\n' + common
            + r'\input{' + fig.file.resolve().as_posix() + '}\n'
            + r'\begin{document}' + '\n'
            + r'\begin{preview}' + '\n'
            + fig.pssets + '\n' + fig.fragment + '\n'
            + r'\end{preview}' + '\n'
            + r'\end{document}' + '\n')


def execute(cmd: list[str], directory: Path, seconds: int,
            log: Path) -> tuple[bool, str]:
    with log.open('a', encoding='utf-8', errors='replace') as out:
        out.write('\nCOMMAND: ' + ' '.join(cmd) + '\n')
        out.flush()
        try:
            # Una sessione per processo: in caso di timeout si termina anche
            # l'eventuale processo figlio avviato dallo strumento TeX.
            p = subprocess.Popen(cmd, cwd=directory, stdout=out,
                                 stderr=subprocess.STDOUT, start_new_session=True)
            try:
                code = p.wait(timeout=seconds)
            except subprocess.TimeoutExpired:
                os.killpg(p.pid, signal.SIGKILL)
                p.wait()
                out.write(f'\nTIMEOUT: superati {seconds} secondi\n')
                return False, f'timeout dopo {seconds}s: {cmd[0]}'
        except OSError as exc:
            out.write(f'\nOS ERROR: {exc}\n')
            return False, f'impossibile eseguire {cmd[0]}: {exc}'
    if code:
        return False, f'{cmd[0]}: exit {code}'
    return True, ''


def run_figure(fig: Figure, out_dir: Path, timeout: int,
               produce_pdf: bool, latex_only: bool) -> tuple[str, str, str]:
    work = out_dir / 'work' / fig.ident
    work.mkdir(parents=True, exist_ok=True)
    log = work / 'compilazione.log'
    log.write_text('', encoding='utf-8')
    (work / 'figura.tex').write_text(tex_source(fig), encoding='utf-8')
    steps = [['latex', '-interaction=nonstopmode', '-halt-on-error',
              '-file-line-error', 'figura.tex']]
    if not latex_only:
        steps.append(['dvisvgm', '--no-fonts', '--bbox=min',
                      '-o', 'figura.svg', 'figura.dvi'])
    if produce_pdf:
        steps += [['dvips', '-o', 'figura.ps', 'figura.dvi'],
                  ['ps2pdf', 'figura.ps', 'figura.pdf']]
    for cmd in steps:
        ok, error = execute(cmd, work, timeout, log)
        if not ok:
            return 'ERRORE', error, ''
    if not (work / 'figura.dvi').is_file():
        return 'ERRORE', 'DVI mancante dopo latex', ''
    path = work / ('figura.dvi' if latex_only else 'figura.svg')
    if not path.is_file() or path.stat().st_size < 90:
        return 'ERRORE', f'Output mancante o vuoto: {path.name}', ''
    # Conservare anche il PDF di confronto, se richiesto, pure nel
    # collaudo --solo-latex senza SVG.
    if produce_pdf and (work / 'figura.pdf').is_file():
        pdf = out_dir / 'pdf' / (fig.ident + '.pdf')
        pdf.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(work / 'figura.pdf', pdf)
    # Copiare l'SVG nel catalogo finale solo se e' prodotto correttamente.
    if latex_only:
        return 'LATEX_OK', '', ''
    svg = out_dir / 'svg' / (fig.ident + '.svg')
    svg.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, svg)
    return 'OK', '', str(svg.relative_to(out_dir))


def load_previous(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        return {r['id']: r for r in data.get('figures', []) if isinstance(r, dict)}
    except (OSError, ValueError, KeyError):
        return {}


def write_report(out: Path, rows: list[dict], errors: list[str],
                 already: Counter, full_inventory: bool):
    out.mkdir(parents=True, exist_ok=True)
    with (out / 'inventario.csv').open('w', newline='', encoding='utf-8') as fp:
        writer = csv.DictWriter(fp, fieldnames=['id','problema','campo','numero','tipo',
               'categoria','motivazione','stato','errore','svg','sha256_sorgente'],
               extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
    data = {'generated_at': datetime.now().astimezone().isoformat(timespec='seconds'),
            'complete_archive': full_inventory,
            'existing_html': dict(already),
            'scan_errors': errors,
            'figures': rows}
    (out/'inventario.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    table = Counter(r['categoria'] for r in rows)
    outcomes = Counter(r['stato'] for r in rows)
    summary = ['ProblemiSSSUP - catalogo PSTricks sperimentale',
               f'Figure inventariate: {len(rows)}',
               f'Categorie suggerite: {dict(table)}',
               f'Stati: {dict(outcomes)}',
               'Gia rese in HTML/MathJax (fuori dai 156): '+str(dict(already)),
               f'Errori inventario: {len(errors)}',
               'Il conteggio completo atteso (al 2026-11-08) e 156.',
               'Conversioni isolate; eventuali difetti tipografici possono essere gia nel PDF.',
               'ATTENZIONE: il catalogo e sperimentale, non e pubblicato sul sito.']
    (out/'RIEPILOGO.txt').write_text('\n'.join(summary + errors)+'\n', encoding='utf-8')
    css = '''body{max-width:1160px;margin:30px auto;padding:0 20px;color:#202e38;background:#f7f9fa;font:15px/1.5 system-ui}
    h1{font-size:27px}.legend{color:#536674}.stats{margin:14px 0}.item{background:white;border:1px solid #d5e1e4;border-radius:12px;margin:14px 0;padding:14px}
    .head{display:flex;gap:15px;align-items:center;flex-wrap:wrap}.tag{background:#e8f2f0;border-radius:5px;padding:3px 7px;font-size:12px}
    .tab{background:#f8efd4}.err{background:#ffe9e9}.img{width:100%;max-height:460px;object-fit:contain;display:block;border:1px solid #edf0f3;margin:12px 0}
    small{color:#526678}code{overflow-wrap:anywhere}a{color:#126b68}
    '''
    parts = ['<!doctype html><html lang="it"><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width, initial-scale=1">',
             '<title>Catalogo PSTricks - ProblemiSSSUP</title><style>'+css+'</style>',
             '<h1>Catalogo PSTricks - ProblemiSSSUP</h1>',
             '<p class="legend">Anteprima tecnica locale. Le tabelle sono soltanto candidate: nessuna sostituzione automatica.</p>',
             '<div class="stats">'+html.escape(' | '.join(summary[1:6]))+'</div>']
    if errors:
        parts.append('<p class="err">Errori di inventario: <code>'+
                     html.escape(' // '.join(errors))+'</code></p>')
    for r in rows:
        label = 'tab' if r['categoria'] == 'tabella-candidata' else ''
        if r['categoria'] == 'griglia-da-valutare': label = 'tab'
        if r['stato'] == 'ERRORE': label = 'err'
        parts.append('<section class="item"><div class="head"><strong>'+html.escape(r['id'])+
                     '</strong><span class="tag '+label+'">'+html.escape(r['categoria'])+
                     '</span><span class="tag">'+html.escape(r['stato'])+'</span></div>')
        parts.append('<small>'+html.escape(r['motivazione'])+'</small>')
        if r['svg'] and (out / r['svg']).is_file():
            parts.append('<a href="'+html.escape(r['svg'], quote=True)+'">Apri SVG originale</a>')
            parts.append('<img loading="lazy" class="img" src="'+html.escape(r['svg'], quote=True)+'" alt="'+html.escape(r['id'], quote=True)+'">')
        if r['errore']:
            parts.append('<p class="err">'+html.escape(r['errore'])+'</p>')
        loglink = 'work/'+r['id']+'/compilazione.log'
        if (out / loglink).is_file():
            parts.append('<small><a href="'+html.escape(loglink,quote=True)+'">Log di compilazione</a></small>')
        parts.append('</section>')
    parts.append('</html>')
    (out/'catalogo.html').write_text('\n'.join(parts)+'\n', encoding='utf-8')


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--id', help='Prova una singola figura, per es. SA_2010_4__Osservazioni__01')
    p.add_argument('--anno', type=int, help='Filtra un anno')
    p.add_argument('--problema', type=int, help='Filtra un problema (richiede --anno)')
    p.add_argument('--limite', type=int, help='Prova al massimo N figure')
    p.add_argument('--solo-inventario', action='store_true', help='Non invoca LaTeX o dvisvgm')
    p.add_argument('--solo-latex', action='store_true', help='Compila DVI, senza invocare dvisvgm')
    p.add_argument('--pdf', action='store_true', help='Produce anche PDF di confronto')
    p.add_argument('--forza', action='store_true', help='Ripete anche le figure gia riuscite')
    p.add_argument('--timeout', type=int, default=35, help='Secondi massimi per ogni comando (default: 35)')
    p.add_argument('--output', type=Path, default=Path('build/figure-svg'), help='Directory output')
    args = p.parse_args()
    if args.problema is not None and args.anno is None:
        p.error('--problema richiede --anno')
    if args.limite is not None and args.limite <= 0:
        p.error('--limite deve essere positivo')
    if args.timeout <= 0:
        p.error('--timeout deve essere positivo')
    root = Path.cwd().resolve()
    if not (root/'contenuti/problemi').is_dir():
        p.error('Eseguire dalla radice di ProblemiSSSUP')
    out = args.output.resolve()
    src = (root/'contenuti/problemi').resolve()
    if out == src or src in out.parents or out == root or out == root/'sito':
        p.error('Directory di output non valida: non scrivere tra i sorgenti canonici')
    try:
        gen = read_generator(root)
        found, scan_errors, existing_html = inventory(root, gen, args.anno, args.problema)
    except (OSError, ValueError, RuntimeError) as exc:
        print('ERRORE DI INVENTARIO:', exc, file=sys.stderr)
        return 2
    if args.id and args.id not in {f.ident for f in found}:
        p.error('ID non trovato: ' + args.id)
    if not found and not scan_errors:
        print('Nessuna figura PSTricks nella selezione.')
        return 0
    if not (args.solo_inventario or args.solo_latex):
        if not shutil.which('dvisvgm'):
            p.error('dvisvgm non trovato. Usare --solo-inventario o --solo-latex.')
    if not args.solo_inventario and not shutil.which('latex'):
        p.error('latex non trovato; usare --solo-inventario')
    if args.pdf and not args.solo_inventario:
        for tool in ('dvips','ps2pdf'):
            if not shutil.which(tool):
                p.error(f'{tool} non trovato; togliere --pdf')
    old = load_previous(out/'inventario.json')
    selected = ({args.id} if args.id else
                {fig.ident for fig in found[:args.limite]} if args.limite else
                {f.ident for f in found})
    rows: list[dict] = []
    cnt = Counter()
    print(f'Figure nel catalogo: {len(found)} (tabelle/griglie candidate: {sum(f.category in ("tabella-candidata","griglia-da-valutare") for f in found)})',flush=True)
    for i, fig in enumerate(found, 1):
        prev = old.get(fig.ident, {})
        status = 'NON_PROVATA'
        error = ''
        svg = ''
        if fig.ident in selected and not args.solo_inventario:
            old_svg = prev.get('svg','')
            if (args.solo_latex and not args.forza and
                    prev.get('stato') == 'LATEX_OK' and
                    prev.get('sha256_sorgente') == fig.source_hash and
                    (out/'work'/fig.ident/'figura.dvi').is_file()):
                status = 'LATEX_OK'
                print(f'[{i:3}/{len(found)}] {fig.ident}: LATEX_OK (gia compilata)',flush=True)
            elif (not args.forza and prev.get('stato') == 'OK' and
                    prev.get('sha256_sorgente') == fig.source_hash and
                    old_svg and (out/old_svg).is_file() and not args.solo_latex and
                    (not args.pdf or (out/'pdf'/(fig.ident+'.pdf')).is_file())):
                status, svg = 'OK', old_svg
                print(f'[{i:3}/{len(found)}] {fig.ident}: OK (gia convertita)',flush=True)
            else:
                try:
                    status, error, svg = run_figure(fig, out, args.timeout,
                                                    args.pdf, args.solo_latex)
                except Exception as exc:
                    # Anche un problema Python su un disegno non ferma gli altri.
                    status, error = 'ERRORE', f'{type(exc).__name__}: {exc}'
                print(f'[{i:3}/{len(found)}] {fig.ident}: {status}' +
                      (f' ({error})' if error else ''),flush=True)
        elif prev.get('sha256_sorgente') == fig.source_hash and not args.forza:
            status = prev.get('stato','NON_PROVATA')
            error = prev.get('errore','')
            svg = prev.get('svg','') if (out/prev.get('svg','__nessuno__')).is_file() else ''
        cnt[status] += 1
        rows.append({'id':fig.ident, 'problema':fig.file.stem, 'campo':fig.field,
                     'numero':fig.index, 'tipo':fig.kind, 'categoria':fig.category,
                     'motivazione':fig.reason, 'stato':status, 'errore':error,
                     'svg':svg, 'sha256_sorgente':fig.source_hash})
        # Salvataggio progressivo: anche un'interruzione di tutto il lotto
        # consente di riprenderlo evitando le conversioni gia riuscite.
        if not args.solo_inventario and i % 5 == 0:
            write_report(out, rows + [
                {'id':f.ident,'problema':f.file.stem,'campo':f.field,
                 'numero':f.index,'tipo':f.kind,'categoria':f.category,
                 'motivazione':f.reason,'stato':'NON_PROVATA','errore':'','svg':'',
                 'sha256_sorgente':f.source_hash}
                for f in found[i:]], scan_errors, existing_html,
                args.anno is None and args.problema is None)
    write_report(out, rows, scan_errors, existing_html,
                 args.anno is None and args.problema is None)
    print('\n'.join((f'SVG OK: {cnt["OK"]}, LaTeX OK: {cnt["LATEX_OK"]}, errori: {cnt["ERRORE"]}, '
                     f'non provate: {cnt["NON_PROVATA"]}',
                     f'Inventario: {out / "inventario.csv"}',
                     f'Catalogo visuale: {out / "catalogo.html"}',
                     'Nessun sorgente o file del sito modificato.')))
    if scan_errors:
        print('Attenzione: errori di inventario:', *scan_errors, sep='\n- ', file=sys.stderr)
    return 0 if not scan_errors else 1


if __name__ == '__main__':
    raise SystemExit(main())
