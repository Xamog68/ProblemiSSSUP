#!/usr/bin/env python3
"""Controlli riproducibili delle bozze AI 2018 (non certificazione delle prove).
Eseguire dalla radice del repository:
    python3 documentazione/CONTROLLI_AI_2018_20261112.py
Richiede soltanto Python 3 e la libreria standard.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import math
import re

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(__file__).with_name('IMPRONTE_AI_2018_20261112.json')
FIELDS = ('Risposta', 'Aiutino', 'SoluzioneRedazionale')


def empty_field(text: str, name: str) -> str:
    match = re.search(r'\\renewcommand\{\\' + re.escape(name) + r'\}\{', text)
    if match is None:
        raise ValueError('Campo mancante: ' + name)
    start = i = match.end()
    depth = 1
    while i < len(text):
        ch = text[i]
        if ch == '\\':
            i += 2
            continue
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return text[:start] + text[i:]
        i += 1
    raise ValueError('Campo non chiuso: ' + name)


def source_checks() -> None:
    for entry in json.loads(MANIFEST.read_text(encoding='utf-8')):
        path = ROOT / entry['file']
        data = path.read_bytes()
        assert sha256(data).hexdigest() == entry['sha256_dopo'], path
        recovered = data.decode('utf-8')
        for name in FIELDS:
            assert recovered.count('% SSSUP-BOZZA-AI: ' + name + ';') == 1
            recovered = empty_field(recovered, name)
        assert sha256(recovered.encode('utf-8')).hexdigest() == entry['sha256_prima'], path
    print('OK: tre sorgenti; fuori dai tre campi aggiunti nessun byte modificato.')


def sum_notes(n: int, d: int) -> int:
    q, r = divmod(n, d)
    return n*(n+1)//2 - (d-1)*(d*q*(q-1)//2 + q*(r+1))


def notes_checks() -> None:
    count = 0
    for n in range(2, 251):
        for d in range(2, n+1):
            direct = sum(s//d + s%d for s in range(1, n+1))
            assert direct == sum_notes(n, d), (n, d)
            count += 1
    scores = {d: sum_notes(100, d) for d in range(2, 101)}
    best = min(scores.values())
    assert best == 910
    assert [d for d, value in scores.items() if value == best] == [10, 11]
    assert min(scores[d] for d in range(2, 6)) >= 1010
    assert min(scores[d] for d in range(21, 101)) >= 950
    print('OK: banconote,', count, 'confronti esatti formula/somma; ottimi 10 e 11.')


def times(n: int, phases: list[F], periods: int = 40) -> list[F]:
    assert len(phases) == n and all(0 < x <= 1 for x in phases)
    return sorted(F(t) + phase for t in range(periods) for phase in phases)


def licence_checks() -> None:
    checks = 0
    for n in range(1, 61):
        d = 19*n - 18
        necessary = (19*(n-1))//n + 1
        sufficient = d//n
        assert necessary == 20 - math.ceil(F(19, n))
        assert sufficient == 19 - math.ceil(F(18, n))
        assert n*necessary > 19*(n-1)
        phase_sets = [
            [F(1)]*n,
            [F(i+1, n) for i in range(n)],
            [F((i*i+7*i+3) % 101 + 1, 102) for i in range(n)],
        ]
        for phases in phase_sets:
            ts = times(n, phases)
            assert all(ts[j+n] == ts[j]+1 for j in range(len(ts)-n))
            for driver in range(n):
                last = 19*(driver+1)-1
                gap = ts[last+d]-ts[last]
                assert gap >= sufficient, (n, driver, gap)
                if phases == phase_sets[1]:
                    assert gap == F(d, n)
                checks += 1
    assert (19*2-18)//2 == 10
    n = 19
    ts = times(n, [F(1)]*n)
    for driver in range(n):
        last = 19*(driver+1)-1
        assert ts[last+19*n-18]-ts[last] == 19
    assert F(343, 19) < F(37, 2) < 19
    print('OK: patente,', checks, 'intervalli di riposo esatti e controesempio n=19.')


def grid(widths: list[F], heights: list[F], side: F) -> Counter:
    assert sum(widths) == 600 and sum(heights) == 600
    parts: Counter = Counter()
    for i, w in enumerate(widths):
        for j, h in enumerate(heights):
            parts[tuple(sorted((w, h)))] += 1
            if w != side or h != side:
                assert i in (0, len(widths)-1) or j in (0, len(heights)-1)
    assert sum(a*b*count for (a, b), count in parts.items()) == 360000
    return parts


def tiles_checks() -> None:
    nine, variant = F(9), F(19, 2)
    assert math.ceil(F(360000)/nine**2) == 4445
    assert math.ceil(F(360000)/variant**2) == 3989
    a = grid([nine]*66+[F(6)], [nine]*66+[F(6)], nine)
    assert a == Counter({(F(9), F(9)): 4356, (F(6), F(9)): 132, (F(6), F(6)): 1})
    b = grid([F(3)]+[nine]*66+[F(3)], [nine]*66+[F(6)], nine)
    assert b == Counter({(F(9), F(9)): 4356, (F(3), F(9)): 132,
                         (F(6), F(9)): 66, (F(3), F(6)): 2})
    c = grid([F(3)]+[nine]*66+[F(3)], [F(3)]+[nine]*66+[F(3)], nine)
    assert c == Counter({(F(9), F(9)): 4356, (F(3), F(9)): 264, (F(3), F(3)): 4})
    v = grid([variant]*63+[F(3, 2)], [variant]*63+[F(3, 2)], variant)
    assert v == Counter({(variant, variant): 3969, (F(3, 2), variant): 126,
                         (F(3, 2), F(3, 2)): 1})
    assert (4356+132+1, 132+2) == (4489, 134)
    assert (4356+44+66+1, 44*2+66+3) == (4467, 157)
    assert (4356+88+1, 88*2+5) == (4445, 181)
    assert (3969+21+1, 21*6+2) == (3991, 128)
    assert 88*3 == 264 and 44*3 == 132 and 21*6 == 126
    assert 6*F(3, 2)+F(1, 2) == variant
    print('OK: mattonelle, quattro griglie, aree, pezzi, acquisti e conteggi dei tagli.')

    # Coefficients of k1 and k3 in the expected cost for m consecutive successful cuts.
    for p in [F(99, 100), F(1)]:
        coeff = {}
        for m in (1, 2, 3, 5):
            tile = 1/p**m
            cuts = sum(p**j for j in range(m))/p**m
            assert tile == 1 + (1-p**m)*tile
            assert cuts == sum(p**j for j in range(m)) + (1-p**m)*cuts
            coeff[m] = (tile, cuts)
        plans = [({1: 132, 2: 1}, (4489, 134)),
                 ({1: 66, 2: 44, 3: 1}, (4467, 157)),
                 ({2: 88, 5: 1}, (4445, 181))]
        for groups, deterministic in plans:
            result = (4356+sum(count*coeff[m][0] for m, count in groups.items()),
                      sum(count*coeff[m][1] for m, count in groups.items()))
            if p == 1:
                assert result == deterministic
    print('OK: attese esatte, identita di rinnovo e limite senza rotture.')


def main() -> None:
    source_checks()
    notes_checks()
    licence_checks()
    tiles_checks()
    print('Tutti i controlli superati. Le prove matematiche restano da revisionare.')


if __name__ == '__main__':
    main()
