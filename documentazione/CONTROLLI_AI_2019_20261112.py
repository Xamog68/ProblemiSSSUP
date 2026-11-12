#!/usr/bin/env python3
"""Controlli riproducibili delle bozze AI 2019. Solo libreria standard.

Dalla radice del repository:
    python3 documentazione/CONTROLLI_AI_2019_20261112.py
Prima dell'installazione, da un pacchetto estratto altrove:
    python3 /percorso/pacchetto/documentazione/CONTROLLI_AI_2019_20261112.py --verifica-base .

Questi controlli NON sono una certificazione delle dimostrazioni.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import re
import sys

FIELDS = ('Risposta', 'Aiutino', 'SoluzioneRedazionale')
MANIFEST = 'IMPRONTE_AI_2019_20261112.json'


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
        require(digest(raw) == info['draft_sha256'],
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


def probabilities() -> None:
    count = 0
    for den in range(2, 11):
        for num in range(1, den):
            p = F(num, den)
            q = 1-p
            for n in range(8):
                a = p*q**n/(2-p)
                b = q**(n+1)/(2-p)
                # Scomposizione esatta in somma finita e coda geometrica.
                stop = 12
                a_sum = sum(p*p*q**(n+2*j) for j in range(stop))
                a_tail = p*p*q**(n+2*stop)/(1-q*q)
                b_sum = sum(p*q**(n+2*j+1) for j in range(stop))
                b_tail = p*q**(n+2*stop+1)/(1-q*q)
                require(a == a_sum+a_tail, 'Formula (a)')
                require(b == b_sum+b_tail, 'Formula (b)')
                # A prima di B: prima dell'installazione di B oppure
                # entrambi ancora vivi, seguita da vittoria stretta di A.
                a_first = 1-q**n+q**(n+1)/(2-p)
                require(a+b+a_first == 1, 'Partizione degli eventi')
                count += 1
            c = p*p*q**3/(3-3*p+p*p)
            require(c == p**3*q**3/(1-q**3), 'Formula (c)')
            require(c == sum(p**3*q**(3*j+3) for j in range(12))
                    +p**3*q**39/(1-q**3), 'Serie esatta (c)')
    # Per p=0 gli eventi di guasto sono impossibili: non si usa il limite.
    # Per p=1 l'anno di guasto coincide deterministicamente con quello iniziale.
    for n in range(8):
        require(F(0)**n == (1 if n == 0 else 0), 'Caso p=1, punto (a)')
    print('2019.1 OK:', count, 'casi razionali e code geometriche esatte; casi limite documentati.')


def backward_game(limits: tuple[int, ...], top: int) -> list[list[bool]]:
    """Ogni turno appartiene alla squadra opposta rispetto al precedente.

    Il DP usa mosse che non oltrepassano il traguardo. La strategia
    esplicita viene verificata separatamente e non dipende da tale vincolo.
    """
    w = [[False]*(top+1) for _ in limits]
    for r in range(1, top+1):
        for turn, maximum in enumerate(limits):
            w[turn][r] = any(a == r or not w[(turn+1) % len(limits)][r-a]
                            for a in range(1, min(maximum, r)+1))
    return w


def games() -> None:
    for n in range(2, 21):
        w = backward_game((n, n, n, n), 500)
        for r in range(1, 501):
            for turn in range(4):
                require(w[turn][r] == (r % (n+1) != 0), 'Gioco uniforme')
    w = backward_game((15, 10, 5, 10), 1000)
    require(not w[0][500], 'Esito iniziale 500')
    require(all(not w[0][22*k+16] for k in range(45)), 'Posizioni controllate')
    nodes = 0
    for k in range(1, 23):
        r = 22*k+16
        require(r > 15, 'A potrebbe oltrepassare il traguardo')
        for a in range(1, 16):
            b = max(1, 11-a)
            require(1 <= b <= 10, 'Mossa B fuori limite')
            require(11 <= a+b <= 16, 'Somma A+B')
            require(r-a-b > 5, 'C potrebbe oltrepassare il traguardo')
            for c in range(1, 6):
                d = 22-a-b-c
                require(1 <= d <= 10, 'Mossa D fuori limite')
                require(r-a-b-c-d == 22*(k-1)+16, 'Invariante del giro')
                require(a+b+c+d < r, 'Fine anticipata inattesa')
                nodes += 1
    for a in range(1, 16):
        if a >= 6:
            b = 16-a
            require(1 <= b <= 10 and a+b == 16, 'Chiusura B')
        else:
            b = 6-a
            require(1 <= b <= 10 and 16-a-b == 10, 'Chiusura, preparazione')
            for c in range(1, 6):
                d = 10-c
                require(1 <= d <= 10 and a+b+c+d == 16, 'Chiusura D')
    print('2019.2 OK: DP uniforme fino a 500, asimmetrico fino a 1000;',
          nodes, 'risposte avversarie nei giri e tutte le chiusure.')


def polygon_area(points: list[tuple[float, float]]) -> float:
    pairs = zip(points, points[1:]+points[:1])
    return abs(sum(x*v-y*u for (x,y),(u,v) in pairs))/2


def polygon_perimeter(points: list[tuple[float, float]]) -> float:
    return sum(math.hypot(x-u,y-v) for (x,y),(u,v)
               in zip(points, points[1:]+points[:1]))


def geometry() -> None:
    rt3 = math.sqrt(3)
    # Realizzazioni esplicite delle uguaglianze, con lato unitario.
    equilateral = [(0.,0.), (1.,0.), (.5,rt3/2)]
    square = [(0.,0.), (1.,0.), (1.,1.), (0.,1.)]
    hexagon = [(-1.,0.), (-.5,-rt3/2), (.5,-rt3/2),
               (1.,0.), (.5,rt3/2), (-.5,rt3/2)]
    trapezoid = [(-1.,0.), (1.,0.), (.5,rt3/2), (-.5,rt3/2)]
    eqA, eqP = polygon_area(equilateral), polygon_perimeter(equilateral)
    require(math.isclose(eqP**2, 12*rt3*eqA), 'Equilatero')
    sqA, sqP = polygon_area(square), polygon_perimeter(square)
    require(math.isclose(sqP**2, 16*sqA), 'Quadrato, area totale')
    hp, ha, ta = polygon_perimeter(hexagon), polygon_area(hexagon), polygon_area(trapezoid)
    require(math.isclose(ha, 2*ta), 'Aree esagono e trapezio')
    require(math.isclose(hp**2, 8*rt3*ha), 'Esagono, area totale')
    require(math.isclose(hp**2, 16*rt3*ta), 'Esagono, area singolo pezzo')
    # Verifica algebrica indipendente del limite per un quadrilatero di lati
    # a,b,c,d: Brahmagupta <= (a+b+c)^4/48. Non usata come sostituto
    # della dimostrazione poligonale presente nel sorgente.
    count = equal = 0
    for a in range(1, 13):
        for b in range(1, 13):
            for c in range(1, 13):
                for d in range(1, 25):
                    if 2*max(a,b,c,d) >= a+b+c+d:
                        continue
                    s = F(a+b+c+d, 2)
                    area2_bound = (s-a)*(s-b)*(s-c)*(s-d)
                    L = a+b+c
                    require(48*area2_bound <= L**4, 'Limite quadrilatero')
                    is_equal = 48*area2_bound == L**4
                    require(is_equal == (a == b == c and d == 2*a), 'Caso uguaglianza trapezio')
                    count += 1
                    equal += int(is_equal)
    print('2019.3 OK: costanti e configurazioni di uguaglianza;', count,
          'quadruple di lati razionali,', equal, 'casi di uguaglianza.')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verifica-base', type=Path, metavar='REPOSITORY')
    parser.add_argument('--root', type=Path, help='Radice con contenuti/ e documentazione/')
    args = parser.parse_args()
    own_manifest = Path(__file__).resolve().parent/MANIFEST
    manifest = json.loads(own_manifest.read_text(encoding='utf-8'))
    root = args.verifica_base or args.root or Path(__file__).resolve().parents[1]
    check_sources(root, manifest, args.verifica_base is not None)
    if args.verifica_base is None:
        probabilities()
        games()
        geometry()
        print('TUTTI I CONTROLLI SUPERATI. Bozze AI: revisione umana ancora necessaria.')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, ValueError, KeyError) as exc:
        print('ERRORE:', exc, file=sys.stderr)
        raise SystemExit(1)
