#!/usr/bin/env python3
"""Controlla l'allineamento LaTeX -> dati web senza modificare alcun file.

Uso dalla radice di ProblemiSSSUP:
  python3 scripts/sito_check.py
  python3 scripts/sito_check.py --anno 2013 --problema 1
  python3 scripts/sito_check.py --dettagli

Codice di uscita 0: tutti allineati. 1: conversioni mancanti/obsolete/errori.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import shutil

from genera_dati_sito import (conversion_status, generator_sha256,
                              pandoc_version, inspect_figure_issues)


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--sorgenti',type=Path,default=Path('contenuti/problemi'))
    p.add_argument('--sito',type=Path,default=Path('sito'))
    p.add_argument('--anno',type=int)
    p.add_argument('--problema',type=int)
    p.add_argument('--dettagli',action='store_true',help='mostra tutti gli elementi anziche un campione')
    args=p.parse_args()
    if args.problema and not args.anno:p.error('--problema richiede --anno')
    if not args.sorgenti.is_dir():p.error('Directory sorgenti non trovata: '+str(args.sorgenti))
    if not shutil.which('pandoc'):p.error('Pandoc non trovato nel PATH')
    title_path=args.sito/'dati/titoli.json'
    try:
        titles=json.loads(title_path.read_text(encoding='utf-8')) if title_path.exists() else {}
    except (ValueError,OSError) as exc:
        p.error(f'Impossibile leggere i titoli: {exc}')
    gen_id=generator_sha256()
    pandoc_id=pandoc_version()
    rows=[]
    figure_rows=[]
    for src in sorted(args.sorgenti.glob('SA_????_*.tex')):
        m=re.fullmatch(r'SA_(\d{4})_(\d+)\.tex',src.name)
        if not m:continue
        year,n=map(int,m.groups())
        if args.anno is not None and year!=args.anno:continue
        if args.problema is not None and n!=args.problema:continue
        key=f'{year}_{n}'
        target=args.sito/'dati/problemi'/f'{key}.js'
        title=titles.get(key,f'Problema {n}')
        state,why=conversion_status(src,target,title,gen_id,pandoc_id)
        rows.append((state,src.name,why))
        issues=inspect_figure_issues(src.read_text(encoding='utf-8'))
        if issues['pstricks'] or issues['da_ricostruire']:
            figure_rows.append((src.name,issues))
    if not rows:p.error('Nessun sorgente canonico corrisponde alla selezione')
    counts=Counter(state for state,_,_ in rows)
    print('ProblemiSSSUP - allineamento LaTeX/web')
    print(f'Problemi canonici esaminati: {len(rows)}')
    print(f'  ALLINEATO : {counts["ALLINEATO"]}')
    print(f'  OBSOLETO  : {counts["OBSOLETO"]}')
    print(f'  MANCANTE  : {counts["MANCANTE"]}')
    print(f'  ERRORE    : {counts["ERRORE"]}')
    pending=[x for x in rows if x[0]!='ALLINEATO']
    if pending:
        print('\nDa controllare:')
        limit=len(pending) if args.dettagli else 20
        for state,name,why in pending[:limit]:
            print(f'  {state:<8} {name}: {why}')
        if len(pending)>limit:
            print(f'  ... altri {len(pending)-limit} (usa --dettagli)')
    count_pst=sum(i['pstricks'] for _,i in figure_rows)
    count_missing=sum(len(i['da_ricostruire']) for _,i in figure_rows)
    print('\nFigure da trattare (controllo indipendente dall\'allineamento):')
    print(f'  INCOMPLETO (figure segnalate): {len(figure_rows)} problemi')
    print(f'  Disegni PSTricks non convertiti: {count_pst}')
    print(f'  Figure da ricostruire: {count_missing}')
    if figure_rows:
        limit=len(figure_rows) if args.dettagli else 12
        for name,issues in figure_rows[:limit]:
            pieces=[]
            if issues['pstricks']:
                pieces.append(f"{issues['pstricks']} PSTricks")
            if issues['da_ricostruire']:
                refs=', '.join(x['riferimento'] for x in issues['da_ricostruire'])
                pieces.append('da ricostruire: '+refs)
            print('  INCOMPLETO '+name+': '+'; '.join(pieces))
        if len(figure_rows)>limit:
            print(f'  ... altri {len(figure_rows)-limit} (usa --dettagli)')
    print('\nNB: ALLINEATO significa tecnicamente aggiornato, NON verificato sul piano matematico.')
    print('NB: assenza di figure segnalate non implica completezza editoriale.')
    return 1 if pending else 0


if __name__=='__main__':
    raise SystemExit(main())
