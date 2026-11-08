#!/usr/bin/env python3
"""Genera SOLO i dati web dei problemi LaTeX, senza riscrivere HTML/CSS/JS.

Esecuzione dalla radice di ProblemiSSSUP:
  python3 scripts/genera_dati_sito.py
  python3 scripts/genera_dati_sito.py --anno 2013
  python3 scripts/genera_dati_sito.py --anno 2013 --problema 2

Richiede Pandoc. I sorgenti del repository NON vengono modificati.
Ogni file web contiene impronte SHA-256 per verificare sorgente e convertitore.
È una prima implementazione sperimentale: verificare sempre PSTricks,
macro storiche, figure ed eventuali riferimenti incrociati.
 Le bozze AI vengono pubblicate soltanto con metadati di provenienza
 che l'interfaccia puo' mostrare anche nelle fisarmoniche chiuse.
"""
from __future__ import annotations
import argparse
from html import escape
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

JS_PREFIX = "window.SSSUP.registerProblem("
JS_SUFFIX = ");"

FIELDS=['Testo','Risposta','Aiutino','SoluzioneUfficiale','SoluzioneRedazionale','SoluzioniAlternative','Osservazioni','Commenti']

# I commenti-marcatori appartengono ai sorgenti canonici e non vengono
# mostrati da TeX. Nel sito diventano segnaposto nello stesso punto.
MISSING_FIGURE_RE = re.compile(
    r'^[ \t]*%[ \t]*SSSUP-FIGURA-DA-RICOSTRUIRE:[ \t]*(?P<ref>[^\r\n]+?)[ \t]*$',
    flags=re.M,
)
PSTRICKS_INLINE_RE = re.compile(r'\\pspicture\b.*?\\endpspicture\b', flags=re.S)
PSTRICKS_ENV_RE = re.compile(r'\\begin\{pspicture\}.*?\\end\{pspicture\}', flags=re.S)

# Rendering web esplicito per le macro locali dei problemi storici.
# Il convertitore non esegue il preambolo LaTeX: gli usi di queste macro
# devono essere tradotti, o segnalati; mai abbandonati a Pandoc.
SUDOKU_PAIR_RE = re.compile(
    r'\\IniziaSudoku((?:\s*\{[^{}]*\}){8})\s*'
    r'\\FinisciSudoku((?:\s*\{[^{}]*\}){8})'
)
DOMINO_RE = re.compile(r'\\domino\s*\{([^{}]*)\}\s*\{([^{}]*)\}')
AREA_RE = re.compile(r'\\AreaInt(?:Pre|Post)\s*\{[^{}]*\}')
LOCAL_USE_RE = re.compile(
    r'\\(?:IniziaSudoku|FinisciSudoku|domino|AreaIntPre|AreaIntPost|'
    r'aula|aulagialla)\b'
)
AI_DRAFT_RE = re.compile(
    r'(?m)^[ \t]*%[ \t]*SSSUP-BOZZA-AI:[ \t]*'
    r'(Risposta|Aiutino|SoluzioneRedazionale)\s*;[^\r\n]*'
    r'\bstato=DA-VERIFICARE\b'
)
AI_SOURCE_RE = re.compile(r'(?m)^[ \t]*%[ \t]*SSSUP-PROVENIENZA:[ \t]*(.+?)\s*$')


def field_provenance(value: str, field: str) -> dict:
    """Classifica il campo dalla sua intestazione, mai per somiglianza testuale."""
    markers = list(AI_DRAFT_RE.finditer(value))
    if not markers:
        if field == 'SoluzioneRedazionale' or 'SSSUP-BOZZA-AI:' in value:
            raise ValueError('Marcatore AI assente o incompleto in ' + field)
        return {'tipo': 'preesistente'}
    if len(markers) != 1 or markers[0].group(1) != field:
        raise ValueError('Marcatori AI ambigui o incoerenti in ' + field)
    source = AI_SOURCE_RE.search(value)
    if source is None:
        raise ValueError('Bozza AI senza nota di provenienza in ' + field)
    return {'tipo': 'ai', 'stato': 'da_verificare', 'fonte': source.group(1).strip()}

