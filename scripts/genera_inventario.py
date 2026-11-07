#!/usr/bin/env python3
"""Genera l'inventario generale del progetto ProblemiSSSUP.

Solo lettura delle fonti: non estrae ZIP, non modifica i problemi canonici,
non pubblica documenti. Richiede solo Python 3 (libreria standard).

Output (default: fonti-locali/inventari/generale/):
  inventario_problemi.csv  - un record per problema canonico
  inventario_annuale.csv  - anni 1996..anno corrente, inclusi quelli senza fonti
  inventario_fonti.csv    - file locali e voci non vuote degli ZIP
  RIEPILOGO_INVENTARIO.md - sintesi e criteri di interpretazione

I CSV hanno separatore ';' e codifica UTF-8 con BOM per Excel italiano.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from datetime import date
import hashlib
from pathlib import Path, PurePosixPath
import re
import sys
import zipfile

try:
    # Riutilizza ESATTAMENTE la definizione di campo compilato del verificatore.
    from verifica_cantiere import MACRO_CONTENUTO, estrai_macro, ha_contenuto
except ImportError as exc:
    raise SystemExit(
        "Mettere questo script in scripts/ accanto a verifica_cantiere.py"
    ) from exc

ROOT = Path(__file__).resolve().parents[1]
CANONICI = ROOT / "contenuti" / "problemi"
FONTI = ROOT / "fonti-locali"
DEST_DEFAULT = FONTI / "inventari" / "generale"
NOME_CANONICO = re.compile(r"SA_(\d{4})_([1-9]\d*)\.tex\Z")
ANNO_DA_DIR = re.compile(r"(?:^|/)SA_(\d{2})(?:/|\Z)")
ANNO_NOME = re.compile(r"SA_(19\d{2}|20\d{2})_(\d+)\.tex\Z")
PER_ANNI = re.compile(r"(?:^|/)(19\d{2}|20\d{2})(?:/|\Z)")
PRIVATE_TOKENS = ("scheda", "fiscale", "risultati", "student", "candidat", "graduator", "anagrafic", "verbali", "codice_fiscale")
TEXT_SOURCE_SUFFIXES = {".tex", ".pdf", ".docx", ".doc", ".rtf", ".txt"}


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for buf in iter(lambda: f.read(1024 * 1024), b""):
            h.update(buf)
    return h.hexdigest()


def digest_zip_entry(archive: zipfile.ZipFile, entry: zipfile.ZipInfo) -> str:
    h = hashlib.sha256()
    with archive.open(entry) as f:
        for buf in iter(lambda: f.read(1024 * 1024), b""):
            h.update(buf)
    return h.hexdigest()


def is_junk(name: str) -> bool:
    parts = PurePosixPath(name).parts
    return any(x == "__MACOSX" or x == ".DS_Store" or x.startswith("._") for x in parts)


def extract_year(name: str) -> int | None:
    m = ANNO_NOME.search(name)
    if m:
        return int(m.group(1))
    m = PER_ANNI.search(name)
    if m:
        return int(m.group(1))
    m = ANNO_DA_DIR.search(name)
    if m:
        return 2000 + int(m.group(1))
    return None


def category(name: str) -> str:
    low = name.lower().replace("\\", "/")
    suffix = PurePosixPath(name).suffix.lower()
    if any(tok in low for tok in PRIVATE_TOKENS):
        return "amministrativo/riservato"
    if "/test/" in low or "/selexi/" in low or "sa_test" in low:
        if "risposte" in low or "soluzion" in low or "correzion" in low:
            return "test a risposta multipla - risposte/soluzioni"
        return "test a risposta multipla - quesiti/generatori"
    if "soluzion" in low or "correzion" in low or "-risposte" in low or re.search(r"(?:_sol|_soluzioni)\.", low):
        return "soluzioni/correzioni da verificare"
    if suffix in {".png", ".jpg", ".jpeg", ".eps", ".svg"} or PurePosixPath(name).name.lower() in {"squares.pdf", "es1.pdf"}:
        return "figura/grafica"
    if "sa_book" in low or "libro" in low:
        return "libro storico/prodotto"
    if "/scritto/" in low or re.search(r"SA_(?:\d{2}|\d{4}(?:_\d+)?)\.tex\Z", name, re.I) or "testi_chat" in low:
        return "prova scritta/testo da verificare"
    if suffix in {".aux", ".log", ".dvi", ".ps", ".synctex", ".toc"}:
        return "prodotto tecnico di compilazione"
    if suffix == ".zip":
        return "archivio annidato (non esplorato)"
    return "altro/non classificato"


def privacy_flag(name: str) -> str:
    return "VERIFICARE PRIVACY" if any(tok in name.lower() for tok in PRIVATE_TOKENS) else ""


def linked_problem(name: str, category_name: str) -> str:
    # Soltanto il nome esatto di un sorgente individuale costituisce un
    # collegamento attendibile, non una generica parola nel nome del file.
    if category_name.startswith("test a risposta multipla"):
        return ""
    m = ANNO_NOME.search(PurePosixPath(name).name)
    if not m:
        return ""
    return f"{int(m.group(1))}.{int(m.group(2))}"


def inventory_canonical() -> list[dict[str, object]]:
    if not CANONICI.is_dir():
        raise SystemExit(f"Cartella canonica assente: {CANONICI}")
    rows = []
    for path in sorted(CANONICI.glob("SA_*.tex")):
        m = NOME_CANONICO.fullmatch(path.name)
        if not m:
            raise SystemExit(f"Nome sorgente canonico non valido: {path.name}")
        year, num = map(int, m.groups())
        src = path.read_text(encoding="utf-8")
        cols: dict[str, object] = {
            "Anno": year, "Numero": num, "ID": f"{year}.{num}",
            "File canonico": str(path.relative_to(ROOT)),
        }
        for macro in MACRO_CONTENUTO:
            try:
                value = estrai_macro(src, macro)
            except ValueError as e:
                raise SystemExit(f"{path.name}: {e}") from e
            cols[macro] = "presente" if ha_contenuto(value) else ("vuoto" if value is not None else "macro assente")
        cols["Figura da ricostruire"] = "SI" if re.search(r"(?im)^\s*%\s*TODO\s+FIGURA\b", src) else ""
        cols["Nota"] = "Figura da ricostruire in LaTeX" if cols["Figura da ricostruire"] else ""
        rows.append(cols)
    if not rows:
        raise SystemExit("Non ho trovato problemi canonici; nessun inventario generato")
    ids = [r["ID"] for r in rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("Identificatori canonici duplicati")
    return sorted(rows, key=lambda r: (int(r["Anno"]), int(r["Numero"])))


def inventory_sources() -> list[dict[str, object]]:
    result: list[dict[str, object]] = []

    def append(origin: str, internal: str, size: int, sha: str) -> None:
        categ = category(internal)
        year = extract_year(internal)
        result.append({
            "Origine": origin, "Percorso interno": internal,
            "Anno": year if year is not None else "",
            "Categoria provvisoria": categ,
            "Problema identificabile": linked_problem(internal, categ),
            "Estensione": PurePosixPath(internal).suffix.lower(),
            "Byte": size, "SHA-256": sha,
            "Privacy": privacy_flag(internal), "Duplicato SHA-256": "",
        })

    if FONTI.is_dir():
        # Evita di inventariare l'inventario stesso e relativi output.
        for path in sorted(FONTI.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(FONTI)
            if rel.parts[0] == "inventari" or is_junk(rel.as_posix()):
                continue
            # Gli ZIP vengono aperti come fonti, non duplicati come singoli file.
            if path.suffix.lower() == ".zip":
                with zipfile.ZipFile(path) as archive:
                    for entry in archive.infolist():
                        if entry.is_dir() or is_junk(entry.filename):
                            continue
                        append("ZIP: " + str(path.relative_to(ROOT)), entry.filename,
                               entry.file_size, digest_zip_entry(archive, entry))
                continue
            append("File locale: " + str(path.relative_to(ROOT)),
                   str(rel.as_posix()), path.stat().st_size, digest_file(path))

    duplicates = Counter(r["SHA-256"] for r in result if r["SHA-256"])
    for r in result:
        if duplicates[r["SHA-256"]] > 1:
            r["Duplicato SHA-256"] = "SI (contenuto identico)"
    return result


def inventory_years(canon: list[dict[str, object]], sources: list[dict[str, object]]) -> list[dict[str, object]]:
    by_year: dict[int, list[dict[str, object]]] = defaultdict(list)
    for r in canon:
        by_year[int(r["Anno"])].append(r)
    src_year: dict[int, list[dict[str, object]]] = defaultdict(list)
    for s in sources:
        if s["Anno"] != "":
            src_year[int(s["Anno"])].append(s)

    last = max(date.today().year, max(by_year), 2026)
    out = []
    for y in range(1996, last + 1):
        problems = by_year[y]
        fs = src_year[y]
        test_count = sum(str(s["Categoria provvisoria"]).startswith("test a risposta multipla") for s in fs)
        test_ans = sum(s["Categoria provvisoria"] == "test a risposta multipla - risposte/soluzioni" for s in fs)
        written_count = sum(s["Categoria provvisoria"] == "prova scritta/testo da verificare" for s in fs)
        sol_count = sum(s["Categoria provvisoria"] == "soluzioni/correzioni da verificare" for s in fs)
        row: dict[str, object] = {"Anno": y, "Problemi canonici": len(problems)}
        for macro in MACRO_CONTENUTO:
            row[macro + " presenti"] = sum(p[macro] == "presente" for p in problems)
        row["Figure da ricostruire"] = sum(p["Figura da ricostruire"] == "SI" for p in problems)
        row.update({
            "File fonte censiti": len(fs),
            "Fonti scritto candidate": written_count,
            "Fonti test multiple-choice": test_count,
            "Di cui risposte test": test_ans,
            "Fonti soluzioni candidate": sol_count,
            "Fonti con possibile privacy": sum(bool(s["Privacy"]) for s in fs),
        })
        if problems:
            row["Stato prova scritta"] = "testo canonico presente"
        elif written_count:
            row["Stato prova scritta"] = "fonti candidate da esaminare"
        else:
            row["Stato prova scritta"] = "non censita (da cercare)"
        if test_count:
            row["Nota test"] = "test a risposta multipla: inventario distinto"
        else:
            row["Nota test"] = ""
        out.append(row)
    return out


def write_csv(path: Path, rows: list[dict[str, object]], columns: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, delimiter=";", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_summary(path: Path, problems: list[dict[str, object]], annual: list[dict[str, object]], sources: list[dict[str, object]]) -> None:
    pcount = len(problems)
    fields = {k: sum(p[k] == "presente" for p in problems) for k in MACRO_CONTENUTO}
    needs_fig = [p["ID"] for p in problems if p["Figura da ricostruire"] == "SI"]
    zip_origins = sorted({str(s["Origine"]) for s in sources if str(s["Origine"]).startswith("ZIP:")})
    gaps = [str(r["Anno"]) for r in annual if r["Problemi canonici"] == 0]
    table_columns = ["Anno", "Problemi canonici", "Testo presenti", "Risposta presenti", "Aiutino presenti", "SoluzioneUfficiale presenti", "SoluzioniAlternative presenti", "Fonti scritto candidate", "Fonti test multiple-choice"]
    lines = [
        "# Inventario generale ProblemiSSSUP",
        "",
        f"Generato il {date.today().isoformat()} da `scripts/genera_inventario.py`.",
        "",
        "## Contenuti canonici",
        "",
        f"- Problemi canonici: **{pcount}**.",
        *[f"- {k}: **{v}/{pcount}** campi compilati." for k, v in fields.items()],
        f"- Figure da ricostruire segnalate: **{len(needs_fig)}**" + (f" ({', '.join(needs_fig)})" if needs_fig else "") + ".",
        "",
        "## Fonti censite",
        "",
        f"- Voci di fonte (file locali e membri degli ZIP): **{len(sources)}**.",
        f"- File da controllare per privacy, conteggiando anche le copie: **{sum(bool(s['Privacy']) for s in sources)}**.",
        f"- ZIP analizzati senza estrazione: **{len(zip_origins)}**.",
        *[f"  - `{z[5:]}`" for z in zip_origins],
        "",
        "## Quadro annuale (estratto)", "",
        "| " + " | ".join(table_columns) + " |",
        "|" + "|".join(["---:"] * len(table_columns)) + "|",
    ]
    for r in annual:
        vals = [str(r[col]) for col in table_columns]
        lines.append("| " + " | ".join(vals) + " |")
    lines += [
        "",
        "## Anni senza problemi canonici",
        "",
        ", ".join(gaps) if gaps else "Nessuno.",
        "",
        "## Come leggere l'inventario",
        "",
        "- **presente** nelle colonne dei problemi significa che la macro canonica ha contenuto non vuoto, secondo le stesse regole del verificatore.",
        "- **vuoto** significa macro presente ma senza contenuto; non dimostra che il materiale manchi in assoluto.",
        "- **Fonte candidata** significa soltanto che un file esiste; non attesta contenuto, autore, ufficialita, correttezza o corrispondenza al singolo problema.",
        "- Le fonti con classificazione 'test a risposta multipla' non colmano l'assenza di prove scritte.",
        "- Il segnale 'Duplicato SHA-256' riguarda solo l'identita dei byte, non le versioni equivalenti o i testi matematicamente uguali.",
        "- I contenuti degli ZIP annidati non sono esplorati. I metadati macOS e i file di inventario preesistenti sono esclusi.",
        "- Possibili documenti personali o amministrativi restano **solo in locale**. Non pubblicare questo catalogo senza verifica della privacy.",
        "",
        "## Prossimi controlli manuali",
        "",
        "1. Confrontare i 18 nuovi testi canonici con le fonti originali.",
        "2. Esaminare per ciascun problema le soluzioni eventualmente presenti tra i file locali, senza attribuirle automaticamente.",
        "3. Recuperare le prove scritte 2014-2020, separandole dai test di maggio e settembre.",
        "4. Ricostruire in LaTeX le figure segnalate, senza importare figure esterne nei sorgenti canonici.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEST_DEFAULT,
                        help="Cartella di output (default: fonti-locali/inventari/generale)")
    args = parser.parse_args()
    out = args.output if args.output.is_absolute() else (ROOT / args.output)
    canon = inventory_canonical()
    src = inventory_sources()
    exact_sources: dict[str, list[str]] = defaultdict(list)
    for item in src:
        if item["Problema identificabile"]:
            exact_sources[str(item["Problema identificabile"])].append(
                f"{item['Origine']} :: {item['Percorso interno']}"
            )
    for problem in canon:
        matches = exact_sources[str(problem["ID"])]
        problem["Fonti con nome esatto (candidate)"] = len(matches)
        problem["Percorsi fonti con nome esatto"] = " | ".join(matches)
    yearly = inventory_years(canon, src)
    out.mkdir(parents=True, exist_ok=True)
    ccols = ["Anno", "Numero", "ID", "File canonico", *MACRO_CONTENUTO,
             "Figura da ricostruire", "Fonti con nome esatto (candidate)",
             "Percorsi fonti con nome esatto", "Nota"]
    scols = ["Origine", "Percorso interno", "Anno", "Categoria provvisoria", "Problema identificabile", "Estensione", "Byte", "SHA-256", "Privacy", "Duplicato SHA-256"]
    ycols = list(yearly[0].keys())
    write_csv(out / "inventario_problemi.csv", canon, ccols)
    write_csv(out / "inventario_fonti.csv", src, scols)
    write_csv(out / "inventario_annuale.csv", yearly, ycols)
    write_summary(out / "RIEPILOGO_INVENTARIO.md", canon, yearly, src)
    print(f"Problemi canonici: {len(canon)}")
    print(f"Fonti censite: {len(src)}")
    print(f"Anni nel riepilogo: {yearly[0]['Anno']}-{yearly[-1]['Anno']}")
    for p in sorted(out.iterdir()):
        print("Creato:", p.relative_to(ROOT) if p.is_relative_to(ROOT) else p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
