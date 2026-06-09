# AGENTS.md / CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) — and other agent tools that read AGENTS.md — when working in this repository. (`CLAUDE.md` is a symlink to this file.)

## What this repo is

A **study-material repository, not a software project** — there is no build, lint, or test step. It organizes the lecture series **"직장인과 문과생을 위한 수학교실" (Mathematics for Professionals and Non-STEM Students)** from the *수학의 즐거움 (Enjoying Math)* community, and ships **AI persona/skill prompts** for studying it. The working language for content and learner interaction is **Korean**.

## Layout & content model

17 unit folders `NN-<slug>/` (`01-sets` … `17-statistics`), one per "렉처노트" topic — the canonical map is `README.md` (unit table) and `index.md` (full 100-video index across 4 cohorts + lecture-note × season grid). Each unit folder mixes several artifact types (see `README.md` → 구성):

- `NN. <Title>.md` — **transcript**, OCR'd / reconstructed from the original PDF.
- `NN. <Title>-0K-season-LL.md` — **video note** for cohort `0K` (기), lecture `LL`, written from a YouTube lecture.
- `<topic> anki-0K-season-LL.tsv` (+ a rendered `.md`) — **Anki** drill decks.
- `0K-season/` — gitignored cohort folder: raw video/captions/frames, **members-only notes**, and persona-made ad-hoc visuals.
- `0K-season-assets/` — **tracked** note visualizations (`svg/`, `html/`, `ipynb/`).
- `NN. <Title>.pdf` — gitignored; the source PDF, rebuilt on demand (see Commands).

## AI tooling (the part that needs reading several files)

Lives under `agents/`; `.claude/skills` and `.claude/rules` symlink into it. Two tightly-coupled layers:

- **Personas** `agents/personas/*.persona.md` (`math-tutor`, `quiz-master`) — portable system prompts, the **single source of truth** for voice/behavior, reused verbatim across ChatGPT/Claude/Gemini and the CLI.
- **Skills** `agents/skills/*/SKILL.md` — the Claude Code entry points. Teaching skills **adopt a persona**: `lecture-tutor` → `math-tutor.persona.md`, `lecture-quiz-master` → `quiz-master.persona.md`. Each such `SKILL.md` is a **condensed mirror** of its persona plus Claude-Code specifics.
  - ⇒ **To change teaching/quiz behavior, edit the persona first, then keep the skill's mirror in sync** — they deliberately restate the same rules, so a one-sided edit drifts them apart.

Skill pipeline for turning a lecture into material:
`lecture-video-fetch` (download video + Korean captions + board frames) → `lecture-video-notes` (write the note from those) → `lecture-quiz-anki` (turn drills into an Anki TSV, **every answer independently re-computed**). `lecture-tutor` / `lecture-quiz-master` are the interactive study modes; `lecture-pdf-split` (re)builds the source PDFs.

## Conventions that bite if missed

- **Season-folder split**: `0K-season/` is gitignored (`**/*-season/`); `0K-season-assets/` is intentionally **tracked**. A file whose *name* ends `-0K-season-LL` is **not** a season folder and **is** tracked. (`.gitignore` documents this.)
- **Membership gating**: public-video notes/decks sit at the unit-folder root, are tracked, and are linked in `index.md`/`README.md`; **members-only** ones go in the gitignored `0K-season/` and are **never listed** in the tracked index (leave that cell `—`).
- **PDFs are gitignored** (`*.pdf`). The original 224-page note lives on Google Drive (linked in `README.md`); regenerate per-unit PDFs locally with `lecture-pdf-split`.
- **Visualizations** follow `agents/rules/visualization.rule.md` (imported below): Mermaid / SVG / HTML / ipynb, and which output goes to `0K-season-assets/` (tracked, note skill) vs `0K-season/` (gitignored, persona/CLI).
- **Note voice** (see `lecture-video-notes/SKILL.md`): lecturer's first-person Korean, plain tone (no "핵심/통찰/놀라운"), always keep the lecture's questions / 생각해볼 점, math in LaTeX, no class housekeeping.

## Commands

No build/lint/test. The runnable scripts (paths from repo root):

```bash
# Download the original notes PDF from Drive, split into per-unit PDFs (gitignored output).
uv run --with gdown --with pypdf agents/skills/lecture-pdf-split/scripts/split_lectures.py
uv run agents/skills/lecture-pdf-split/scripts/split_lectures.py --dry-run   # preview, no download/write

# Validate / render an Anki deck.
python3 agents/skills/lecture-quiz-anki/scripts/validate_anki_tsv.py "<deck>.tsv"
python3 agents/skills/lecture-quiz-anki/scripts/tsv_to_md.py "<deck>.tsv"     # -> <deck>.md beside the tsv

# Fetch a lecture video + Korean captions + board frames (see lecture-video-fetch/SKILL.md for the yt-dlp flags).
python3 agents/skills/lecture-video-fetch/scripts/clean_vtt.py "<id>.ko.vtt"
python3 agents/skills/lecture-video-fetch/scripts/extract_frames.py "<video>.mp4" --every 360 --out frames
```

The skills are normally triggered by intent, not the shell — e.g. "1강 가르쳐줘" → `lecture-tutor`, "퀴즈 내줘 / 계산 훈련" → `lecture-quiz-master`, "이 강의 노트로 정리해줘" → `lecture-video-notes`.

## Rules (memory)

When adding figures/diagrams/interactive/numerical artifacts — or when a note skill or persona produces a visualization — follow this rule as the single source of truth (methods + output location + git-tracking):

@agents/rules/visualization.rule.md