LOCAL_DEF_RE = re.compile(r'\\(?:providecommand|newcommand)\s*\{\\([A-Za-z@]+)\}')


def render_sudoku(cells: list[str]) -> str:
    """Rende le 16 caselle nell'ordine originale (righe dall'alto)."""
    if len(cells) != 16:
        raise ValueError('Sudoku: attese esattamente 16 caselle')
    rows = []
    for r in range(4):
        cols = []
        for c in range(4):
            value = cells[4*r+c].strip()
            # In questi problemi le caselle contengono cifre, A-D, ?, o vuoto.
            if not re.fullmatch(r'[A-Za-z0-9?]*', value):
                raise ValueError(f'Sudoku: casella non supportata: {value!r}')
            top = '2px solid' if r in (0, 2) else '1px dotted'
            left = '2px solid' if c in (0, 2) else '1px dotted'
            style = (f'width:1.8em;height:1.8em;text-align:center;'
                     f'border-top:{top};border-left:{left};'
                     f'border-right:{"2px solid" if c==3 else "0"};'
                     f'border-bottom:{"2px solid" if r==3 else "0"};')
            cols.append(f'<td style="{style}">{escape(value)}</td>')
        rows.append('<tr>'+''.join(cols)+'</tr>')
    return ('<table class="sssup-sudoku" aria-label="Sudoku 4 per 4" '
            'style="display:inline-table;border-collapse:collapse;vertical-align:middle;'
            'margin:.3em .6em;">'
            +'<tbody>'+''.join(rows)+'</tbody></table>')


def render_local_macros(text: str, local_defs=()) -> tuple[str, dict[str, str]]:
    """Sostituisce le macro locali con HTML differito o LaTeX standard."""
    sudoku: dict[str,str] = {}
    def replace_sudoku(match: re.Match) -> str:
        cells = re.findall(r'\{([^{}]*)\}', match.group())
        token = f'SSSUPSUDOKURENDER{len(sudoku):04d}FINE'
        sudoku[token] = render_sudoku(cells)
        return '\n\n'+token+'\n\n'
    text = SUDOKU_PAIR_RE.sub(replace_sudoku, text)

    def replace_domino(match: re.Match) -> str:
        a,b = match.groups()
        # La macro originale e' una tabella matematica 1x2 con bordi.
        # Ora la formula MathJax contiene solo comandi LaTeX standard.
        return (r'\begin{array}{|c|c|}\hline '
                + a + ' & ' + b + r' \\ \hline\end{array}')
    text = DOMINO_RE.sub(replace_domino, text)
    remaining = LOCAL_USE_RE.search(text)
    if remaining:
        raise ValueError(f'Macro locale non convertita: {remaining.group(0)}')
    # Anche una macro locale aggiunta in futuro non deve sparire nel nulla.
    # Le macro delle figure PSTricks sono gia' state rimosse con il disegno.
    for name in local_defs:
        if re.search(r'\\' + re.escape(name) + r'(?![A-Za-z@])', text):
            raise ValueError('Macro locale senza conversione web: ' + chr(92) + name)
    return text,sudoku



def inspect_figure_issues(tex: str) -> dict:
    """Legge le figure pendenti direttamente dalle macro del sorgente.

    Non deduce che un problema sia completo dall'assenza di segnalazioni.
    """
    pst = 0
    missing = []
    for field in FIELDS:
        value = extract_macro(tex, field)
        if value is None:
            continue
        # Un unico riconoscitore per inventario e conversione.
        _, nfig, refs = preprocess(value)
        pst += nfig
        missing.extend(
            {'campo': field, 'riferimento': ref}
            for ref in refs
        )
    return {'pstricks': pst, 'da_ricostruire': missing}



