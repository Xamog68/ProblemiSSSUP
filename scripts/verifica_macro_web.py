#!/usr/bin/env python3
"""Controlli in sola lettura delle conversioni locali dei problemi SSSUP.

Uso dalla radice del repository:
    python3 ~/Downloads/verifica_macro_web.py

Richiede pandoc e scripts/genera_dati_sito.py.
"""
from __future__ import annotations
from pathlib import Path
import importlib.util
import re
import sys

ROOT = Path.cwd()
GEN = ROOT / 'scripts/genera_dati_sito.py'
BASE = ROOT / 'contenuti/problemi'


def require(ok, explanation):
    if not ok:
        raise AssertionError(explanation)


def main():
    require(GEN.is_file() and BASE.is_dir(), 'Avviare dalla radice del repository')
    spec = importlib.util.spec_from_file_location('sssup_web_generator', GEN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    def source(year, number):
        return (BASE / f'SA_{year}_{number}.tex').read_text(encoding='utf-8')
    def field(tex, name):
        return mod.extract_macro(tex, name)
    def convert(tex, name):
        defs = set(mod.LOCAL_DEF_RE.findall(tex))
        return mod.convert(field(tex, name), f'test/{name}', defs)

    t=source(2005,1)
    n=[convert(t, name)[0].count('class="sssup-sudoku"')
       for name in ('Testo','SoluzioneUfficiale','SoluzioniAlternative')]
    require(n == [1, 10, 20], f'Sudoku attesi [1,10,20], trovati {n}')
    h,_=convert(t,'Testo')
    require(h.count('<td ') == 16, 'Il Sudoku dell\'enunciato non ha 16 caselle')

    t=source(2009,3)
    fields=('Testo','SoluzioneUfficiale')
    converted={name:convert(t,name)[0] for name in fields}
    require(sum(h.count(r'\begin{array}{|c|c|}') for h in converted.values()) == 53,
            'Attese 53 tessere domino convertite')
    require(all(r'\domino' not in h for h in converted.values()), 'Rimane un comando domino')

    t=source(2010,4)
    issues=mod.inspect_figure_issues(t)
    require(issues['pstricks']==11, '2010.4: attesi 5 disegni diretti e 6 dalle macro locali')
    html,n=convert(t,'Osservazioni')
    require(n==6 and html.count('Disegno PSTricks non ancora convertito')==6,
            '2010.4: sei disegni macro non segnalati')

    # Fail-closed: una futura macro locale sconosciuta non deve sparire.
    try:
        mod.convert(r'\UnmappedMacro{abc}', 'test/macro_ignota', {'UnmappedMacro'})
    except ValueError:
        pass
    else:
        raise AssertionError('Una macro locale ignota non ha prodotto errore')

    t=source(2021,1)
    for name in ('Risposta','Aiutino','SoluzioneRedazionale'):
        require(mod.AI_DRAFT_RE.search(field(t,name)) is not None,
                f'Bozza AI {name} non riconosciuta')
        require(mod.field_provenance(field(t,name),name)['tipo']=='ai',
                f'Bozza AI {name} senza provenienza esplicita')
    require('SoluzioneRedazionale' in mod.FIELDS,
            'Le soluzioni AI devono essere esportate con etichette')
    original=source(2005,1)
    require(mod.field_provenance(field(original,'SoluzioneUfficiale'),
                                 'SoluzioneUfficiale')['tipo']=='preesistente',
            'Una soluzione preesistente e stata classificata AI')
    # In caso di marcatori AI incompleti il convertitore deve fermarsi.
    try:
        mod.field_provenance('% SSSUP-BOZZA-AI: Risposta; stato=INCERTO\nProva',
                             'Risposta')
    except ValueError:
        pass
    else:
        raise AssertionError('Marcatore AI incompleto non rifiutato')
    print('VERIFICA MACRO WEB SUPERATA: 31 Sudoku, 53 tessere domino, '
          '6 grafici locali segnalati; bozze AI riconosciute con provenienza.')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('VERIFICA FALLITA:', e, file=sys.stderr)
        sys.exit(1)
