#!/usr/bin/env python3
"""Controlli riproducibili delle bozze AI 2020. Solo libreria standard.

Dalla radice del repository:
    python3 documentazione/CONTROLLI_AI_2020_20261112.py
Prima dell'installazione, da un pacchetto estratto altrove:
    python3 /percorso/pacchetto/documentazione/CONTROLLI_AI_2020_20261112.py --verifica-base .

Questi controlli NON sono una certificazione delle dimostrazioni.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from decimal import Decimal, localcontext
import hashlib
import json
import math
from pathlib import Path
import re
import sys

FIELDS = ('Risposta', 'Aiutino', 'SoluzioneRedazionale')
MANIFEST = 'IMPRONTE_AI_2020_20261112.json'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def field_span(text: str, field: str) -> tuple[int, int]:
    pattern = r'\\renewcommand\s*\{\\' + re.escape(field) + r'\}\s*\{'
    matches = list(re.finditer(pattern, text))
    require(len(matches) == 1, 'Macro assente o duplicata: ' + field)
    start = i = matches[0].end()
    depth = 1
    while i < len(text):
        char = text[i]
        if char == '\\':
            i += 2
            continue
        if char == '%':
            newline = text.find('\n', i)
            i = len(text) if newline < 0 else newline + 1
            continue
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                return start, i
        i += 1
    raise RuntimeError('Macro non chiusa: ' + field)


def check_sources(root: Path, manifest: dict, base_only: bool) -> None:
    for rel, info in manifest['files'].items():
        path = root / rel
        require(path.is_file(), 'File non trovato: ' + str(path))
        raw = path.read_bytes()
        if base_only:
            require(digest(raw) == info['base_sha256'],
                    'BASE DIVERSA: ' + rel + '\nInstallazione interrotta: confrontare il file prima di sostituirlo.')
            print('BASE OK:', rel)
            continue
        require(digest(raw) == info['output_sha256'],
                'Bozza modificata rispetto al pacchetto: ' + rel)
        text = raw.decode('utf-8')
        spans = []
        for field in FIELDS:
            a, b = field_span(text, field)
            body = text[a:b]
            require(f'% SSSUP-BOZZA-AI: {field};' in body, 'Marcatore AI mancante: ' + rel + '/' + field)
            require('stato=DA-VERIFICARE' in body and '% SSSUP-PROVENIENZA:' in body,
                    'Provenienza incompleta: ' + rel + '/' + field)
            spans.append((a, b))
        # Ripristinando a vuoto i tre soli campi aggiunti, il sorgente deve
        # essere identico byte per byte alla base: Testo e altri campi inclusi.
        stripped = text
        for a, b in sorted(spans, reverse=True):
            stripped = stripped[:a] + stripped[b:]
        require(digest(stripped.encode('utf-8')) == info['base_sha256'],
                'Modifica esterna ai tre campi consentiti: ' + rel)
        print('INTEGRITA E PROVENIENZA OK:', rel)



def check_tree() -> None:
    for r in (F(1, 4), F(1, 2), F(3, 4)):
        total = r / (1-r)
        partial = sum(r**j for j in range(1, 31))
        require(partial < total, 'Errore nella somma verticale finita')
        require((total >= 1) == (r >= F(1, 2)), 'Soglia della chiusura errata')
        if r == F(1, 2):
            require(partial < 1, 'Il caso critico non deve toccare in tempo finito')
        if r > F(1, 2):
            require(partial > 1, 'Contatto finito non verificato nel caso di prova')
    # Verifica numerica indipendente dell'altezza a profondita finita:
    # programmazione dinamica sulle otto direzioni possibili.
    for rho in (0.2, 0.5, 0.8, 1.0):
        states = {0: 1.0}
        for depth in range(1, 17):
            nxt = {}
            for angle, height in states.items():
                for step in (-1, 1):
                    a = (angle+step) % 8
                    value = height + rho**depth*math.cos(a*math.pi/4)
                    nxt[a] = max(nxt.get(a, -math.inf), value)
            states = nxt
            expected = sum(rho**j*(1 if j%2 == 0 else 1/math.sqrt(2))
                           for j in range(depth+1))
            require(abs(max(states.values())-expected) < 1e-11,
                    'Altezza massima finita non coerente')
    for r in (F(1, 2), F(2, 3), F(9, 10)):
        # I due intervalli -1+rI e 1+rI si sovrappongono.
        require(-1+r/(1-r) >= 1-r/(1-r), 'Espansioni con segni: intervallo vuoto')
    print('ALBERO: soglia, serie geometriche e altezze finite controllate.')


def finite_tree_certificate(x_input: str, y_input: str) -> None:
    with localcontext() as ctx:
        ctx.prec = 65
        x, y = abs(Decimal(x_input)), Decimal(y_input)
        require(x > 0, 'Questa verifica numerica richiede x non nullo')
        y0 = 2*(y/2).to_integral_value(rounding='ROUND_HALF_EVEN')
        require(abs(y-y0) < 1, 'Usare separatamente la griglia per ordinate intere dispari')
        b = int(y0)-1
        q = abs(b)
        k = max(8, (q+2)//2)
        for _ in range(20):
            if Decimal(k*k) > x:
                low = 1-x/Decimal(k*k)
                def abscissa(rho: Decimal) -> Decimal:
                    if rho == 1:
                        return Decimal(0)
                    r = rho*rho
                    return rho*(1-r**k)**2/(1-r)
                if abscissa(low) > x:
                    lo, hi = low, Decimal(1)
                    for _ in range(230):
                        mid = (lo+hi)/2
                        if mid == lo or mid == hi:
                            break
                        if abscissa(mid) > x:
                            lo = mid
                        else:
                            hi = mid
                    rho = (lo+hi)/2
                    r = rho*rho
                    m = (2*k-1-q)//2
                    y_start = (1 + (1 if b>0 else -1)*r*(1-r**q)/(1-r)
                               + r**(q+1)*(1-r**(2*m))/(1+r))
                    length = r**(2*k)
                    if abs(y-y_start) < length:
                        require(abs(abscissa(rho)-x) < Decimal('1e-45'),
                                'Precisione insufficiente nella coordinata orizzontale')
                        return
            k *= 2
        raise RuntimeError('Costruzione numerica non terminata nel limite di verifica')


def check_finite_tree() -> None:
    cases = [('0.1','0.2'), ('0.1','-0.2'), ('0.3','-5.3'), ('2.4','3.3'),
             ('7.2','-9.99'), ('0.25','10.1'), ('-4.3','-4.2'), ('10.5','0.5')]
    for x, y in cases:
        finite_tree_certificate(x, y)
    print('ALBERO (c): 8 costruzioni finite verificate numericamente a 65 cifre.')


def check_polynomials() -> None:
    for n in range(3, 16, 2):
        u = F(1, 4)
        a = n*u**(n-1)
        bound = (n-1)*u**n
        require(0 < a < 1 and 0 < bound < 1, 'Caso di prova non ammissibile')
        for b in (bound/2, bound, 2*bound):
            p_minus = (-u)**n+a*u+b
            p_plus = u**n-a*u+b
            require(p_minus == b+bound and p_plus == b-bound,
                    'Valori critici non corretti')
        power = n/(n-1)
        formula = (n-1)**2/((2*n-1)*n**power)
        # Integrale controllato anche mediante trapezi (test numerico, non prova).
        mesh = 8000
        scale = (n-1)/n**power
        numeric = scale*(0.5+sum((j/mesh)**power for j in range(1, mesh)))/mesh
        require(abs(numeric-formula) < 1e-7, 'Integrazione numerica non coerente')
    require(abs(4/(15*math.sqrt(3))-4/(5*3**1.5)) < 1e-14, 'p3 non coerente')
    print('POLINOMI: valori critici esatti e integrali numerici controllati.')


def staggered(n: int, row_count: int) -> list[tuple[int, int]]:
    # (x,j) rappresenta il punto (x,j*sqrt(3)).
    return [(x,j) for j in range(row_count)
            for x in range(j%2, 2*n+1, 2)]


def min_distance_check(points: list[tuple[int, int]]) -> None:
    for i, (x,j) in enumerate(points):
        for xx,jj in points[:i]:
            require((x-xx)**2+3*(j-jj)**2 >= 4,
                    'Distanza fra studenti inferiore a 2')


def check_classrooms() -> None:
    require(F(2) < 4 and F(32,9) < 4, 'Diametri delle celle non ammissibili')
    for n in range(7, 501):
        require(3*(n+1)**2 <= 4*n*n, 'Altezza delle file eccessiva')
        count = n*(n+2)+(n+3)//2
        require(count > (n+1)**2, 'Non si migliora la griglia quadrata')
    for n in (7,8,9,12,20):
        points = staggered(n,n+2)
        require(len(points) == n*(n+2)+(n+3)//2, 'Conteggio delle file errato')
        min_distance_check(points)
    points = staggered(2,5)
    require(len(points) == 13, 'Configurazione dell aula non da 13 studenti')
    min_distance_check(points)
    require(3*4**2 < 7**2, 'La fascia di 2 metri non e libera')
    require(4*9 == 36 and 4 >= 4, 'Dimensioni aula non ammissibili')
    require(F(196,3) < F(289,4), 'F(4) non e minore di 15')
    require(14 > 9, 'Confronto F(4)>F(9) non verificato')
    print('AULE: configurazioni, distanze e arrotondamenti verificati esattamente.')
    print('ATTENZIONE: non risolti n=3,4,5,6; non risolto se M*=13 oppure 14.')
    print('Il limite 14 usa il teorema esterno di Oler, non dimostrato da questo script.')


def check_editorial_example() -> None:
    meals = (1,3,5,7,9)
    for judge in range(10):
        require(sum(judge <= t <= judge+1 for t in meals) == 1,
                'Controesempio con masse istantanee non valido')
    require(len(meals) == 5, 'Totale del controesempio errato')
    print('CAHIER 2014.1: esempio da 5 kg con atomi ed estremi inclusi verificato.')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verifica-base', type=Path,
                        help='Controlla soltanto i tre sorgenti prima della sostituzione.')
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    manifest = json.loads((here / MANIFEST).read_text(encoding='utf-8'))
    if args.verifica_base is not None:
        check_sources(args.verifica_base.resolve(), manifest, True)
        for source in sorted(here.iterdir()):
            if source.is_file():
                target = args.verifica_base.resolve() / 'documentazione' / source.name
                if target.exists():
                    require(target.is_file() and target.read_bytes() == source.read_bytes(),
                            'DOCUMENTO ESISTENTE DIVERSO: ' + str(target)
                            + '\nFermarsi e integrare le note esistenti prima della copia.')
        print('Le basi coincidono. Nessun file e stato modificato.')
        return 0
    check_sources(here.parent, manifest, False)
    check_tree()
    check_finite_tree()
    check_polynomials()
    check_classrooms()
    check_editorial_example()
    print('CONTROLLI COMPLETATI. Bozze AI da sottoporre a revisione umana.')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, KeyError) as exc:
        print('ERRORE:', exc, file=sys.stderr)
        raise SystemExit(1)