def extract_macro(text: str, name: str) -> str | None:
    pattern=r'\\renewcommand\s*\{\\'+re.escape(name)+r'\}\s*\{'
    match=re.search(pattern,text)
    if match is None:return None
    start=i=match.end()
    depth=1
    while i<len(text):
        c=text[i]
        if c=='\\':
            i+=2
            continue
        if c=='{':depth+=1
        elif c=='}':
            depth-=1
            if depth==0:return text[start:i]
        i+=1
    raise ValueError(f'La macro {name} non e chiusa')


def no_comments(text: str) -> str:
    lines=[]
    for line in text.splitlines():
        for i,ch in enumerate(line):
            if ch=='%':
                backslashes=0
                j=i-1
                while j>=0 and line[j]=='\\':backslashes+=1;j-=1
                if backslashes%2==0:
                    line=line[:i]
                    break
        lines.append(line)
    return '\n'.join(lines).strip()


def has_content(text: str | None) -> bool:
    if text is None:return False
    # Anche un campo contenente solo un disegno da completare e' contenuto.
    if MISSING_FIGURE_RE.search(text):return True
    v=no_comments(text)
    if PSTRICKS_INLINE_RE.search(v) or PSTRICKS_ENV_RE.search(v):return True
    v=re.sub(r'\\(?:ldots|dots|quad|qquad|par|medskip|smallskip)\b','',v)
    v=re.sub(r'\\[A-Za-z@]+\*?(?:\[[^\]]*\])?','',v)
    return bool(re.sub(r'[{}\s.~\\]','',v))


def preprocess(text: str) -> tuple[str,int,list[str]]:
    missing=[]

    def mark_missing(match):
        missing.append(match.group('ref').strip())
        # I ritorni a capo isolano il marcatore come blocco Pandoc.
        return '\n\nSSSUPFIGURAMANCANTE'+str(len(missing))+'FINE\n\n'

    text=MISSING_FIGURE_RE.sub(mark_missing,text)
    text=no_comments(text)
    # Le sei invocazioni nel 2010.4 generano ciascuna un intero pspicture
    # nella macro locale. Segnalarle come disegno anziche' farle sparire.
    text=AREA_RE.sub(r'\\pspicture\\endpspicture', text)
    for letter in 'ABCDEFG':
        text=re.sub(r'\\Domanda'+letter+r'\b',r'\\textbf{Punto ('+letter.lower()+r').} ',text)
    text=re.sub(r'\\TitoloSoluzione\b','',text)
    figure_count=0
    def figure(m):
        nonlocal figure_count
        figure_count+=1
        # Spazi essenziali: evitiamo che \hfill immediatamente precedente
        # inglobi il segnaposto nel nome del comando LaTeX letto da Pandoc.
        return ' SSSUPFIGURASEGNAPOSTO'+str(figure_count)+'FINE '
    # Riconosce blocchi PSTricks completi, anche se annidati.
    # Conta soltanto i disegni esterni.
    commands = re.compile(
        r'\\(?:begin\{pspicture\*?\}|end\{pspicture\*?\}|'
        r'endpspicture(?![A-Za-z@])|pspicture\*?(?![A-Za-z@]))'
    )

    parts = []
    last = 0
    start = None
    depth = 0

    for match in commands.finditer(text):
        command = match.group()

        closing = (
            command.startswith(r'\endpspicture')
            or command.startswith(r'\end{pspicture')
        )

        if closing:
            if depth == 0:
                raise ValueError("PSTricks: chiusura senza apertura")

            depth -= 1

            if depth == 0:
                parts.append(text[last:start])
                parts.append(figure(match))
                last = match.end()
                start = None
        else:
            if depth == 0:
                start = match.start()
            depth += 1

    if depth != 0:
        raise ValueError("PSTricks: disegno non chiuso")

    parts.append(text[last:])
    text = ''.join(parts)
    text=re.sub(r'\\psset\{[^{}]*\}','',text)
    return text,figure_count,missing


