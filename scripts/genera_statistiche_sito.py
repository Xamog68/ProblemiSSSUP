#!/usr/bin/env python3
"""Sincronizza aggregati per la sezione 'Come e andata al concorso?'.

Eseguire dalla radice del repository:
  python3 scripts/genera_statistiche_sito.py
  python3 scripts/genera_statistiche_sito.py --includi-bozze  # SOLO anteprima locale

Non legge tabelloni/verbalini e non modifica mai il LaTeX.
Per pubblicare in modo ordinario, contrassegnare i soli dati verificati con
`pubblicabile: true` nei rispettivi file contenuti/statistiche/SA_*.json.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

RX=re.compile(r'SA_(\d{4})_(\d+)\.json$')
REQUIRED_TOP={'5','10','20'}


def validate(d: dict, filename: str) -> None:
    if not isinstance(d,dict) or d.get('schema')!=1:
        raise ValueError(f'{filename}: schema non valido')
    match=RX.fullmatch(filename)
    if not match or (int(match[1]),int(match[2])) != (d.get('anno'), d.get('numero')):
        raise ValueError(f'{filename}: identita non coerente')
    if d.get('problema')!=filename.removesuffix('.json'):
        raise ValueError(f'{filename}: chiave problema incoerente')
    n=d.get('elaborati')
    if not isinstance(n,int) or n<=0 or n>=10000:
        raise ValueError(f'{filename}: numerosita non valida')
    if not isinstance(d.get('pubblicabile'),bool):
        raise ValueError(f'{filename}: pubblicabile deve essere booleano')
    if d.get('stato') not in ('bozza_da_verificare','quantitativo_controllato','verificato'):
        raise ValueError(f'{filename}: stato non riconosciuto')
    # La pubblicazione di bozze richiede una marcatura AI esplicita.
    # La revisione rimane 'bozza_da_verificare'; non si finge una validazione.
    if d.get('pubblicabile') and d.get('stato')=='bozza_da_verificare' and d.get('ai_da_verificare') is not True:
        raise ValueError(f'{filename}: bozza pubblicabile solo con ai_da_verificare=true')
    if not isinstance(d.get('ai_da_verificare'), bool):
        raise ValueError(f'{filename}: manca la dichiarazione ai_da_verificare')
    ss=d.get('sottodomande')
    if not isinstance(ss,list) or len(ss) not in (2,3,4,5) or len(ss)!=len({x.get('id') for x in ss}):
        raise ValueError(f'{filename}: sottodomande non valide')
    for sub in ss:
        a=sub.get('contributo');b=sub.get('sostanzialmente_completo')
        if not all(isinstance(x,int) for x in (a,b)) or not 0<=b<=a<=n:
            raise ValueError(f'{filename}: conteggi errati nel punto {sub.get("id")}')
    top=d.get('top_matematica')
    if not isinstance(top,dict) or set(top)!=REQUIRED_TOP:
        raise ValueError(f'{filename}: top 5/10/20 mancanti')
    for key,g in top.items():
        if not isinstance(g,dict) or not isinstance(g.get('effettivi'),int) or g['effettivi']<int(key):
            raise ValueError(f'{filename}: gruppo top {key} non valido')
        for field in ('contributo_problema','almeno_meta','almeno_quattro_quinti','anche_top_problema'):
            v=g.get(field)
            if not isinstance(v,int) or not 0<=v<=g['effettivi']:
                raise ValueError(f'{filename}: {field} non valido per top {key}')
        if 'completi_sostanziali' in g:
            points=g['completi_sostanziali']
            if set(points) != {row['id'] for row in ss}:
                raise ValueError(f'{filename}: sottodomande top {key} incoerenti')
            for letter,point in points.items():
                if point.get('stato') not in ('controllato','ricostruzione_da_verificare','non_ricostruibile'):
                    raise ValueError(f'{filename}: stato non valido per top {key}/{letter}')
                a=point.get('documentati');b=point.get('da_verificare')
                if not all(isinstance(v,int) for v in (a,b)) or min(a,b)<0 or a+b>g['effettivi']:
                    raise ValueError(f'{filename}: valori incoerenti per top {key}/{letter}')
        if 'completi_stretti' in g:
            if any(not isinstance(v,int) or v<0 or v>g['effettivi'] for v in g['completi_stretti'].values()):
                raise ValueError(f'{filename}: completi_stretti errati')
    if not isinstance(d.get('osservazioni'),list) or not all(isinstance(s,str) for s in d['osservazioni']):
        raise ValueError(f'{filename}: osservazioni mancanti')
    forbidden={'nome','cognome','candidato','matricola','email','punteggi_individuali','id_personale'}
    if forbidden.intersection(d.keys()):
        raise ValueError(f'{filename}: chiavi personali non ammesse')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path('.'))
    p.add_argument('--includi-bozze',action='store_true',help='Solo anteprima locale; non committare i dati web generati')
    args=p.parse_args()
    root=args.root.resolve(); source=root/'contenuti/statistiche'; target=root/'sito/dati/statistiche'
    if not (root/'sito/index.html').exists() or not source.is_dir():
        p.error('Eseguire dalla radice del repository, con contenuti/statistiche installati')
    validated=[]
    for f in sorted(source.glob('SA_*.json')):
        item=json.loads(f.read_text(encoding='utf-8'))
        validate(item,f.name)
        if item['pubblicabile'] or args.includi_bozze:
            validated.append((f,item))
    target.mkdir(parents=True,exist_ok=True)
    expected={f.name for f,_ in validated}
    for old in target.glob('SA_*.json'):
        if old.name not in expected: old.unlink()
    for src,data in validated:
        out=target/src.name
        encoded=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
        if not out.exists() or out.read_text(encoding='utf-8')!=encoded:
            out.write_text(encoded,encoding='utf-8')
    manifest={'schema':1,'problemi':[d['problema'] for _,d in validated]}
    index=target/'indice.json'; output=json.dumps(manifest,ensure_ascii=False,indent=2)+'\n'
    if not index.exists() or index.read_text(encoding='utf-8')!=output:
        index.write_text(output,encoding='utf-8')
    print(f'Statistiche web: {len(validated)} schede ({len(list(source.glob("SA_*.json")))} totali nel catalogo)')
    if args.includi_bozze:
        print('ATTENZIONE: versione per anteprima con conteggi provvisori! Prima del push rieseguire SENZA --includi-bozze.')
    else:
        print('Versione pubblicabile. Le bozze non sono incluse nei file dati web.')

if __name__=='__main__':main()
