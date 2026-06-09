---
name: lecture-quiz-anki
description: >-
  Turn the computation/quiz drills a lecturer runs in class into an Anki
  flashcard deck (TSV), with **every answer independently re-computed** (e.g.
  with SymPy) so no wrong answers slip into the cards. The 직장인과 문과생을 위한
  수학교실 4기 lectures, especially, open with rounds of "계산 훈련" drills (근의 공식,
  완전제곱, 인수분해, 행렬식, 고유치/고유벡터, 행렬 곱·거듭제곱 …) where the lecturer poses a
  problem to a participant and confirms the answer. Use this whenever the user
  wants Anki / flashcards / 복습 카드 from a lecture's quizzes or drills, wants to
  turn quiz problems into spaced-repetition cards, or says things like "이 강의
  퀴즈로 anki 만들어줘", "드릴 문제 플래시카드로", "make anki cards from these drill
  problems". Pairs with `lecture-video-fetch`, which provides the transcript.

  Make sure to reach for this skill even when the user just says "anki" or
  "플래시카드" in the context of a lecture/video — that's exactly the case it's for.
---

# Lecture quiz → Anki

Produce one Anki-importable `.tsv` from the drill quizzes in a lecture. One quiz = one card: **Front = the problem (as posed), Back = the correct answer + a short worked step.**

## Input

The cleaned transcript from `lecture-video-fetch`:
- `<id>.transcript_timed.txt` — `[HH:MM:SS]` per line; gives the quiz order and timestamps.
- `<id>.transcript_clean.txt` — plain text; easier to grep.

These drills are usually **spoken** (the lecturer reads a problem, a participant answers, the lecturer confirms) — often with no board on screen — so the transcript is the source. If a unit note (`…-0K-season.md`) exists, skim it for the drill outline.

## Step 1 — Find the checks the lecturer runs (two kinds)

These lectures quiz participants out loud in **two** ways — capture **both**:

- **계산 (computation drill)** — the lecturer poses a problem to *compute* (근의 공식, 완전제곱, 인수분해, 행렬식, 고유치, 고유벡터, 행렬 곱·거듭제곱, 미분/적분 …); a participant works it; it's confirmed ("잘하셨습니다 / 다음 분"). The "계산 훈련" rounds are these.
- **암기 (recall / oral check)** — the lecturer asks a participant to **state a definition, the statement of a theorem, a method/procedure, or an argument from memory** (예: "고유치를 구하는 방법은?", "무지개 정리를 진술해 보세요", "함수의 정의는?", "왜 \(\det(A-\lambda I)=0\) 인가?"). They answer from understanding — a mini oral exam. This is prime spaced-repetition material, so **don't skip it just because nothing is computed.**

Tells for a real check (either kind): a question put to a *specific* person, an attempt, then a confirm/correct. Skip pure discussion, philosophy, anecdotes, and housekeeping. Note which kind each is — you'll tag it `계산` or `암기`.

## Step 2 — Reconstruct each problem from the (garbled) transcript

The Korean auto-caption mangles math badly ("2분의 -2 + 루트", "4분의 17", "산에 2가 들어갑니다"). Use the surrounding dialogue to recover the actual numbers/matrix. A line like "양변을 2로 나누면 x²+2x+1" tells you the original equation was `2x²+4x+2`. If you genuinely can't pin the problem down, drop the card rather than guess.

## Step 3 — Compute every answer yourself (this is the point)

**Do not trust the spoken answer.** Take the Front you reconstructed and compute the answer **independently** — the cleanest way is a quick SymPy check:

```python
import sympy as sp
x = sp.symbols('x')
print(sp.factor(3*x**2 + 6*x + 1 - 0))          # 완전제곱/인수분해 검산
print(sp.solve(2*x**2 + 4*x + 1, x))            # 근의 공식
A = sp.Matrix([[1,0],[2,3]]); print(A.det(), A.eigenvals(), A.eigenvects())
print((sp.Matrix([[1,1],[0,1]]))**3)            # 거듭제곱
```

Why this matters: these are flashcards. A card that says "−8" when the answer is "−2" actively trains the wrong thing. In practice both the auto-caption **and the lecturer** make slips (e.g. a participant's uncorrected guess, or "3(x+1)²−8" for `3x²+6x+1` where it should be `−2`). The transcript is how you find *which problems* were asked; your own computation is how you get *the answers right*. Make the card's worked step internally consistent with its answer.

When the lecturer's stated answer differs from the correct one, put the **correct** answer on the card and add a short note: `※ 영상에서는 −8로 말했으나 계산상 −2`. (Where a verbal answer was a participant's uncorrected guess, just use the correct value.)

For **암기(recall) cards** there's nothing to compute — instead make the Back state the definition / theorem / method **correctly and in standard form**, the way this lecture (and the unit transcript) establishes it. Keep it to the essential recallable content, not a discursive paragraph; cross-check the unit transcript for the precise statement.