def convert(text: str, provenance: str, local_defs=(), svg_index=None, source_hash=None) -> tuple[str,int]:
    text, figures, missing=preprocess(text)
    text, sudoku_html = render_local_macros(text, local_defs)

    # Protegge ambienti numerati e riferimenti prima di Pandoc.
    protected = {}

    def preserve(match):
        token = f'SSSUPMATHPRESERVED{len(protected):05d}END'
        protected[token] = match.group(0)
        return token

    envs = r'equation\*?|align\*?|gather\*?|multline\*?|flalign\*?|alignat\*?'
    text = re.sub(
        r'\\begin\{(' + envs + r')\}.*?\\end\{\1\}',
        preserve, text, flags=re.S
    )
    text = re.sub(
        r'\\(?:ref|eqref)\{[^{}]+\}',
        preserve, text
    )

    run=subprocess.run(['pandoc','--from=latex','--to=html5','--mathjax','--wrap=none'],input=text,text=True,capture_output=True)
    if run.returncode:
        raise RuntimeError(f'Pandoc {provenance}: {run.stderr[-1800:]}')
    h=run.stdout.strip()
    for token, latex in protected.items():
        h=h.replace(token, escape(latex))
    if not h and has_content(text):raise RuntimeError(f'Conversione vuota per {provenance}')
    for token, table in sudoku_html.items():
        if token not in h:
            raise RuntimeError(f'Sudoku non reso da Pandoc in {provenance}: {token}')
        h=h.replace('<p>'+token+'</p>',table).replace(token,table)
    for n in range(1,figures+1):
        token='SSSUPFIGURASEGNAPOSTO'+str(n)+'FINE'
        file_name, field = provenance.split('/', 1)
        figure_id = Path(file_name).stem + '__' + field + '__' + f'{n:02d}'
        asset = (svg_index or {}).get(figure_id)
        if asset and asset.get('sha256_sorgente') == source_hash:
            url = 'assets/figure/' + figure_id + '.svg'
            alt = f'Figura {n} del problema {Path(file_name).stem[3:].replace("_", ".")}, campo {field}'
            marker = (f'<a class="pstricks-figure-link" href="{escape(url, quote=True)}" '
                      f'target="_blank" rel="noopener noreferrer" title="Apri la figura vettoriale" '
                      f'style="display:inline-block;vertical-align:middle;max-width:100%;margin:.55em .25em;text-align:center">'
                      f'<img class="pstricks-svg" loading="lazy" decoding="async" '
                      f'style="display:block;max-width:100%;max-height:520px;width:auto;height:auto" '
                      f'src="{escape(url, quote=True)}" alt="{escape(alt, quote=True)}"></a>')
        else:
            marker = ('<span class="figure-placeholder">Disegno PSTricks non ancora '
                      'convertito o da rigenerare (figura ' + str(n) + ').</span>')
        h=h.replace('<p>'+token+'</p>',marker).replace(token,marker)
    for n, reference in enumerate(missing, 1):
        token='SSSUPFIGURAMANCANTE'+str(n)+'FINE'
        marker=('<span class="figure-placeholder">Figura da ricostruire in LaTeX '
                '(riferimento storico: '+escape(reference)+').</span>')
        h=h.replace('<p>'+token+'</p>',marker).replace(token,marker)
    return h,figures




