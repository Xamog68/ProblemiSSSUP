#!/usr/bin/env python3
"""Genera SOLO i dati web dei problemi LaTeX, senza riscrivere HTML/CSS/JS.

Esecuzione dalla radice di ProblemiSSSUP:
  python3 scripts/genera_dati_sito.py
  python3 scripts/genera_dati_sito.py --anno 2013
  python3 scripts/genera_dati_sito.py --anno 2013 --problema 2

Richiede Pandoc. I sorgenti del repository NON vengono modificati.
La cache SHA-256 evita di convertire nuovamente i problemi invariati.
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

FIELDS=['Testo','Risposta','Aiutino','SoluzioneUfficiale','SoluzioniAlternative','Osservazioni','Commenti']


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
    v=no_comments(text)
    v=re.sub(r'\\(?:ldots|dots|quad|qquad|par|medskip|smallskip)\b','',v)
    v=re.sub(r'\\[A-Za-z@]+\*?(?:\[[^\]]*\])?','',v)
    return bool(re.sub(r'[{}\s.~\\]','',v))


def preprocess(text: str) -> tuple[str,int]:
    text=no_comments(text)
    for letter in 'ABCDEFG':
        text=re.sub(r'\\Domanda'+letter+r'\b',r'\\textbf{Punto ('+letter.lower()+r').} ',text)
    text=re.sub(r'\\TitoloSoluzione\b','',text)
    figure_count=0
    def figure(m):
        nonlocal figure_count
        figure_count+=1
        return 'SSSUPFIGURASEGNAPOSTO'+str(figure_count)+'FINE'
    text=re.sub(r'\\pspicture\b.*?\\endpspicture\b',figure,text,flags=re.S)
    text=re.sub(r'\\begin\{pspicture\}.*?\\end\{pspicture\}',figure,text,flags=re.S)
    text=re.sub(r'\\psset\{[^{}]*\}','',text)
    return text,figure_count


def convert(text: str, provenance: str) -> tuple[str,int]:
    text, figures=preprocess(text)

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
    return h,figures


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
    cache_path=dest/'build_cache.json'
    cache=json.loads(cache_path.read_text(encoding='utf8')) if cache_path.exists() else {}
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
        if not args.force and cache.get(key)==digest and path.exists():
            skipped+=1
            continue
        tex=f.read_text(encoding='utf8')
        fields={}
        warnings=[]
        pictures=0
        for field in FIELDS:
            v=extract_macro(tex,field)
            if not has_content(v):continue
            html,nfig=convert(v or '',f'{f.name}/{field}')
            if html:fields[field]=html
            pictures+=nfig
        if not fields.get('Testo'):
            print('ERRORE: testo mancante o vuoto in',f.name,file=sys.stderr)
            return 2
        problem={'year':y,'number':n,'title':titles.get(key,f'Problema {n}'),'source':f.name,'sections':fields}
        if pictures:problem['warning']=f'{pictures} disegni PSTricks sono segnaposto: verificare la resa grafica prima di pubblicare.'
        payload='window.SSSUP.registerProblem('+json.dumps(problem,ensure_ascii=False,separators=(',',':'))+');\n'
        path.write_text(payload,encoding='utf8')
        cache[key]=digest
        changed+=1
        print('CONVERTITO',f.name,':',len(fields),'campi')
    cache_path.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
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