## Step 4 — Write the Anki TSV

Anki imports tab-separated files with directive lines on top. Use this shape:

```
#separator:tab
#html:true
#notetype:Basic
#columns:Front	Back	Tags
<Front>	<Back>	<Tags>
```

Card conventions:
- **One quiz per row**, exactly two tabs (Front, Back, Tags). No raw tabs/newlines inside a field.
- **Math in Anki MathJax**: inline `\( … \)`, display `\[ … \]`. Do **not** use `$ … $` — Anki doesn't render it by default.
- **Line breaks inside a field**: `<br>` (that's why `#html:true`).
- **Front** = the check as posed — 계산: instruction + the problem (`다음 2차 방정식의 해를 구하시오.<br>\( 2x^2+4x+1=0 \)`); 암기: the question (`무지개(스펙트럼) 정리를 진술하시오`, `고유치를 구하는 방법을 설명하시오`). **Back** = 계산: answer + 1–3 line worked step; 암기: the correct definition/statement/method.
- **Tags** = space-separated, **exactly these six tokens** so the deck filters cleanly in Anki:
  `MfPaNSS <0K-season-NN> <unit-slug> ko-kr <type> <수식 분야>`
  - `MfPaNSS` — the course (Mathematics for Professionals and Non Stem Students); fixed.
  - `<0K-season-NN>` — cohort + 강 번호, e.g. `04-season-17`.
  - `<unit-slug>` — the unit folder name, e.g. `06-Linalg-2-inverse-determinant`.
  - `ko-kr` — language; fixed.
  - `<type>` — **`계산`** (a computation drill) or **`암기`** (a recall/oral check), so memorization cards can be filtered.
  - `<수식 분야>` — this card's field, in Korean (행렬, 근의공식, 완전제곱, 행렬식, 고유치, 고유벡터, 미분 / 정의, 정리, 방법, 내적 …).
  Examples: `MfPaNSS 04-season-17 06-Linalg-2-inverse-determinant ko-kr 계산 근의공식` · `MfPaNSS 04-season-20 08-Linalg-4-spectral ko-kr 암기 무지개정리`.

## Step 5 — Validate and spot-check

Run the bundled checker, then eyeball a few cards across types:

```bash
python3 "<skill_dir>/scripts/validate_anki_tsv.py" "<out>.tsv"
```

It confirms the directives, that every data row has exactly 3 fields, that math uses `\( … \)` (not `$`), and that `\(`/`\)` are balanced — the usual ways an Anki import breaks. Then read 3–4 cards yourself and re-check their arithmetic; if you find one wrong, assume there are more and re-verify the batch.

## Output location & naming

Name it after the unit and tag it with cohort + 강 번호, alongside that unit's note:
`<NN-unit>/<short title> anki-0K-season-LL.tsv` — where **`0K`** = 기, **`LL`** = 강 번호.
e.g. `06-linalg-2-inverse-determinant/2x2 matrix anki-04-season-17.tsv`.

The `-LL` keeps decks unique when one unit gets drills from several lectures of the same cohort. Find the unit/season the way `lecture-video-fetch` / `lecture-video-notes` do (look the video up in `index.md` / `README.md`; season from the title's "N기"). A `.tsv` whose name ends in `-0K-season-LL` is **not** caught by the `**/*-season/` gitignore (that matches season *folders*). If the source video is **members-only**, keep the deck inside the gitignored `0K-season/<LL>/` folder instead, same as a members-only note.


## Also export a problem/answer Markdown

Besides the `.tsv` (for Anki), produce a plain-Markdown problem set so the deck is readable/printable without Anki — **problems first, answers in a separate `## 해답` section below** (attempt each problem, then scroll down to check), and **no tags**:

```bash
python3 "<skill_dir>/scripts/tsv_to_md.py" "<out>.tsv"   # -> <out>.md beside the tsv
```

Layout — each card becomes a numbered `###` entry in both sections:

```
## 문제
### 1. <지시문>
- <문제 식>

## 해답
### 1. <지시문>
- <문제 식>
- <답><br><풀이>
```

The script splits the Front on its first `<br>` → the **instruction** becomes the `### N.` heading (trailing `.`/`:` trimmed) and the **expression(s)** become bullet(s); a Front with no `<br>` (a full-sentence question) is used as the heading with no expression bullet. The `## 해답` entry repeats the heading + problem bullet, then adds the answer (with its `<br>` worked step) as a final bullet. The tag column is dropped, and math is rewritten from Anki's `\( \)`/`\[ \]` to Markdown `$ … $`/`$$ … $$` so it renders like the rest of the repo. Same gitignore note as the tsv (a `.md` whose name ends `-0K-season-LL` isn't caught by `**/*-season/`).

## Import (tell the user)

Anki → File → Import → pick the `.tsv` → it reads the `#` directives automatically (separator = Tab, note type = Basic, fields Front/Back/Tags). MathJax renders on review.