def carica_svg(sito: Path) -> dict[str, dict]:
    """SVG pubblicabili solo se file e impronte concordano con il catalogo.

    L'installatore genera manifest.json dopo il controllo degli SVG. Se
    manca, il comportamento precedente (segnaposto) e' invariato.
    """
    directory = sito / 'assets' / 'figure'
    manifesto = directory / 'manifest.json'
    if not manifesto.is_file():
        return {}
    data = json.loads(manifesto.read_text(encoding='utf-8'))
    if data.get('schema') != 1 or not isinstance(data.get('figures'), list):
        raise RuntimeError(f'Manifest SVG non valido: {manifesto}')
    figures: dict[str, dict] = {}
    for item in data['figures']:
        name = item.get('id', '')
        if not re.fullmatch(r'SA_\d{4}_\d+__[A-Za-z]+__\d{2}', name):
            raise RuntimeError(f'Identificativo SVG sospetto: {name!r}')
        if name in figures:
            raise RuntimeError(f'SVG duplicato: {name}')
        path = directory / (name + '.svg')
        # Un file mancante o cambiato non puo' essere pubblicato come valido.
        if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == item.get('sha256_svg'):
            figures[name] = item
        else:
            print(f'AVVISO SVG mancante o non valido: {name}', file=sys.stderr)
    return figures


def generator_sha256() -> str:
    """Impronta delle regole effettive di conversione, inclusa la configurazione."""
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def pandoc_version() -> str:
    """La versione di Pandoc fa parte dell'identita del convertitore."""
    out=subprocess.run(['pandoc','--version'],text=True,capture_output=True,check=True).stdout
    return out.splitlines()[0]


