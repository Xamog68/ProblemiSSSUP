#!/usr/bin/env python3
"""Bonifica puramente tipografica dei sorgenti SA_YYYY_N.tex.

- converte gli accenti TeX in UTF-8, fuori dalla matematica e dai disegni;
- riunisce solo gli a capo di prosa riconosciuti con criteri prudenziali;
- non corregge refusi, non modifica formule e non scrive soluzioni;
- anteprima per impostazione predefinita; --apply per salvare.

Non crea copie di lavorazione: per annullare le modifiche usare Git.
"""

import argparse
import difflib
import re
import unicodedata
from pathlib import Path

ACCENT = {
    '`': '\u0300', "'": '\u0301', '^': '\u0302', '"': '\u0308',
    '~': '\u0303', '.': '\u0307', 'c': '\u0327', 'v': '\u030c',
    'H': '\u030b', 'u': '\u0306', '=': '\u0304',
}
# Gli accenti a comando alfabetico (\c, \v, \H, \u) devono essere
# comandi TeX completi: mai interpretare \centering come \c + e.
# Gli accenti simbolici (\`, \', \^, ecc.) non hanno questa ambiguita'.
ACCENT_RE = re.compile(
    r'''(?<!\\)\\(?:(?P<symbol>[`'\^"~.=])|(?P<word>[cvHu])(?![A-Za-z@]))'''
    r'''[ \t]*(?:\{(?P<braced>\\[ij]|[A-Za-z])\}|(?P<plain>\\[ij]|[A-Za-z]))'''
)
GRAPH_COMMAND = re.compile(
    r'\\(?:begin\{pspicture\*?\}|end\{pspicture\*?\}|'
    r'endpspicture(?![A-Za-z@])|pspicture\*?(?![A-Za-z@]))'
)
DISPLAY_ENV = re.compile(
    r'\\(begin|end)\{(equation\*?|align\*?|alignat\*?|gather\*?|'
    r'multline\*?|flalign\*?|displaymath|math|array|eqnarray\*?|'
    r'aligned|alignedat|gathered|split|cases|matrix|pmatrix|bmatrix|'
    r'Bmatrix|vmatrix|Vmatrix|smallmatrix|tabular\*?|tabularx|longtable|'
    r'figure\*?|table\*?|center|picture|psmatrix|tikzpicture|'
    r'verbatim\*?|lstlisting|minted|alltt)\}'
)
STRUCTURAL = re.compile(
    r'\\(?:begin|end|renewcommand|newcommand|providecommand|'
    r'input|include|label|ref|eqref|psset|pspicture|endpspicture|'
    r'pst[A-Za-z]*|ps[A-Za-z]*|rput|uput|nput|pcline|'
    r'centering|hfill|vfill|bigskip|medskip|smallskip|'
    r'clearpage|newpage|Domanda[A-G]|Titolo\w*|'
    r'par|paragraph|subparagraph|verb)\b'
)
ITEM_WITH_TEXT = re.compile(r'^\\item(?:\[[^\]]*\])?\s+\S')
PREFIX_PROSE_MACRO = re.compile(r'^\\(?:emph|textbf|textit|textsc)\{')


def comment_pos(line: str) -> int:
    for i, c in enumerate(line):
        if c == '%':
            k = i - 1
            while k >= 0 and line[k] == '\\':
                k -= 1
            if (i - 1 - k) % 2 == 0:
                return i
    return len(line)


def unescaped_at(text: str, i: int) -> bool:
    k = i - 1
    while k >= 0 and text[k] == '\\':
        k -= 1
    return (i - 1 - k) % 2 == 0


def convert_accents(prose: str) -> str:
    def sub(m: re.Match) -> str:
        letter = m.group('braced') or m.group('plain')
        if letter == r'\i':
            letter = 'ı'  # punto omesso come nel comando TeX
        if letter == r'\j':
            letter = 'ȷ'
        accent = m.group('symbol') or m.group('word')
        candidate = unicodedata.normalize('NFC', letter + ACCENT[accent])
        # Per alcuni accenti rari l'Unicode precomposto non esiste.
        return candidate if len(candidate) == 1 else m.group(0)
    return ACCENT_RE.sub(sub, prose)


