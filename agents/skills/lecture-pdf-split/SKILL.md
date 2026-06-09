---
name: lecture-pdf-split
description: >-
  Download the original "직장인과 문과생을 위한 수학교실" lecture-notes PDF from
  Google Drive and split it into per-lecture PDFs (one per unit folder), using
  the page ranges in README.md. The repo keeps these PDFs out of git
  (.gitignore: `*.pdf`), so this skill re-creates them locally on demand. Use
  whenever the user wants to fetch/restore the original note PDF, regenerate the
  per-lecture (강의별) split PDFs, or says things like "원본 노트 pdf 받아서
  강의별로 쪼개줘", "pdf 다시 받아줘", "단원별 pdf 만들어줘", "download and split the
  lecture notes pdf". Pairs with the README "단원 목록" table, which is the
  source of truth for each unit's page range.
---

# Lecture PDF split (원본 노트 다운로드 + 강의별 분할)

The original lecture notes — a single ~94 MB PDF (224 pages) authored by
"geonheecho" — are **not committed** to this repo. The README links to the
original on Google Drive and lists each unit's page range; this skill turns that
link + table back into the per-unit PDFs (`NN-*/NN. ….pdf`) on the local disk,
where `.gitignore` keeps them untracked.

The README **단원 목록** table is the single source of truth: each row's document
link gives the output name (`.md` → `.pdf`) and its page range gives the slice.
The splitter parses the table, so if a range or filename changes there, this
skill follows automatically — don't hardcode ranges elsewhere.

## Prerequisites

- **`uv`** (preferred) — runs the script with ephemeral deps, no global installs:
  `gdown` (Google Drive download, handles the large-file confirm token) and
  `pypdf` (page slicing). If only `pip` is available, `pip install gdown pypdf`
  and run with `python3` instead.

## Run it

From the repo root:

```bash
uv run --with gdown --with pypdf \
  agents/skills/lecture-pdf-split/scripts/split_lectures.py
```

This downloads the original to `Lecture notes of Mathematics for Professionals and Non Stem Students.pdf`
(repo root, gitignored) if it isn't already there, then writes the 17 per-unit
PDFs into their folders. Re-running is cheap: it reuses an already-downloaded
original unless you pass `--force`.

Preview without touching anything first if you like:

```bash
# parse the README and print the planned splits — no download, no write
uv run agents/skills/lecture-pdf-split/scripts/split_lectures.py --dry-run
```

## Key options

- `--dry-run` — show the planned splits (unit → page range) and stop.
- `--pdf PATH` — use an original you already have instead of downloading.
- `--no-download` / `--force` — require an existing original / re-download it.
- `--verify` — print the first text snippet of each split's first page, so you
  can confirm the range landed on the right lecture (the original is typeset, so
  text usually extracts cleanly).
- `--page-offset N` — shift every README page number by N to reach the physical
  PDF page. Default `0` assumes README "p2" == the PDF's 2nd page (page 1 is the
  cover). If a spot-check is off by a constant, set the offset and re-run.

## Verify after splitting

The script reports `original: … (N pages)` and warns if N ≠ 224 (a sign the
offset/ranges need a look). Spot-check a couple of units with `--verify`, or open
one split PDF and confirm its first page is that lecture's title. Units 12–14 use
**approximate** ranges in the README (marked `*`) — double-check those boundaries
if they matter.

## Notes & gotchas

- Page ranges are **1-indexed and inclusive** as written in the README; the
  script converts to physical PDF pages internally.
- If `gdown` fails on the Drive confirm/virus-scan interstitial, run
  `gdown --fuzzy 'https://drive.google.com/file/d/1JCb7mX5I5r37BxibXv8_5VKoMwTrhZV_/view'`
  manually, then pass the result via `--pdf`.
- These PDFs are the community's original material — they stay **local and
  untracked** (`.gitignore`). Don't commit or redistribute them; the repo ships
  only the link.