def sections_sha256(sections: dict) -> str:
    b=json.dumps(sections,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf-8')
    return hashlib.sha256(b).hexdigest()


def read_problem(path: Path) -> dict | None:
    """Legge soltanto il JSON del wrapper JS generato; non esegue JavaScript."""
    try:
        raw=path.read_text(encoding='utf-8').strip()
        if not (raw.startswith(JS_PREFIX) and raw.endswith(JS_SUFFIX)):
            return None
        payload=json.loads(raw[len(JS_PREFIX):-len(JS_SUFFIX)])
        return payload if isinstance(payload,dict) else None
    except (OSError,ValueError,UnicodeError):
        return None


def conversion_status(src: Path, output: Path, title: str,
                      version_hash: str, pandoc_id: str, svg_index_hash: str | None=None) -> tuple[str,str]:
    """Verifica indipendente dalla cache locale e senza scrivere nulla."""
    # sito_check usa questa funzione senza passare il valore esplicito.
    if svg_index_hash is None:
        manifest = output.parent.parent.parent / 'assets' / 'figure' / 'manifest.json'
        svg_index_hash = (hashlib.sha256(manifest.read_bytes()).hexdigest()
                          if manifest.is_file() else '')
    if not output.exists():
        return 'MANCANTE','nessun file web generato'
    data=read_problem(output)
    if data is None:
        return 'ERRORE','file web illeggibile o formato imprevisto'
    m=re.fullmatch(r'SA_(\d{4})_(\d+)\.tex',src.name)
    if not m or data.get('year')!=int(m.group(1)) or data.get('number')!=int(m.group(2)):
        return 'ERRORE','identificativo anno/problema incoerente'
    if data.get('source')!=src.name:
        return 'ERRORE','nome del sorgente incoerente'
    if not isinstance(data.get('sections'),dict) or not data['sections'].get('Testo'):
        return 'ERRORE','manca il testo web'
    try:
        digest=hashlib.sha256(src.read_bytes()).hexdigest()
    except OSError as e:
        return 'ERRORE',f'sorgente non leggibile: {e}'
    meta=data.get('_build')
    if not isinstance(meta,dict):
        return 'OBSOLETO','conversione legacy priva di impronte verificabili'
    if meta.get('sections_sha256')!=sections_sha256(data['sections']):
        return 'ERRORE','frammenti HTML modificati dopo la conversione'
    # Verifica anche i file SVG fisici, non soltanto le impronte dei dati web.
    svg_links = [rel for body in data['sections'].values()
                 for rel in re.findall(
                     r'src="(assets/figure/SA_\d{4}_\d+__[A-Za-z]+__\d{2}\.svg)"', body)]
    if svg_links:
        svg_manifest = output.parent.parent.parent / 'assets' / 'figure' / 'manifest.json'
        try:
            svg_metadata = json.loads(svg_manifest.read_text(encoding='utf-8'))
            asset_hashes = {item['id']: item['sha256_svg']
                            for item in svg_metadata['figures']}
        except (OSError, ValueError, KeyError, TypeError):
            return 'ERRORE', 'manifest SVG mancante o malformato'
        for rel in svg_links:
            full_path = output.parent.parent.parent / rel
            fig_id = full_path.stem
            if not full_path.is_file():
                return 'OBSOLETO', f'immagine SVG mancante: {rel}'
            if hashlib.sha256(full_path.read_bytes()).hexdigest() != asset_hashes.get(fig_id):
                return 'OBSOLETO', f'immagine SVG alterata: {rel}'
    figures=data.get('figure_issues')
    if not isinstance(figures,dict) or meta.get('figures_sha256')!=sections_sha256(figures):
        return 'OBSOLETO','metadati sulle figure assenti o da rigenerare'
    provenance=data.get('provenance')
    if not isinstance(provenance,dict) or set(provenance)!=set(data['sections']):
        return 'OBSOLETO','provenienza dei campi assente o incompleta'
    if meta.get('provenance_sha256')!=sections_sha256(provenance):
        return 'ERRORE','metadati di provenienza modificati dopo la conversione'
    if meta.get('latex_sha256')!=digest:
        return 'OBSOLETO','il sorgente LaTeX e cambiato'
    if meta.get('generator_sha256')!=version_hash:
        return 'OBSOLETO','regole del generatore modificate'
    # L'indice SVG cambia quando aggiorniamo una figura senza toccare il LaTeX.
    if meta.get('svg_index_sha256') != svg_index_hash:
        return 'OBSOLETO','inventario SVG aggiornato'
    if meta.get('pandoc_version')!=pandoc_id:
        return 'OBSOLETO','versione Pandoc cambiata'
    if data.get('title')!=title:
        return 'OBSOLETO','titolo modificato'
    return 'ALLINEATO','impronte corrispondenti (non equivale a revisione matematica)'

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--sorgenti',type=Path,default=Path('contenuti/problemi'))
    p.add_argument('--sito',type=Path,default=Path('sito'))
    p.add_argument('--anno',type=int)
    p.add_argument('--problema',type=int)
    p.add_argument('--force',action='store_true')
    args=p.parse_args()
    if args.problema and not args.anno:p.error('--problema richiede --anno')
    if not args.sorgenti.is_dir():p.error('Non trovo la directory sorgenti '+str(args.sorgenti))
    if not shutil.which('pandoc'):p.error('Pandoc non e installato: puoi comunque aprire l\'anteprima HTML gia generata.')
    dest=args.sito/'dati'
    (dest/'problemi').mkdir(parents=True,exist_ok=True)
    # La vecchia build_cache.json non e piu usata: le impronte
    # viaggiano insieme a ciascun file web, anche su GitHub.
    gen_id=generator_sha256()
    pandoc_id=pandoc_version()
    title_path=dest/'titoli.json'
    titles=json.loads(title_path.read_text(encoding='utf8')) if title_path.exists() else {}
    svg_index=carica_svg(args.sito)
    svg_manifest=args.sito/'assets'/'figure'/'manifest.json'
    svg_index_hash=(hashlib.sha256(svg_manifest.read_bytes()).hexdigest()
                    if svg_manifest.is_file() else '')
    files=sorted(args.sorgenti.glob('SA_????_*.tex'))
    all_files=[]
    for f in files:
        m=re.fullmatch(r'SA_(\d{4})_(\d+)\.tex',f.name)
        if m:all_files.append((int(m.group(1)),int(m.group(2)),f))
    selected=[(y,n,f) for y,n,f in all_files if (args.anno is None or y==args.anno) and (args.problema is None or n==args.problema)]
    if not selected:p.error('Nessun problema canonico corrispondente alla selezione')
    changed=skipped=0
    total_ai_esposte=0
    for y,n,f in selected:
        key=f'{y}_{n}'
        digest=hashlib.sha256(f.read_bytes()).hexdigest()
        path=dest/'problemi'/f'{key}.js'
        title=titles.get(key,f'Problema {n}')
        state,why=conversion_status(f,path,title,gen_id,pandoc_id,svg_index_hash)
        if not args.force and state=='ALLINEATO':
            skipped+=1
            continue
        tex=f.read_text(encoding='utf8')
        fields={}
        provenance={}
        pictures=0
        issues=inspect_figure_issues(tex)
        local_defs=set(LOCAL_DEF_RE.findall(tex))
        for field in FIELDS:
            v=extract_macro(tex,field)
            if not has_content(v):continue
            origin=field_provenance(v or '',field)
            html,nfig=convert(v or '',f'{f.name}/{field}',local_defs,svg_index,digest)
            if html:
                fields[field]=html
                provenance[field]=origin
                total_ai_esposte+=int(origin['tipo']=='ai')
            pictures+=nfig
        if not fields.get('Testo'):
            print('ERRORE: testo mancante o vuoto in',f.name,file=sys.stderr)
            return 2
        # Il preprocessore conta i disegni esterni, senza contare
        # separatamente gli eventuali pspicture annidati.
        # Questo e' il numero di segnaposto effettivamente prodotti.
        if pictures != issues['pstricks']:
            raise RuntimeError(
                f'Conteggio PSTricks incoerente in {f.name}: '
                f"conversione={pictures}, inventario={issues['pstricks']}"
            )
        converted=sum(html.count('class="pstricks-svg"') for html in fields.values())
        issues['pstricks_totali']=pictures
        issues['pstricks_svg']=converted
        # Compatibilita' con sito_check: pstricks indica i disegni irrisolti.
        issues['pstricks']=pictures-converted
        problem={'year':y,'number':n,'title':title,'source':f.name,
                 'sections':fields,'provenance':provenance,'figure_issues':issues}
        problem['_build']={
            'latex_sha256':digest,
            'generator_sha256':gen_id,
            'svg_index_sha256':svg_index_hash,
            'pandoc_version':pandoc_id,
            'sections_sha256':sections_sha256(fields),
            'figures_sha256':sections_sha256(issues),
            'provenance_sha256':sections_sha256(provenance),
        }
        warnings=[]
        if issues['pstricks']:
            warnings.append(f"{issues['pstricks']} figure PSTricks da convertire o rigenerare")
        if issues['da_ricostruire']:
            warnings.append(f"{len(issues['da_ricostruire'])} figure da ricostruire in LaTeX")
        if warnings:
            problem['warning']='; '.join(warnings)+'. Verificare prima di pubblicare.'
        payload='window.SSSUP.registerProblem('+json.dumps(problem,ensure_ascii=False,separators=(',',':'))+');\n'
        path.write_text(payload,encoding='utf8')
        changed+=1
        print('CONVERTITO',f.name,':',len(fields),'campi')
    count_by_year={}
    for y,n,f in all_files:count_by_year[y]=count_by_year.get(y,0)+1
    rows=[]
    for y in range(1996,max(2026,max(count_by_year,default=2026))+1):
        count=count_by_year.get(y,0)
        preview=sum((dest/'problemi'/f'{y}_{n}.js').exists() for yr,n,f in all_files if yr==y)
        rows.append({'year':y,'count':count,'preview':preview,'missing':count==0})
    manifest={'range':[rows[0]['year'],rows[-1]['year']],'years':rows}
    (dest/'manifest.js').write_text('window.SSSUP_CATALOG='+json.dumps(manifest,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf8')
    print(f'Fine. Convertiti {changed}, gia aggiornati {skipped}. Interfaccia HTML/CSS/JS non modificata.')
    if total_ai_esposte:
        print(f'Bozze AI esposte nei dati web: {total_ai_esposte} '
              '(ciascuna con metadati di provenienza).')
    return 0

if __name__=='__main__':raise SystemExit(main())
