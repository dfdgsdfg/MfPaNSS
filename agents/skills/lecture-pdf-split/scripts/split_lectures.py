#!/usr/bin/env python3
"""Download the original lecture-notes PDF from Google Drive and split it into
per-lecture PDFs — one per unit folder — using the page ranges in README.md.

The README "단원 목록" table is the single source of truth. Each row gives the
unit's document path and its page range in the original (e.g. "p2–14"); this
script swaps `.md`→`.pdf` for the output name and slices those pages out of the
downloaded original. The per-unit PDFs (and the original) are kept out of git
via .gitignore, so this script re-creates them locally on demand.

Run with uv (no global installs needed):
    uv run --with gdown --with pypdf \
        agents/skills/lecture-pdf-split/scripts/split_lectures.py

Useful options:
    --dry-run          parse the README and print the planned splits, then stop
                       (no download, no pypdf needed)
    --pdf PATH         use an already-downloaded original instead of fetching
    --no-download      require an existing original (don't fetch from Drive)
    --force            re-download even if the original is already present
    --page-offset N    shift every README page number by N to reach the physical
                       PDF page (default 0: README "p2" == physical page 2)
    --verify           print the first text snippet of each split's first page
                       so you can confirm the range landed on the right lecture
    --repo-root PATH   repo root (auto-detected from cwd / this skill otherwise)
    --file-id ID       Google Drive file id (defaults to the known original)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DEFAULT_FILE_ID = "1JCb7mX5I5r37BxibXv8_5VKoMwTrhZV_"
DEFAULT_PDF_NAME = "Lecture notes of Mathematics for Professionals and Non Stem Students.pdf"
EXPECTED_TOTAL_PAGES = 224
EXPECTED_UNITS = 17

MD_RE = re.compile(r"\(<(?P<md>[^>]+?\.md)>\)")
PAGE_RE = re.compile(r"p(?P<start>\d+)\s*[–\-]\s*(?P<end>\d+)")  # en-dash or hyphen


def find_repo_root(explicit: str | None) -> Path:
    if explicit:
        root = Path(explicit).resolve()
        if not (root / "README.md").is_file():
            sys.exit(f"--repo-root has no README.md: {root}")
        return root
    seen = []
    for base in (Path.cwd().resolve(), Path(__file__).resolve()):
        seen.append(base)
        seen.extend(base.parents)
    for cand in seen:
        if (cand / "README.md").is_file() and (cand / "01-sets").is_dir():
            return cand
    sys.exit("Could not locate the repo root (needs README.md + 01-sets/). Pass --repo-root.")


def parse_readme(readme: Path):
    """Return [(pdf_rel, start, end, approx)] parsed from the README table."""
    entries = []
    for line in readme.read_text(encoding="utf-8").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        md, pg = MD_RE.search(line), PAGE_RE.search(line)
        if not (md and pg):
            continue
        pdf_rel = md.group("md")[:-3] + ".pdf"  # foo.md -> foo.pdf
        start, end = int(pg.group("start")), int(pg.group("end"))
        approx = line[pg.end():pg.end() + 1] == "*"  # "p159–168*" = approximate range
        entries.append((pdf_rel, start, end, approx))
    return entries


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--repo-root")
    ap.add_argument("--pdf", help="path to an already-downloaded original PDF")
    ap.add_argument("--file-id", default=DEFAULT_FILE_ID)
    ap.add_argument("--no-download", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--page-offset", type=int, default=0)
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    repo = find_repo_root(args.repo_root)
    entries = parse_readme(repo / "README.md")
    if not entries:
        sys.exit("Parsed 0 unit rows from README.md — has the table format changed?")
    if len(entries) != EXPECTED_UNITS:
        print(f"warning: parsed {len(entries)} unit rows (expected {EXPECTED_UNITS})", file=sys.stderr)

    if args.dry_run:
        print(f"repo: {repo}")
        print(f"planned splits ({len(entries)}):")
        for pdf_rel, start, end, approx in entries:
            flag = " (approx)" if approx else ""
            print(f"  p{start:>3}–{end:<3} ({end - start + 1:>2}p){flag}  ->  {pdf_rel}")
        print("dry run: no PDF downloaded or written.")
        return

    # Locate or download the original.
    original = Path(args.pdf).resolve() if args.pdf else (repo / DEFAULT_PDF_NAME)
    if args.pdf:
        if not original.is_file():
            sys.exit(f"--pdf not found: {original}")
    elif original.is_file() and not args.force:
        print(f"original already present: {original}")
    elif args.no_download:
        sys.exit(f"original missing and --no-download set: {original}")
    else:
        import gdown  # noqa: PLC0415

        print(f"downloading original from Google Drive (id={args.file_id}) …")
        gdown.download(id=args.file_id, output=str(original), quiet=False)
        if not original.is_file():
            sys.exit("download failed — try `gdown --fuzzy '<share url>'` manually, then pass --pdf")

    from pypdf import PdfReader, PdfWriter  # noqa: PLC0415

    reader = PdfReader(str(original))
    total = len(reader.pages)
    print(f"original: {original.name}  ({total} pages)")
    if total != EXPECTED_TOTAL_PAGES:
        print(f"warning: expected {EXPECTED_TOTAL_PAGES} pages, got {total} — verify --page-offset", file=sys.stderr)

    made = 0
    for pdf_rel, start, end, approx in entries:
        p0 = start - 1 + args.page_offset  # README page -> 0-indexed physical
        p1 = end + args.page_offset  # exclusive slice end
        if p0 < 0 or p1 > total:
            print(f"  SKIP {pdf_rel}: p{start}–{end} out of range w/ offset {args.page_offset}", file=sys.stderr)
            continue
        writer = PdfWriter()
        for page in reader.pages[p0:p1]:
            writer.add_page(page)
        out = repo / pdf_rel
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "wb") as fh:
            writer.write(fh)
        flag = " (approx range)" if approx else ""
        snippet = ""
        if args.verify:
            try:
                snippet = " | " + " ".join(reader.pages[p0].extract_text().split())[:60]
            except Exception:
                snippet = " | (no extractable text)"
        print(f"  ✓ {pdf_rel}  ← p{start}–{end} ({p1 - p0}p){flag}{snippet}")
        made += 1

    print(f"done: wrote {made}/{len(entries)} per-unit PDFs under {repo}")


if __name__ == "__main__":
    main()
