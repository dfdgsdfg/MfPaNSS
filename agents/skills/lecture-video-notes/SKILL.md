---
name: lecture-video-notes
description: >-
  Write a structured Korean lecture-notes markdown ("정리 노트") from a downloaded
  lecture video — YAML frontmatter + section headings that link to YouTube
  timestamps + a plain summary — written in the lecturer's own first-person voice,
  centered on the actual lecture content, and ALWAYS keeping the questions and
  "생각해볼 점" raised during the lecture. Use this whenever the user wants notes
  from a lecture video, to write up what a lecture taught, or to turn a video +
  transcript + board frames into study notes — e.g. "이 강의 노트로 정리해줘",
  "강의 정리노트 만들어줘", "make notes from this lecture video", "write up this
  lecture". Pairs with `lecture-video-fetch`, which prepares the inputs.
---

# Lecture video notes

Produce one Korean markdown note that lets someone re-study a lecture without re-watching it, with section titles that jump to the right moment in the video.

For **layout/structure**, an example lives at
`07-linalg-3-geometry/02-season/07. Linear Algebra Part 3 - Linear Algebra and Geometry-02-season-07.md`,
and a blank skeleton is in `assets/note_template.md`. Copy the *structure* from these — but for **voice and tone, follow the section below** (the older example notes were written in a third-person tone this skill no longer uses).

## Voice & tone

Write the note **as if the lecturer wrote it up themselves** — first person, their own lesson. This shapes everything:

- **No third-person "강사".** Never write "강사가 ~했다 / 강사가 질문했다 / 강사가 정리해 주었다". The author *is* the lecturer, so just teach: "…를 보겠습니다", "…라고 정의합니다", "여기서 한번 생각해 봅시다".
- **The audience is 여러분 / 참여자.** Address the class as **여러분** or **참여자** — not "수강생/학생" in the third person. When someone in the room asked something, fold it in naturally ("여러분 중 한 분이 물었듯이, …", "한 참여자분의 질문처럼, …") and then answer it in your own voice; don't narrate "수강생이 묻고 강사가 답했다".
- **Plain, even phrasing.** State things matter-of-factly. Hold back on hype and meta-labels — avoid decorating sentences with "핵심은 ~", "놀라운 통찰", "여기서 가장 중요한 것은". If something matters, a clear explanation shows it; you don't need to announce it. (The summary heading is just `## 요약`, not "핵심 요약".)

The point of the restraint: these read as a calm personal write-up, not a hyped recap. Insight should be *demonstrated* by the explanation, not *asserted* with adjectives.

## Inputs

From `lecture-video-fetch` (or already on disk), under the lecture's `<NN-unit>/<0K>-season/<LL>/`:
- the **video file** — read the board directly from it,
- **`<id>.transcript_timed.txt`** (and `_clean.txt`) — spoken flow + timestamps,
- **`frames/`** — periodic board screenshots.

If frames aren't extracted yet, extract them first (the board is the primary source). Also grab the video's metadata (title, id, duration, upload date, `availability`) for the frontmatter.

## The two essentials

These are the whole point of this skill — get them right.

### 1. Follow the lecture's own content and order

The note tracks **what the lecture actually did, in the order it did it**, rebuilt from the board frames (primary) and the transcript (flow). Don't compress it into a tidy textbook abstract, and don't re-summarize some other note. If twenty minutes went into building the rotation matrix from where the basis vectors land, walk through *that* construction — the motivating question, the figure, the intermediate step — not just the final boxed result.

Why: the value here is the path and the intuition, in order. A generic topic summary is available anywhere; the particular framing, examples, and asides are what's worth keeping.

Read frames in order, in batches, and rebuild the sequence of ideas. The handwritten board beats the auto-caption whenever they disagree (Korean math ASR garbles terms badly).

### 2. Always keep the questions and "생각해볼 점"

Every section that had one **must** keep the questions raised in the lecture and the "생각해볼 점" — including the point that got settled after putting a question to 여러분. These are mandatory, not optional flavor.

