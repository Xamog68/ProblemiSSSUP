#!/usr/bin/env python3
"""Porta gli SVG gia compilati in sito/assets/figure senza toccare i LaTeX.

Uso dalla radice di ProblemiSSSUP:
    python3 scripts/installa_figure_svg.py              # solo preflight
    python3 scripts/installa_figure_svg.py --applica     # installa tutti gli SVG

L'inventario e gli SVG devono essere presenti in build/figure-svg, creati
con genera_figure_svg_massivo.py. Se anche UN SOLO file e' mancante, obsoleto,
non vettoriale o in errore, non scrive nulla.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import xml.etree.ElementTree as ET

from genera_figure_svg_massivo import inventory, read_generator

ID_RE = re.compile(r'SA_\d{4}_\d+__[A-Za-z]+__\d{2}\Z')
SVG_NS = 'http://www.w3.org/2000/svg'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def preflight(root: Path, build: Path) -> tuple[list[tuple[Path, Path, dict]], dict]:
    source_index = build / 'inventario.json'
    if not source_index.is_file():
        raise ValueError(f'Inventario non trovato: {source_index}')
    report = json.loads(source_index.read_text(encoding='utf-8'))
    rows = report.get('figures', [])
    if report.get('complete_archive') is not True or report.get('scan_errors'):
        raise ValueError('L\'inventario non copre tutto l\'archivio oppure contiene errori')
    if not rows:
        raise ValueError('Inventario delle figure vuoto')
    gen = read_generator(root)
    expected, scan_errors, _ = inventory(root, gen)
    if scan_errors:
        raise ValueError('Inventario attuale non valido: ' + '; '.join(scan_errors[:3]))
    expected_by_id = {f.ident: f for f in expected}
    seen = set()
    jobs = []
    manifest_rows = []
    issues = []
    for row in rows:
        fid = row.get('id', '')
        if not ID_RE.fullmatch(fid) or fid in seen:
            issues.append(f'Identificativo non valido o duplicato: {fid!r}')
            continue
        seen.add(fid)
        fig = expected_by_id.get(fid)
        if fig is None:
            issues.append(f'Figura non piu presente nei sorgenti: {fid}')
            continue
        if row.get('stato') != 'OK':
            issues.append(f'Conversione non riuscita: {fid} ({row.get("stato")})')
            continue
        if row.get('sha256_sorgente') != fig.source_hash:
            issues.append(f'Sorgente modificato dopo la conversione: {fid}')
            continue
        if row.get('campo') != fig.field or row.get('numero') != fig.index:
            issues.append(f'Campo o numero non corrispondente: {fid}')
            continue
        if row.get('svg') != f'svg/{fid}.svg':
            issues.append(f'Percorso SVG inatteso per {fid}: {row.get("svg")}')
            continue
        infile = build / 'svg' / f'{fid}.svg'
        if not infile.is_file():
            issues.append(f'File SVG mancante: {infile}')
            continue
        raw = infile.read_bytes()
        if len(raw) < 90:
            issues.append(f'File SVG troppo piccolo: {fid}')
            continue
        try:
            root_svg = ET.fromstring(raw)
        except ET.ParseError as exc:
            issues.append(f'SVG XML non valido {fid}: {exc}')
            continue
        if root_svg.tag != '{' + SVG_NS + '}svg':
            issues.append(f'Non e un SVG: {fid}')
            continue
        if any(node.tag == '{' + SVG_NS + '}image' for node in root_svg.iter()):
            issues.append(f'SVG contiene un elemento raster <image>: {fid}')
            continue
        if b'data:image/' in raw:
            issues.append(f'SVG contiene immagini raster incorporate: {fid}')
            continue
        target = root / 'sito' / 'assets' / 'figure' / (fid + '.svg')
        jobs.append((infile, target, {'id': fid, 'campo': fig.field,
                                     'sha256_sorgente': fig.source_hash,
                                     'sha256_svg': sha(raw),
                                     'categoria': fig.category}))
        manifest_rows.append(jobs[-1][2])
    extra = set(expected_by_id) - seen
    if extra:
        issues.append(f'Figure presenti nei sorgenti ma assenti dall\'inventario: {len(extra)}')
    if len(rows) != len(expected):
        issues.append(f'Numero delle figure diverso: {len(rows)} nel catalogo / {len(expected)} nei sorgenti')
    if issues:
        raise ValueError('\n  '.join([f'Preflight fallito ({len(issues)} problemi):'] + issues[:22] +
                                      ([f'... altri {len(issues)-22}'] if len(issues) > 22 else [])))
    manifest = {'schema': 1, 'figures': sorted(manifest_rows, key=lambda d: d['id'])}
    return jobs, manifest


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--applica', action='store_true', help='Copia SVG e scrive il manifesto')
    p.add_argument('--verifica-sito', action='store_true',
                   help='Controlla che i dati web contengano tutti gli SVG')
    p.add_argument('--output', type=Path, default=Path('build/figure-svg'),
                   help='Directory del catalogo SVG prodotto dal generatore')
    args = p.parse_args()
    root = Path.cwd().resolve()
    if not (root / 'contenuti' / 'problemi').is_dir():
        p.error('Eseguire dalla radice del repository ProblemiSSSUP')
    try:
        jobs, manifest = preflight(root, args.output.resolve())
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(f'ERRORE: {exc}', file=sys.stderr)
        return 1
    cnt = Counter(d['categoria'] for _, _, d in jobs)
    size = sum(a.stat().st_size for a, _, _ in jobs)
    print(f'PRE-FLIGHT OK: {len(jobs)} SVG vettoriali / {len(manifest["figures"])} voci, '
          f'{size/1024/1024:.2f} MiB')
    print(f'Classificazione orientativa: {dict(cnt)}')
    if args.verifica_sito:
        if args.applica:
            p.error('--verifica-sito e --applica sono modalita alternative')
        import re
        files = sorted((root / 'sito' / 'dati' / 'problemi').glob('????_*.js'))
        expected = Counter(row['id'] for _, _, row in jobs)
        actual: Counter = Counter()
        unresolved = 0
        missing_other = 0
        for filename in files:
            raw = filename.read_text(encoding='utf-8').strip()
            prefix = 'window.SSSUP.registerProblem('
            if not raw.startswith(prefix) or not raw.endswith(');'):
                raise SystemExit(f'ERRORE: dato web malformato: {filename}')
            data = json.loads(raw[len(prefix):-2])
            for body in data.get('sections', {}).values():
                actual.update(re.findall(
                    r'src="assets/figure/(SA_\d{4}_\d+__[A-Za-z]+__\d{2})\.svg"', body))
            unresolved += data.get('figure_issues', {}).get('pstricks', 0)
            missing_other += len(data.get('figure_issues', {}).get('da_ricostruire', []))
        if actual != expected or unresolved != 0:
            print(f'ERRORE SITO: SVG attesi={sum(expected.values())}, '
                  f'SVG trovati={sum(actual.values())}, PSTricks pendenti={unresolved}', file=sys.stderr)
            for ident in sorted((expected-actual).elements()):
                print('  manca:', ident, file=sys.stderr)
            for ident in sorted((actual-expected).elements()):
                print('  inatteso:', ident, file=sys.stderr)
            return 1
        print(f'VERIFICA SITO OK: {len(files)} problemi, {sum(actual.values())} SVG, '
              f'{unresolved} PSTricks pendenti, {missing_other} figure esterne da ricostruire.')
        return 0
    if not args.applica:
        print('Nessun file modificato. Per installarli: aggiungere --applica.')
        return 0
    folder = root / 'sito' / 'assets' / 'figure'
    folder.mkdir(parents=True, exist_ok=True)
    updated = 0
    for src, dst, row in jobs:
        if not dst.is_file() or sha(dst.read_bytes()) != row['sha256_svg']:
            shutil.copy2(src, dst)
            updated += 1
    manifest_file = folder / 'manifest.json'
    raw = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    tmp = folder / 'manifest.json.tmp'
    tmp.write_bytes(raw)
    tmp.replace(manifest_file)
    print(f'INSTALLATI: {len(jobs)} SVG, {updated} file copiati/aggiornati; '
          f'indice: {manifest_file}')
    print('Prossimo passo: python3 scripts/genera_dati_sito.py --sito sito')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
