# Visualization Rule

Single source of truth for adding figures / diagrams / interactive widgets / numeric notebooks to this repo's lecture material. The `lecture-video-notes` skill and the `math-tutor` · `quiz-master` personas all defer to this file.

**Baseline.** Math is always **LaTeX** (`$…$`) — never a picture of an equation. Figures are described in words by default; add a visualization only where it genuinely builds intuition, not as decoration. Always prefer the **lightest method that works**.

## 1. Decision tree — which method?

```
What are you showing?
│
├─ a structure / relation / flow (group hom, function composition, concept map)
│        → Mermaid   inline ```mermaid fence in the note
│
├─ a static figure / quantitative plot / geometric diagram          ← default
│        → SVG       embed with ![…](…svg); keep the generating .py beside it
│
├─ something the reader should manipulate (drag vectors, sliders)
│        → HTML      self-contained page, linked (never embedded)
│
└─ numbers to compute · matplotlib graphs to (re)generate · experiments to run
         → ipynb     one note-level "계산 컴패니언" notebook, linked
```

If two fit, take the lighter one. The method is never an excuse to skip LaTeX for the math itself.

## 2. Methods at a glance

| method | use for | in the note | renders on |
|---|---|---|---|
| **Mermaid** | structure / relation / flow | inline ` ```mermaid ` fence | GitHub native; degrades to readable text |
| **SVG** (default) | plots / diagrams / figures | `![…](…svg)` embed | everywhere; small vector |
| **HTML** | hands-on / interactive | **link only** (GitHub strips in-`.md` JS/iframe) | local `open` / GitHub Pages |
| **ipynb** | numbers + matplotlib graphs; the note's compute companion | **link only** | GitHub renders code + outputs (incl. plots) |

## 3. Where outputs live & git tracking

Path: `<NN-unit>/<0K>-season-assets/<LL>/{svg,html,ipynb}/<filename>` — the `<LL>/` level groups one lecture's assets (a unit+season can hold several lectures, e.g. `04-season-assets/19/`, `04-season-assets/24/`).

- **Made by the note skill → `…/<0K>-season-assets/` · tracked.** Committed with the note; visible on GitHub.
  - A **members-only** note lives in the gitignored `<0K>-season/<LL>/`; put its assets in that same folder so they stay untracked.
- **Made ad-hoc by a persona (chat/CLI) → `<NN-unit>/<0K>-season/<LL>/` · gitignored.** One-off study output stays out of git.

`.gitignore` already ignores `**/*-season/` (= `0K-season/`) but tracks `0K-season-assets/` — that folder-name difference *is* the "is it versioned?" switch.

## 4. File naming

`<slug>-<0K>-season-<LL>[-<CC>].<ext>`

- `<slug>` = topic (kebab) · `<0K>-season-<LL>` = the **same cohort+lecture tail as the note's `.md`** (e.g. `04-season-19`) · `<CC>` = the **note section (chapter) number** it illustrates, 2 digits.
- **Chapter-scoped** assets (svg, html, a section-specific ipynb) carry `-<CC>`:
  `inner-product-projection-04-season-19-08.svg`, `inner-product-geometry-04-season-19-10.html`.
- **Note-level** asset (the whole-note ipynb companion) drops `-<CC>` and uses the **note's exact basename**:
  `07. Linear Algebra Part 3 - Linear Algebra and Geometry-04-season-19.ipynb`.
- A generating source (`.py`) sits under the **same name, same folder** (`…-19-08.py` → `…-19-08.svg`).

## 5. HTML conventions

- **Self-contained, link-only.** One file; libraries via CDN (Tailwind / Canvas-SVG / KaTeX). Never embed in the `.md` — GitHub strips `<script>`/`<iframe>`. Reference with a concise callout (see §7).
- **The page self-identifies** so it makes sense opened standalone:
  - `<h1>` = **note title + tail** → `<note title>-<NN>강 <0K>기 <LL>강` (e.g. `내적을 토대로 벡터들 관계 규정짓기-07강 4기 19강`)
  - `<h2>` = **chapter** → `<CC>. <chapter title>` (e.g. `10. 내적에서 크기와 각도가 따라 나온다`)
  - `<title>` = `<CC>. <chapter title>-<NN>강 <0K>기 <LL>강`
- **Viewing**: `open …html` locally (or publish via GitHub Pages). GitHub serves raw `.html` as text, so it does not render inline from a repo link.

## 6. ipynb conventions

- **One note-level companion per note** (`계산 노트`), named like the note `.md` (`<note basename>.ipynb`), with its **jupytext `.py` source beside it** (same basename).
- **Section numbers mirror the note's chapters** — include only chapters that have computation, and reuse those exact numbers (notebook `## 10.` ↔ note §10).
- **First cell = the H1 title only** (`# <note title>-<NN>강 <0K>기 <LL>강`). No companion/source/section-mapping preamble.
- **Execute to bake outputs** so GitHub shows results + plots:
  `uv run --with jupytext --with nbconvert --with ipykernel --with numpy --with sympy --with matplotlib jupytext --to ipynb --execute <py> -o <ipynb>`
- **matplotlib text: avoid CJK.** Plot titles/labels in ASCII/English — the default font has no Korean glyphs, so Korean renders as tofu boxes. Korean belongs in markdown cells, not in plotted text.

## 7. Authoring — don't narrate the plumbing

- The artifact speaks for itself: **embed/link it, don't describe its machinery.** Don't write "이 노트의 계산 컴패니언이에요", "섹션 번호는 `.md` 챕터를 따릅니다", "(소스: … → jupytext 생성)", or SVG "생성 스크립트 …py" captions. (Same spirit as the persona's "show it, don't narrate your structure".)
- Keep an interactive callout to one concise line: `> 🔧 [title](<…html>) 에서 직접 ~해 보자.`

## 8. Who makes them

- **`lecture-video-notes` skill** — during video→note, build visuals into `0K-season-assets/` (public) or `0K-season/` (members-only) and reference them from the note.
- **Personas (tutor / quiz), chat-first** — make on demand (or on request), using whatever the platform renders easiest (Claude Artifacts, code-interpreter inline plots, inline Mermaid). When writing a file via local CLI, put it in the gitignored `0K-season/<LL>/`. **If the note already ships a visualization, point the learner to it** instead of rebuilding.

> For linking a point in a note to its sources (notebook / transcript / video), see the **참조 링크 (cross-reference) standard** in `lecture-video-notes/SKILL.md`.