def normalize_once(text: str, do_accents: bool, do_wraps: bool) -> tuple[str, int, int]:
    original_lines = text.splitlines(keepends=True)
    lines = []
    eligible = []
    math = None
    graph_depth = 0
    environments = []
    accents_count = 0

    for raw in original_lines:
        eol = '\r\n' if raw.endswith('\r\n') else ('\n' if raw.endswith('\n') else '')
        line = raw[:-len(eol)] if eol else raw
        cutoff = comment_pos(line)
        code, comment = line[:cutoff], line[cutoff:]

        # I grafici e gli ambienti strutturati sono zone intoccabili.
        graph_hits = list(GRAPH_COMMAND.finditer(code))
        was_graph = graph_depth > 0
        for m in graph_hits:
            closing = m.group().startswith(r'\end')
            graph_depth += -1 if closing else 1
        was_environment = bool(environments)
        for m in DISPLAY_ENV.finditer(code):
            if m.group(1) == 'begin':
                environments.append(m.group(2))
            elif environments and environments[-1] == m.group(2):
                environments.pop()
        protected = was_graph or bool(graph_hits) or was_environment or bool(DISPLAY_ENV.search(code))
        graphics_line = bool(re.match(r'\s*\\(?:ps|pst)[A-Za-z@]*|\s*\\(?:rput|uput|nput|pcline)\b', code))
        outside = not protected and not environments and not graphics_line
        beginning_math = math

        if outside:
            chunks = []
            plain = []
            i = 0
            while i < len(code):
                c = code[i]
                if c == '$' and unescaped_at(code, i):
                    if plain:
                        p = ''.join(plain)
                        q = convert_accents(p) if do_accents and math is None else p
                        accents_count += int(p != q)
                        chunks.append(q)
                        plain = []
                    double = code.startswith('$$', i)
                    delim = '$$' if double else '$'
                    if math is None:
                        math = delim
                    elif math == delim:
                        math = None
                    chunks.append(delim)
                    i += len(delim)
                    continue
                token = code[i:i + 2]
                if token in (r'\(', r'\[', r'\)', r'\]') and unescaped_at(code, i):
                    if plain:
                        p = ''.join(plain)
                        q = convert_accents(p) if do_accents and math is None else p
                        accents_count += int(p != q)
                        chunks.append(q)
                        plain = []
                    if math is None and token in (r'\(', r'\['):
                        math = token
                    elif (math, token) in ((r'\(', r'\)'), (r'\[', r'\]')):
                        math = None
                    chunks.append(token)
                    i += 2
                    continue
                plain.append(c)
                i += 1
            if plain:
                p = ''.join(plain)
                q = convert_accents(p) if do_accents and math is None else p
                accents_count += int(p != q)
                chunks.append(q)
            revised_code = ''.join(chunks)
            if (revised_code != code and not comment
                    and beginning_math is None and math is None):
                revised_code = revised_code.rstrip(' \t')
            line = revised_code + comment

        # 'eligible' e' una condizione strettamente conservativa.
        stripped = line.strip()
        prose_start = (
            stripped and not stripped.startswith('%') and
            (not stripped.startswith('\\') or
             bool(ITEM_WITH_TEXT.match(stripped)) or
             bool(PREFIX_PROSE_MACRO.match(stripped)))
        )
        safe = bool(
            do_wraps and outside and beginning_math is None and math is None
            and not comment and prose_start
            and not STRUCTURAL.search(code)
            and not re.search(r'\\\\|\$\$|\\\[|\\\]', code)
            and not re.search(r'(?<!\\)[{}]\s*$', code)
        )
        # Anche per \item valgono tutte le protezioni di 'safe':
        # non aggiriamo il controllo dei comandi strutturali.
        lines.append((line, eol))
        eligible.append(safe)

    out = []
    joins = 0
    i = 0
    while i < len(lines):
        content, eol = lines[i]
        j = i
        while (do_wraps and j + 1 < len(lines)
               and eligible[j] and eligible[j + 1]
               and not ITEM_WITH_TEXT.match(lines[j + 1][0].strip())
               and lines[j][1] and lines[j + 1][0].strip()):
            # Nessun commento, macro di struttura, matematica multilinea,
            # disegno, o paragrafo vuoto puo' essere attraversato.
            content = content.rstrip() + ' ' + lines[j + 1][0].lstrip()
            eol = lines[j + 1][1]
            j += 1
            joins += 1
        if j > i and eligible[j]:
            content = content.rstrip(' \t')
        out.append(content + eol)
        i = j + 1
    return ''.join(out), accents_count, joins



# Verifiche di integrita': i blocchi matematici e i disegni devono restare identici.
MATH_BLOCK = re.compile(
    r'(?<!\\)\$\$.*?(?<!\\)\$\$|'
    r'(?<!\\)\$(?!\$).*?(?<!\\)\$(?!\$)|'
    r'\\\(.*?\\\)|\\\[.*?\\\]', re.S
)
MATH_ENV_BLOCK = re.compile(
    r'\\begin\{(equation\*?|align\*?|alignat\*?|gather\*?|'
    r'multline\*?|flalign\*?|displaymath|math|eqnarray\*?)\}'
    r'.*?\\end\{\1\}', re.S
)


def drawing_blocks(text: str) -> list[str]:
    depth = 0
    first = None
    blocks = []
    for m in GRAPH_COMMAND.finditer(text):
        if m.group().startswith(r'\end'):
            depth -= 1
            if depth == 0 and first is not None:
                blocks.append(text[first:m.end()])
                first = None
        else:
            if depth == 0:
                first = m.start()
            depth += 1
    return blocks


