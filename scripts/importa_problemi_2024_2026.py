#!/usr/bin/env python3
"""Importa i testi SSSUP 2024-2026 senza immagini e commenti editoriali.

Usare dalla radice del progetto (o da qualsiasi directory):
    python3 scripts/importa_problemi_2024_2026.py
    python3 scripts/importa_problemi_2024_2026.py --write

Gli originali sotto fonti-locali/ non sono mai modificati. I file canonici
esistenti non vengono mai sovrascritti. Le figure devono essere ridisegnate
nel sorgente LaTeX; i PDF originari restano solo come riferimento locale.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'contenuti' / 'problemi'

CAMPI_VUOTI = (
    'Risposta', 'Aiutino', 'SoluzioneUfficiale',
    'SoluzioniAlternative', 'Osservazioni', 'Commenti',
)
ESERCIZIO = re.compile(r'(?m)^[ \t]*\\paragraph\{Esercizio ([1-3])\.?\}[ \t]*$')
FIGURA_2024 = re.compile(
    r'(?m)^[ \t]*\\begin\{center\}[ \t]*\n'
    r'[ \t]*\\includegraphics\[scale=0\.4\]\{squares\.pdf\}[ \t]*\n'
    r'[ \t]*\\end\{center\}[ \t]*$'
)
FIGURA_2026 = re.compile(
    r'\A\s*\\begin\{wrapfigure\}\{r\}\{0\.23\\textwidth\}'
    r'.*?\\includegraphics\[scale=0\.75\]\{es1\.pdf\}'
    r'.*?\\end\{wrapfigure\}\s*\Z', re.S
)
NOTE = {
    (2024, 2): (
        '% TODO FIGURA: ricostruire direttamente in LaTeX il disegno dei nove'
        ' quadrati, cerniere, rombi ed elastico.\n'
        '% Riferimento storico (non importare): fonti-locali/2024/squares.pdf'
    ),
    (2026, 1): (
        '% TODO FIGURA: ricostruire direttamente in LaTeX il quadrilatero'
        ' con i lati 2, 4, 5, 3 e il vertice A.\n'
        '% Riferimento storico (non importare): fonti-locali/2026/es1.pdf'
    ),
}


def pulisci(testo: str) -> str:
    """Elimina commenti TeX e spazi superflui, preservando i caratteri \\%."""
    righe = []
    for riga in testo.splitlines():
        # Un % in TeX apre un commento solo se non e' preceduto da un
        # numero dispari di backslash consecutivi.
        for i, carattere in enumerate(riga):
            if carattere != '%':
                continue
            n_backslash = 0
            j = i - 1
            while j >= 0 and riga[j] == '\\':
                n_backslash += 1
                j -= 1
            if n_backslash % 2 == 0:
                riga = riga[:i]
                break
        riga = riga.rstrip(' \t')
        if riga or (righe and righe[-1]):
            righe.append(riga)
    while righe and not righe[0]:
        righe.pop(0)
    while righe and not righe[-1]:
        righe.pop()
    return '\n'.join(righe)


def estrai(anno: int) -> list[tuple[int, str]]:
    fonte = ROOT / 'fonti-locali' / str(anno) / f'SA_{anno}_testi_chat.tex'
    originale = fonte.read_text(encoding='utf-8')
    marcatori = list(ESERCIZIO.finditer(originale))
    numeri = [int(m.group(1)) for m in marcatori]
    if numeri != [1, 2, 3]:
        raise ValueError(f'{fonte}: esercizi inattesi {numeri}')

    intestazione = originale[:marcatori[0].start()]
    if anno == 2026:
        if not FIGURA_2026.fullmatch(intestazione):
            raise ValueError('2026: figura iniziale diversa da quella attesa')
    elif intestazione.strip():
        raise ValueError(f'{anno}: materiale inatteso prima del primo esercizio')

    risultati = []
    for i, m in enumerate(marcatori):
        fine = marcatori[i + 1].start() if i + 1 < len(marcatori) else len(originale)
        frammento = originale[m.end():fine]
        if (anno, i + 1) == (2024, 2):
            frammento, sostituzioni = FIGURA_2024.subn('@@FIGURA_2024_2@@', frammento)
            if sostituzioni != 1:
                raise ValueError('2024.2: figura non trovata esattamente una volta')
        frammento = pulisci(frammento)
        if (anno, i + 1) == (2024, 2):
            frammento = frammento.replace('@@FIGURA_2024_2@@', NOTE[(2024, 2)])
        if (anno, i + 1) == (2026, 1):
            frammento = NOTE[(2026, 1)] + '\n\n' + frammento
        if re.search(r'\\(?:includegraphics|input|include)\b|\\begin\{wrapfigure\}', frammento):
            raise ValueError(f'{anno}.{i + 1}: riferimento esterno residuo')
        if not frammento.strip():
            raise ValueError(f'{anno}.{i + 1}: testo vuoto')
        risultati.append((i + 1, frammento))
    return risultati


def genera(anno: int, numero: int, testo: str) -> str:
    pezzi = [
        f'\\renewcommand{{\\Anno}}{{{anno}}}',
        f'\\renewcommand{{\\NumeroProblema}}{{{numero}}}',
        '\\renewcommand{\\Testo}{\n' + testo + '\n}',
    ]
    pezzi.extend(f'\\renewcommand{{\\{nome}}}{{}}' for nome in CAMPI_VUOTI)
    return '\n\n'.join(pezzi) + '\n'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='crea i file; default: solo anteprima')
    args = parser.parse_args()

    operazioni = []
    for anno in (2024, 2025, 2026):
        for numero, testo in estrai(anno):
            destinazione = DEST / f'SA_{anno}_{numero}.tex'
            operazioni.append((destinazione, genera(anno, numero, testo)))
    for percorso, contenuto in operazioni:
        if percorso.exists():
            print(f'ESISTE     {percorso.name} (non sovrascritto)')
        elif args.write:
            with percorso.open('x', encoding='utf-8', newline='\n') as out:
                out.write(contenuto)
            print(f'CREATO     {percorso.name}')
        else:
            print(f'DA CREARE  {percorso.name}')


if __name__ == '__main__':
    main()