Why: in a discussion-style lecture the questions *are* the teaching — they're where you want the reader to stop and think. Dropping them keeps the conclusions but loses the lesson.

Use clearly marked callouts, written in your own (lecturer's) voice — no "(강사)/(수강생)" tags:

```
> **💭 생각해볼 점** 여기서 던지는 물음을 1인칭으로. 참여자가 낸 물음이면 "여러분 중 한 분이 물었듯이 …"로 녹이고, 정리까지 담담하게 이어간다.
> **✏️ 연습문제** 이번 시간에 낸 연습/숙제.
> **📚 참고·응용** 강의에서 언급한 응용·참고.
```

Place them at the end of the relevant section. Mine them from the board (look for "질문", "연습문제", "생각해볼", boxed prompts) and the transcript (the question is often spoken before it's written). If a section genuinely had none, that's fine — but look before concluding so.

## Keep the mathematics, drop the housekeeping

A recording is full of things that aren't the lesson: the instructor's **personal life** (a rough morning with the toddler, how they're feeling, off-hand biography) and the **running of the class** — attendance, "post one piece every week", "please speak up like 이동훈 did today", recruitment, book-work logistics, scheduling, greetings and sign-offs, and the gentle scolding about participation. These matter in the room, but a study note is not a session log.

Leave them out. Keep only:
- the **mathematics** — definitions, results, computations, intuitions, the path of ideas;
- the **mathematically substantive exchanges** between the instructor and participants — a participant's math question and the answer, a 생각해볼 점 that is genuinely about the math.

So a 💭 is "왜 \(\det(A-\lambda I)=0\)이어야 하는가" — never "여러분 더 적극적으로 질문하세요". Keep the math of an interaction and drop its social framing, names, and personal context. If a whole section is just housekeeping or personal talk (a chatty intro, an admin stretch, an off-topic story), omit the section rather than summarizing it — then renumber the remaining sections in order.

Why: the reader wants to re-learn the math, not relive the session. Cutting the housekeeping is exactly what makes the note worth more than re-watching the video.

## Verify against *this* video — don't import from elsewhere

Only include questions, points, and applications that are actually in **this specific video**. The same course is re-run across cohorts (기/시즌) and also exists as written notes, and those versions differ. It's tempting to fill a thin section with material from the written notes or another cohort — don't. If it isn't on this video's board or in its transcript, leave it out.

Quick cross-check before committing to a claim that something was covered: grep the transcript for the key term.

```bash
grep -o -E ".{20}<키워드>.{30}" <id>.transcript_clean.txt | head
```

If a term you were about to treat as covered returns nothing (and isn't on the board), drop it — or mark it as your own editorial bridge — rather than writing it as if it happened in this video. Getting this wrong silently mixes cohorts and is the most common way these notes go bad.

## Use the unit's written transcript as a reference (and cite it)

Most lectures have a written transcript of the handwritten notes in the unit folder — the `lecture_note` named in the frontmatter (e.g. `07-linalg-3-geometry/07. Linear Algebra Part 3 - Linear Algebra and Geometry.md`). When one exists, read it and lean on it where it helps:

- **Recover garbled terms and notation.** The auto-caption mangles math vocabulary; the transcript is the canonical written form of the same material, so use it to fix a term, definition, or formula when a board frame is unclear.
- **Sanity-check how a definition/theorem is stated.**
- **Cite it when you use it.** When a definition or statement is drawn from or confirmed against the transcript, attribute it briefly — `(→ 전사본 참조)` or a link `[전사본](<lecture_note 파일명>)` — so the reader can tell it came from the written notes rather than this video.

This does **not** override "verify against this video." The transcript fixes *wording*; it must not pull in **content the video doesn't cover**. The lecture's path, examples, and especially the questions / 생각해볼 점 still come from *this* video. If the written note covers something the video skips, leave it out — or mark it `전사본 보충` rather than writing it as if it happened on camera.

## Output format

Follow `assets/note_template.md`. Key rules:

- **YAML frontmatter** (exactly as in the template): `title` (the **original YouTube video title, verbatim** — e.g. `[직장인과 문과생을 위한 수학교실 2기] 7. 선형대수학과 기하학`), `season` (cohort number, e.g. `2`; 뉴진수/3기 → `3`), `lecture` (the **unit folder slug**, e.g. `07-linalg-3-geometry`), `lecture_note` (that unit's written-transcript `.md` filename), `channel`, `youtube`, `video_id`, `playlist`, `youtube_playlist`, `playlist_id`, `duration`, `recorded`, `uploaded`, `membership` (`true` iff `availability=subscriber_only`).
- **After the frontmatter**: an `# H1` (the lecture title) and a 1–2 sentence plain overview of what this session covers and in what order — in the lecturer's voice, no hype.
- **Section headings are YouTube timestamp links**:
  `## [N. <제목> · ▶ MM:SS](https://www.youtube.com/watch?v=<id>&t=<sec>s)`
  Number sections from 0 (use 0 for the intro). `<sec>` is the start time in seconds (`MM:SS → 60·MM + SS`; for `H:MM:SS` add `3600·H`). Times are approximate (read from the transcript/frames) — but **do not add a "시각 안내" / "타임스탬프는 근사값" / "화면 판서 없음" disclaimer** to the note. Just let the links stand; that housekeeping note is clutter.
- **Body**: plain Korean prose in the lecturer's voice, all math in LaTeX (`$…$`, `$$…$$`). Describe figures in words ("그림: 단위원 위 점 …"). Mark illegible handwriting with `[?]`.
- End with `## 요약` (plain bullets). Do **not** add a personal-use / membership disclaimer line, nor a "함께 만든 파일" file-list section — the overall limitations/disclaimer lives in the repo README, not per-note.

## Visualizations (optional) — rule: `agents/rules/visualization.rule.md`

Default stays "describe figures in words + LaTeX for math." But where a picture genuinely helps, build one per the repo rule. **Artifacts this skill produces are committed with the note** — put them under `<NN-unit>/<0K>-season-assets/<LL>/{svg,html,ipynb}/` (git-tracked; distinct from the gitignored `0K-season/`). The `<LL>/` level groups one lecture's assets (a unit+season can hold several lectures), e.g. `04-season-assets/19/`.

Filenames follow the rule: `<slug>-<0K>-season-<LL>[-<CC>].<ext>` (`<CC>` = the note section it illustrates, 2 digits).

- **Mermaid** — structure/relations/flow → inline ` ```mermaid ` block in the note.
- **SVG (default)** — plots/diagrams → write to `<0K>-season-assets/<LL>/svg/<slug>-<0K>-season-<LL>-<CC>.svg` (keep the generating `.py` beside it, same name), embed with `![설명](<0K>-season-assets/<LL>/svg/…-<CC>.svg)`.
- **HTML** — hands-on/interactive → write to `<0K>-season-assets/<LL>/html/<slug>-<0K>-season-<LL>-<CC>.html`, reference as a **concise link** (never embed; GitHub strips in-`.md` JS). The page self-identifies: `<h1>`=note title+꼬리표, `<h2>`=`<CC>. 챕터 제목`, `<title>`=`<CC>. 챕터 제목-꼬리표`.
- **ipynb (계산 노트)** — numerical/graphs → one **note-level** notebook named like the note `.md` (`<note basename>.ipynb`) in `<0K>-season-assets/<LL>/ipynb/`, with its `.py` jupytext source beside it; section numbers **mirror the note's chapters**. Reference as a **link**.

**Don't narrate plumbing** — no "이 노트의 계산 노트에요", "섹션 번호는 챕터를 따릅니다", "(소스: …생성)", or SVG "생성 스크립트 …py" captions. Just show the artifact. (Full conventions: the rule.)

For a **members-only note** (which lives in the gitignored `0K-season/<LL>/`), put its visuals in that same `0K-season/<LL>/` folder so they stay untracked too.

## Cross-reference links (참조 링크) — standard

When a point in the note should be verifiable/explorable, link its sources in **one line, fixed icons & order**, including only what applies:

`[🧮 계산 §N](<…ipynb>) · [📄 전사본](<NN. <Unit>.md#<anchor>>) · [▶ MM:SS](https://www.youtube.com/watch?v=<id>&t=<sec>s)`

- **🧮 계산 노트** — the companion notebook's matching section (its numbers = the note's chapters), labelled `§N`.
- **📄 전사본** — the unit transcript's matching heading (the transcript is **topic-numbered**, so map by topic, not by the note's chapter number).
- **▶ 영상** — the lecture moment; `&t=<sec>s` (sec = 3600·H + 60·M + S).

**Anchor reality — what actually deep-links on GitHub** (don't ship broken anchors):
- **▶ 영상** `&t=<sec>s` — reliable; the deepest link.
- **📄 전사본 (`.md`)** — GitHub auto heading anchors work; for a stable target add an explicit `<a id="…"></a>` at the heading and link `#…`.
- **🧮 계산 노트 (`.ipynb`)** — GitHub's notebook viewer does **not** guarantee per-cell anchors → link the file + `§N` label (sections are numbered). For a precise jump, put an explicit `<a id="…"></a>` in a markdown cell.

## Filename & location — depends on membership

Name the note `<NN. Unit Title>-0K-season-LL.md` where **`0K`** = cohort/기 and **`LL`** = the lecture's 강 번호 (e.g. `04-season-17` = 4기 17강). The lecture number keeps notes unique when several videos from one cohort land in the same unit. For a sub-series video with no official number (e.g. 뉴진수), use its position in that sub-series; omit `-LL` only if there's truly no index.

**Where it goes depends on `membership`:**

- **Public (`membership: false`)** → unit folder root (tracked in git):
  `<NN-unit>/<NN. Unit Title>-0K-season-LL.md`
  e.g. `06-linalg-2-inverse-determinant/06. Linear Algebra Part 2 - Inverse Matrix and Determinant-04-season-17.md`.
- **Members-only (`membership: true`)** → gitignored `0K-season/<LL>/` folder, so a note on members-only content stays out of version control:
  `<NN-unit>/0K-season/<LL>/<NN. Unit Title>-0K-season-LL.md`
  e.g. `07-linalg-3-geometry/02-season/07/07. Linear Algebra Part 3 - Linear Algebra and Geometry-02-season-07.md`.

Find the unit/season the way `lecture-video-fetch` does — look the video up in the repo's `index.md` / `README.md` (unit + 기), season from the title's "N기". The `0K-season/` folder is gitignored (`**/*-season/`); a `.md`/`.tsv` file whose *name* ends in `-0K-season-LL` is **not** caught by that (it matches season *folders*). If the repo structure isn't present, use a clear descriptive name and tell the user where it landed.

When listing notes/decks in the repo index (`index.md` / `README`), link **only public-video** notes and Anki decks. A members-only note still gets written (into its gitignored `0K-season/<LL>/` folder for personal use), but it is **not** advertised in the tracked index — keep that row's note/deck cell as `—`.


## Quick self-check before handing off

- Written in the lecturer's first-person voice; the class is 여러분/참여자; the word "강사" never appears.
- Plain tone — no "핵심/통찰/놀라운" decoration; the summary heading is `## 요약`.
- Only mathematics and math-relevant exchanges remain — no personal/biographical talk, no class housekeeping (posting cadence, attendance, participation pep-talks, recruitment, scheduling, greetings/sign-offs).
- Sections trace the lecture's real order, not a generic outline.
- Every applicable section keeps its question / 생각해볼 점.
- Everything stated as covered was verified against this video's board or transcript (written-transcript borrowings cited).
- Frontmatter + timestamp links + `## 요약` all present; math renders.
