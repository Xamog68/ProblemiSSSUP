#!/usr/bin/env python3
"""Verifica in sola lettura il pacchetto AI contro il contenuti.zip ricevuto.

Uso dalla radice del pacchetto estratto:
    python3 scripts/verifica_integrazione_ai.py --originale /percorso/contenuti.zip
Non estrae archivi, non modifica il repository, non richiede librerie aggiuntive.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

MARKER = '\n% Aggiunta redazionale: la soluzione preesistente non viene modificata.\n'
FIELDS = ('Anno', 'NumeroProblema', 'Testo', 'Risposta', 'Aiutino',
          'SoluzioneUfficiale', 'SoluzioniAlternative', 'Osservazioni', 'Commenti')


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def macro(text: str, name: str):
    matches = list(re.finditer(r'\\renewcommand\s*\{\\' + re.escape(name) + r'\}\s*\{', text))
    if not matches:
        return None
    if len(matches) != 1:
        raise ValueError(f'Macro ripetuta: {name}')
    start = i = matches[0].end()
    depth = 1
    while i < len(text):
        if text[i] == '\\':
            i += 2
            continue
        if text[i] == '%':
            pos = text.find('\n', i)
            i = len(text) if pos < 0 else pos + 1
            continue
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return start, i, text[start:i]
        i += 1
    raise ValueError(f'Macro non chiusa: {name}')


def blank(text: str) -> bool:
    text = re.sub(r'(?<!\\)%[^\n]*', '', text)
    text = re.sub(r'\\(?:ldots|dots|quad|qquad|par|medskip|smallskip|bigskip)\b', '', text)
    return not re.sub(r'[{}\s~.]', '', text)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--originale', type=Path, required=True)
    parser.add_argument('--radice', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        meta = json.loads((args.radice / 'dati/integrazioni_ai/20261108.json').read_text(encoding='utf-8'))
        require(digest(args.originale.read_bytes()) == meta['archivi_ingresso']['contenuti.zip'],
                'Lo ZIP originale non coincide con la fotografia ricevuta.')
        count = Counter()
        with ZipFile(args.originale) as archive:
            expected = {row['file'] for row in meta['problemi']}
            actual = {n for n in archive.namelist()
                      if re.fullmatch(r'contenuti/problemi/SA_[0-9]{4}_[1-9][0-9]*\.tex', n)}
            require(actual == expected, 'Elenco dei sorgenti originali inatteso.')
            for row in meta['problemi']:
                rel = PurePosixPath(row['file'])
                require(not rel.is_absolute() and '..' not in rel.parts, 'Percorso non valido.')
                before_bytes = archive.read(row['file'])
                after_bytes = (args.radice / Path(*rel.parts)).read_bytes()
                require(digest(before_bytes) == row['sha256_prima'], f"Hash originale: {rel}")
                require(digest(after_bytes) == row['sha256_dopo'], f"Hash finale: {rel}")
                before = before_bytes.decode('utf-8')
                after = after_bytes.decode('utf-8')
                additions = {x['campo']: x for x in row['aggiunte']}
                require(set(additions) <= {'Risposta', 'Aiutino', 'SoluzioneRedazionale'},
                        f'Campo non consentito: {rel}')
                for field in FIELDS:
                    m0, m1 = macro(before, field), macro(after, field)
                    require((m0 is None) == (m1 is None), f'Presenza macro: {rel}/{field}')
                    if m0 is None:
                        continue
                    if field not in additions or not blank(m0[2]):
                        require(m0[2] == m1[2], f'Campo preesistente alterato: {rel}/{field}')
                    if field in additions:
                        require(blank(m0[2]), f'Campo non vuoto sostituito: {rel}/{field}')
                for field, details in additions.items():
                    m1 = macro(after, field)
                    require(m1 is not None, f'Manca aggiunta: {rel}/{field}')
                    require(digest(m1[2].encode('utf-8')) == details['sha256_contenuto'],
                            f'Hash del campo: {rel}/{field}')
                    require('% SSSUP-BOZZA-AI: ' + field in m1[2],
                            f'Marcatore AI assente: {rel}/{field}')
                    count[field] += 1
                recovered = after
                if 'SoluzioneRedazionale' in additions:
                    require(macro(before, 'SoluzioneRedazionale') is None,
                            f'Soluzione redazionale gia esistente: {rel}')
                    legacy = macro(before, 'SoluzioneUfficiale')
                    require(legacy is not None and blank(legacy[2]),
                            f'Soluzione preesistente non vuota: {rel}')
                    require(after.count(MARKER) == 1, f'Appendice non riconoscibile: {rel}')
                    recovered = recovered[:recovered.index(MARKER)]
                for field in ('Risposta', 'Aiutino'):
                    if field in additions:
                        old = macro(before, field)
                        current = macro(recovered, field)
                        recovered = recovered[:current[0]] + old[2] + recovered[current[1]:]
                require(recovered.encode('utf-8') == before_bytes,
                        f'Modifica fuori dalle aggiunte consentite: {rel}')
                changed = before_bytes != after_bytes
                require(changed == row['modificato'], f'Stato file incoerente: {rel}')
                count['modificati' if changed else 'identici'] += 1
        require(count['modificati'] == 43 and count['identici'] == 53, 'Conteggio file inatteso.')
        require(all(count[k] == v for k, v in meta['conteggi_aggiunte'].items()), 'Conteggio campi inatteso.')
        print('VERIFICA SUPERATA')
        print('96 sorgenti: 43 integrati, 53 identici byte per byte.')
        print('24 Risposta, 18 Aiutino, 40 SoluzioneRedazionale.')
        print('Tutti i campi preesistenti compilati sono identici.')
        print('Nessuna modifica fuori dalle aggiunte autorizzate.')
        print('Questo controllo non certifica la correttezza matematica.')
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('VERIFICA FALLITA:', exc)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
