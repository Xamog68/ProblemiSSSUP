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

FIELDS=['Testo','Risposta','Aiutino','SoluzioneUfficiale','SoluzioniAlternative','Osservazioni','Commenti']

# I commenti-marcatori appartengono ai sorgenti canonici e non vengono
# mostrati da TeX. Nel sito diventano segnaposto nello stesso punto.
MISSING_FIGURE_RE = re.compile(
    r'^[ \t]*%[ \t]*SSSUP-FIGURA-DA-RICOSTRUIRE:[ \t]*(?P<ref>[^\r\n]+?)[ \t]*$',
    flags=re.M,
)
PSTRICKS_INLINE_RE = re.compile(r'\\pspicture\b.*?\\endpspicture\b', flags=re.S)
PSTRICKS_ENV_RE = re.compile(r'\\begin\{pspicture\}.*?\\end\{pspicture\}', flags=re.S)


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
        for match in MISSING_FIGURE_RE.finditer(value):
            missing.append({'campo': field, 'riferimento': match.group('ref').strip()})
        clean = no_comments(value)
        pst += len(PSTRICKS_INLINE_RE.findall(clean))
        clean = PSTRICKS_INLINE_RE.sub('', clean)
        pst += len(PSTRICKS_ENV_RE.findall(clean))
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
    for letter in 'ABCDEFG':
        text=re.sub(r'\\Domanda'+letter+r'\b',r'\\textbf{Punto ('+letter.lower()+r').} ',text)
    text=re.sub(r'\\TitoloSoluzione\b','',text)
    figure_count=0
    def figure(m):
        nonlocal figure_count
        figure_count+=1
        return 'SSSUPFIGURASEGNAPOSTO'+str(figure_count)+'FINE'
    text=PSTRICKS_INLINE_RE.sub(figure,text)
    text=PSTRICKS_ENV_RE.sub(figure,text)
    text=re.sub(r'\\psset\{[^{}]*\}','',text)
    return text,figure_count,missing


def convert(text: str, provenance: str) -> tuple[str,int]:
    text, figures, missing=preprocess(text)

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

    run=subprocess.run(['pandoc','--from=latex','--to=html5','--math-method=mathjax','--wrap=none'],input=text,text=True,capture_output=True)
    if run.returncode:
        raise RuntimeError(f'Pandoc {provenance}: {run.stderr[-1800:]}')
    h=run.stdout.strip()
    for token, latex in protected.items():
        h=h.replace(token, escape(latex))
    if not h and has_content(text):raise RuntimeError(f'Conversione vuota per {provenance}')
    for n in range(1,figures+1):
        token='SSSUPFIGURASEGNAPOSTO'+str(n)+'FINE'
        marker='<span class="figure-placeholder">Disegno PSTricks non ancora convertito (figura '+str(n)+').</span>'
        h=h.replace('<p>'+token+'</p>',marker).replace(token,marker)
    for n, reference in enumerate(missing, 1):
        token='SSSUPFIGURAMANCANTE'+str(n)+'FINE'
        marker=('<span class="figure-placeholder">Figura da ricostruire in LaTeX '
                '(riferimento storico: '+escape(reference)+').</span>')
        h=h.replace('<p>'+token+'</p>',marker).replace(token,marker)
    return h,figures



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
                      version_hash: str, pandoc_id: str) -> tuple[str,str]:
    """Verifica indipendente dalla cache locale e senza scrivere nulla."""
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
    figures=data.get('figure_issues')
    if not isinstance(figures,dict) or meta.get('figures_sha256')!=sections_sha256(figures):
        return 'OBSOLETO','metadati sulle figure assenti o da rigenerare'
    if meta.get('latex_sha256')!=digest:
        return 'OBSOLETO','il sorgente LaTeX e cambiato'
    if meta.get('generator_sha256')!=version_hash:
        return 'OBSOLETO','regole del generatore modificate'
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
    files=sorted(args.sorgenti.glob('SA_????_*.tex'))
    all_files=[]
    for f in files:
        m=re.fullmatch(r'SA_(\d{4})_(\d+)\.tex',f.name)
        if m:all_files.append((int(m.group(1)),int(m.group(2)),f))
    selected=[(y,n,f) for y,n,f in all_files if (args.anno is None or y==args.anno) and (args.problema is None or n==args.problema)]
    if not selected:p.error('Nessun problema canonico corrispondente alla selezione')
    changed=skipped=0
    for y,n,f in selected:
        key=f'{y}_{n}'
        digest=hashlib.sha256(f.read_bytes()).hexdigest()
        path=dest/'problemi'/f'{key}.js'
        title=titles.get(key,f'Problema {n}')
        state,why=conversion_status(f,path,title,gen_id,pandoc_id)
        if not args.force and state=='ALLINEATO':
            skipped+=1
            continue
        tex=f.read_text(encoding='utf8')
        fields={}
        pictures=0
        issues=inspect_figure_issues(tex)
        for field in FIELDS:
            v=extract_macro(tex,field)
            if not has_content(v):continue
            html,nfig=convert(v or '',f'{f.name}/{field}')
            if html:fields[field]=html
            pictures+=nfig
        if not fields.get('Testo'):
            print('ERRORE: testo mancante o vuoto in',f.name,file=sys.stderr)
            return 2
        # Controllo di coerenza fra inventario e conversione dei PSTricks.
        if pictures != issues['pstricks']:
            raise RuntimeError(f'Conteggio PSTricks incoerente in {f.name}: '
                               f"conversione={pictures}, inventario={issues['pstricks']}")
        problem={'year':y,'number':n,'title':title,'source':f.name,
                 'sections':fields,'figure_issues':issues}
        problem['_build']={
            'latex_sha256':digest,
            'generator_sha256':gen_id,
            'pandoc_version':pandoc_id,
            'sections_sha256':sections_sha256(fields),
            'figures_sha256':sections_sha256(issues),
        }
        warnings=[]
        if pictures:
            warnings.append(f'{pictures} figure PSTricks non convertite')
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
    return 0

if __name__=='__main__':raise SystemExit(main())
