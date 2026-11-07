#!/usr/bin/env python3
from __future__ import annotations
"""Controlli strutturali non distruttivi sul cantiere ProblemiSSSUP."""

from collections import Counter
from pathlib import Path
import re
import sys


RADICE = Path(__file__).resolve().parents[1]
PROBLEMI = RADICE / "contenuti" / "problemi"

MACRO_OBBLIGATORIE = (
    "Anno",
    "NumeroProblema",
    "Testo",
    "Risposta",
    "Aiutino",
    "SoluzioneUfficiale",
    "SoluzioniAlternative",
    "Osservazioni",
)
MACRO_CONTENUTO = (
    "Testo",
    "Risposta",
    "Aiutino",
    "SoluzioneUfficiale",
    "SoluzioniAlternative",
    "Osservazioni",
    "Commenti",
)
ATTESI = {
    "Testo": 78,
    "Risposta": 72,
    "Aiutino": 78,
    "SoluzioneUfficiale": 56,
    "SoluzioniAlternative": 21,
    "Osservazioni": 33,
    "Commenti": 2,
}


def estrai_macro(testo: str, nome: str) -> str | None:
    prefisso = "\\renewcommand{\\" + nome + "}{"
    posizione = testo.find(prefisso)
    if posizione < 0:
        return None
    indice = posizione + len(prefisso)
    inizio = indice
    profondita = 1
    while indice < len(testo):
        carattere = testo[indice]
        if carattere == "\\":
            indice += 2
            continue
        if carattere == "{":
            profondita += 1
        elif carattere == "}":
            profondita -= 1
            if profondita == 0:
                return testo[inizio:indice]
        indice += 1
    raise ValueError(f"Graffe non bilanciate nella macro {nome}")


def ha_contenuto(valore: str | None) -> bool:
    if valore is None:
        return False
    pulito = re.sub(r"(?m)%.*$", "", valore)
    pulito = re.sub(
        r"\\(?:ldots|dots|qquad|quad|par|medskip|smallskip|bigskip)\b",
        "",
        pulito,
    )
    pulito = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^]]*\])?", "", pulito)
    pulito = re.sub(r"[{}\s~.]|\\", "", pulito)
    return bool(pulito)


def attesi() -> list[tuple[int, int]]:
    risultato = []
    for anno in range(1996, 2014):
        massimo = 6 if anno <= 1998 else 4
        risultato.extend((anno, numero) for numero in range(1, massimo + 1))
    return risultato


def main() -> int:
    errori: list[str] = []
    conteggi = Counter()
    conteggi_totali = Counter()
    trovati: set[tuple[int, int]] = set()
    insieme_atteso = set(attesi())

    file = sorted(PROBLEMI.glob("SA_????_*.tex"))

    for percorso in file:
        corrispondenza = re.fullmatch(r"SA_(\d{4})_([1-9]\d*)\.tex", percorso.name)
        if not corrispondenza:
            errori.append(f"Nome non valido: {percorso.name}")
            continue

        anno, numero = map(int, corrispondenza.groups())
        identificatore = (anno, numero)
        if identificatore in trovati:
            errori.append(f"Problema duplicato: {anno}.{numero}")
        trovati.add(identificatore)

        try:
            testo = percorso.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errori.append(f"File non UTF-8: {percorso.name}")
            continue

        if "\r" in testo:
            errori.append(f"Terminatori CR residui: {percorso.name}")

        valori = {}
        for macro in set(MACRO_OBBLIGATORIE) | set(MACRO_CONTENUTO):
            try:
                valori[macro] = estrai_macro(testo, macro)
            except ValueError as errore:
                errori.append(f"{percorso.name}: {errore}")
                valori[macro] = None

        for macro in MACRO_OBBLIGATORIE:
            if valori[macro] is None:
                errori.append(f"{percorso.name}: manca {macro}")

        if valori["Anno"] is not None and valori["Anno"].strip() != str(anno):
            errori.append(f"{percorso.name}: anno interno incoerente")
        if (
            valori["NumeroProblema"] is not None
            and valori["NumeroProblema"].strip() != str(numero)
        ):
            errori.append(f"{percorso.name}: numero interno incoerente")

        if identificatore not in insieme_atteso and not ha_contenuto(valori["Testo"]):
            errori.append(f"{percorso.name}: testo vuoto")

        for macro in MACRO_CONTENUTO:
            if ha_contenuto(valori[macro]):
                conteggi_totali[macro] += 1
                if identificatore in insieme_atteso:
                    conteggi[macro] += 1

    for identificatore in sorted(insieme_atteso - trovati):
        errori.append(f"Problema mancante: {identificatore[0]}.{identificatore[1]}")
    for identificatore in sorted(trovati - insieme_atteso):
        if identificatore[0] < 2014:
            errori.append(f"Anno non ammesso: {identificatore[0]}.{identificatore[1]}")

    for macro, numero_atteso in ATTESI.items():
        if conteggi[macro] != numero_atteso:
            errori.append(
                f"{macro}: attesi {numero_atteso} campi compilati, "
                f"trovati {conteggi[macro]}"
            )

    if errori:
        print("Cantiere NON coerente:")
        for errore in errori:
            print(f"- {errore}")
        return 1

    nuovi = len(trovati - insieme_atteso)
    totale = len(trovati)
    print(f"Cantiere coerente: {totale} problemi canonici (78 storici + {nuovi} nuovi)")
    for macro in MACRO_CONTENUTO:
        print(f"- {macro}: storici {conteggi[macro]}/78; totale {conteggi_totali[macro]}/{totale}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