def normalize(text: str, do_accents: bool, do_wraps: bool) -> tuple[str, int, int]:
    # Ripeti finche' la forma non cambia: alcuni a capo ai confini
    # di una formula multilinea diventano unibili al passaggio successivo.
    current = text
    accents = wraps = 0
    while True:
        revised, na, nw = normalize_once(current, do_accents, do_wraps)
        accents += na
        wraps += nw
        if revised == current:
            break
        current = revised

    if MATH_BLOCK.findall(text) != MATH_BLOCK.findall(current):
        raise ValueError('Bonifica interrotta: una formula inline/display risulta modificata')
    if [m.group() for m in MATH_ENV_BLOCK.finditer(text)] != [m.group() for m in MATH_ENV_BLOCK.finditer(current)]:
        raise ValueError('Bonifica interrotta: un ambiente matematico risulta modificato')
    if drawing_blocks(text) != drawing_blocks(current):
        raise ValueError('Bonifica interrotta: un disegno PSTricks risulta modificato')
    # Qualsiasi comando TeX alfabetico di almeno due lettere e' intoccabile.
    # Questo controllo intercetta anche falsi accenti dentro \centering,
    # \vspace, \usepackage e simili.
    long_commands = re.compile(r'(?<!\\)\\[A-Za-z@]{2,}')
    if long_commands.findall(text) != long_commands.findall(current):
        raise ValueError('Bonifica interrotta: un comando LaTeX e stato modificato')

    # Preserva anche i comandi a una lettera e i comandi simbolici.
    # Sono esclusi soltanto gli accenti TeX ammessi dalla bonifica.
    commands = re.compile(r'(?<!\\)\\(?:[A-Za-z@]+|[^A-Za-z@\s])')
    def command_signature(source: str) -> list[str]:
        return commands.findall(ACCENT_RE.sub('', source))
    if command_signature(text) != command_signature(current):
        raise ValueError('Bonifica interrotta: sequenza di comandi TeX modificata')

    # I commenti non sono materiale da bonificare: restano identici.
    def comments(source: str) -> list[str]:
        return [line[comment_pos(line):]
                for line in source.splitlines()
                if comment_pos(line) < len(line)]
    if comments(text) != comments(current):
        raise ValueError('Bonifica interrotta: un commento e stato modificato')

    # Nessun paragrafo nuovo e nessuna separazione fra paragrafi soppressa.
    def blank_lines(source: str) -> list[str]:
        return [line for line in source.splitlines() if not line.strip()]
    if blank_lines(text) != blank_lines(current):
        raise ValueError('Bonifica interrotta: righe vuote modificate')

    # Idempotenza: il risultato non deve cambiare a una seconda passata.
    again, _, _ = normalize_once(current, do_accents, do_wraps)
    if again != current:
        raise ValueError('Bonifica interrotta: risultato non idempotente')
    return current, accents, wraps

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--sorgenti', type=Path, default=Path('contenuti/problemi'))
    p.add_argument('--anno', type=int)
    p.add_argument('--problema', type=int)
    p.add_argument('--apply', action='store_true', help='scrive solo dopo preflight completo')
    p.add_argument('--diff', action='store_true', help='stampa tutte le differenze')
    p.add_argument('--only-accents', action='store_true')
    p.add_argument('--only-wraps', action='store_true')
    args = p.parse_args()
    if args.only_accents and args.only_wraps:
        p.error('scegliere al massimo una delle due opzioni --only-*')
    sources = sorted(args.sorgenti.glob('SA_????_*.tex'))
    sources = [x for x in sources if re.fullmatch(r'SA_\d{4}_\d+\.tex', x.name)]
    if args.anno is not None:
        sources = [x for x in sources if x.name.startswith(f'SA_{args.anno}_')]
    if args.problema is not None:
        if args.anno is None:
            p.error('--problema richiede --anno')
        sources = [x for x in sources if x.name == f'SA_{args.anno}_{args.problema}.tex']
    if not sources:
        p.error('Nessun sorgente trovato')
    # Preflight completo: non scrivere alcun file prima che tutte le
    # conversioni e tutte le verifiche siano state superate.
    proposals = []
    changes = 0
    accents = wraps = 0
    for path in sources:
        before = path.read_text(encoding='utf-8')
        after, na, nw = normalize(before, not args.only_wraps, not args.only_accents)
        if after == before:
            continue
        changes += 1
        accents += na
        wraps += nw
        print(f'{path.name}: accenti su {na} segmenti, {nw} a capo rimossi')
        if args.diff:
            print(''.join(difflib.unified_diff(
                before.splitlines(keepends=True), after.splitlines(keepends=True),
                fromfile=str(path), tofile=str(path) + ' [proposta]')))
        proposals.append((path, before, after))

    if args.apply:
        # Il contenuto su disco deve ancora coincidere con quello esaminato.
        for path, before, _ in proposals:
            if path.read_text(encoding='utf-8') != before:
                raise RuntimeError(f'File cambiato dopo la verifica: {path}')
        for path, _, after in proposals:
            path.write_text(after, encoding='utf-8')

    print(f'Problemi esaminati: {len(sources)}; da modificare: {changes}; '
          f'segmenti con accenti normalizzati: {accents}; a capo rimossi: {wraps}.')
    print('Modalita:', 'MODIFICHE APPLICATE' if args.apply else 'ANTEPRIMA, NESSUN FILE MODIFICATO')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
