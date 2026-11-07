#!/usr/bin/env python3
"""Importa i problemi 2021-2023 dai sorgenti annuali."""

from pathlib import Path
import argparse
import re

ROOT = Path(__file__).resolve().parents[1]
ORIGINI = {
    2021: "SA_21.tex",
    2022: "SA_22.tex",
    2023: "SA_23.tex",
}

CAMPI_VUOTI = (
    "Risposta",
    "Aiutino",
    "SoluzioneUfficiale",
    "SoluzioniAlternative",
    "Osservazioni",
    "Commenti",
)

PATTERN = re.compile(
    r"(?m)^[ \t]*\\paragraph\{Esercizio\s+([1-9]\d*)\.?\}[ \t]*$"
)


def pulisci(testo):
    righe = [r.rstrip(" \t") for r in testo.splitlines()]
    while righe and not righe[0]:
        righe.pop(0)
    while righe and not righe[-1]:
        righe.pop()
    return "\n".join(righe) + "\n"


def estrai(anno):
    sorgente = ROOT / "fonti-locali" / str(anno) / ORIGINI[anno]
    testo = sorgente.read_text(encoding="utf-8")

    corpo = testo.split(r"\begin{document}", 1)[1]
    corpo = corpo.split(r"\end{document}", 1)[0]

    marcatori = list(PATTERN.finditer(corpo))
    numeri = [int(m.group(1)) for m in marcatori]

    if numeri != [1, 2, 3]:
        raise ValueError(f"{anno}: esercizi inattesi: {numeri}")

    risultati = []

    for i, m in enumerate(marcatori):
        fine = (
            marcatori[i + 1].start()
            if i + 1 < len(marcatori)
            else len(corpo)
        )
        frammento = corpo[m.end():fine]

        if i == len(marcatori) - 1:
            taglio = re.search(
                r"(?m)^[ \t]*\\clearpage[ \t]*$", frammento
            )
            if taglio is None:
                raise ValueError(
                    f"{anno}: fine dell'ultimo esercizio non riconosciuta"
                )
            coda = frammento[taglio.end():]
            if any(
                r.strip() and not r.lstrip().startswith("%")
                for r in coda.splitlines()
            ):
                raise ValueError(f"{anno}: materiale inatteso in coda")
            frammento = frammento[:taglio.start()]

        frammento = re.sub(
            r"\s*\\clearpage\s*$", "", frammento
        )
        risultati.append((numeri[i], pulisci(frammento)))

    return risultati


def genera(anno, numero, testo):
    parti = [
        f"\\renewcommand{{\\Anno}}{{{anno}}}",
        f"\\renewcommand{{\\NumeroProblema}}{{{numero}}}",
        "\\renewcommand{\\Testo}{\n" + testo.rstrip("\n") + "\n}",
    ]
    for campo in CAMPI_VUOTI:
        parti.append(f"\\renewcommand{{\\{campo}}}{{}}")

    return "\n\n".join(parti) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write", action="store_true",
        help="crea i file (senza questa opzione mostra solo l'anteprima)"
    )
    args = parser.parse_args()

    operazioni = []

    # Prima controlliamo tutti i sorgenti, senza scrivere nulla.
    for anno in ORIGINI:
        for numero, testo in estrai(anno):
            destinazione = (
                ROOT / "contenuti" / "problemi"
                / f"SA_{anno}_{numero}.tex"
            )
            operazioni.append(
                (destinazione, genera(anno, numero, testo))
            )

    for destinazione, contenuto in operazioni:
        if destinazione.exists():
            print(f"ESISTE    {destinazione.name}")
        elif args.write:
            with destinazione.open("x", encoding="utf-8") as f:
                f.write(contenuto)
            print(f"CREATO    {destinazione.name}")
        else:
            print(f"DA CREARE {destinazione.name}")


if __name__ == "__main__":
    main()
