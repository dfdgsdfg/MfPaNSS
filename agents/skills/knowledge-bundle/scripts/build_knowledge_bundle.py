#!/usr/bin/env python3
"""Build an upload-ready knowledge pack for Custom GPT / Claude Project / Gemini Gem.

Consolidates this repo's lecture markdown (transcripts + video notes + Anki decks)
into a handful of thematic bundle files that fit each platform's knowledge-file
limit (Gemini Gem ~10, Custom GPT ~20), and assembles paste-ready instruction
text. Everything lands under the repo's gitignored `build/` — fully regenerable
from tracked sources (the repo md, the personas, and the condensed tutor
instruction asset beside this script).

Run:  python3 agents/skills/knowledge-bundle/scripts/build_knowledge_bundle.py
"""
from __future__ import annotations
import glob
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "assets"))


def find_repo_root():
    for base in (os.getcwd(), SCRIPT_DIR):
        p = os.path.abspath(base)
        while True:
            if os.path.isfile(os.path.join(p, "README.md")) and os.path.isdir(os.path.join(p, "01-sets")):
                return p
            parent = os.path.dirname(p)
            if parent == p:
                break
            p = parent
    sys.exit("repo root not found (needs README.md + 01-sets/).")


ROOT = find_repo_root()
OUT = os.path.join(ROOT, "build")
KN = os.path.join(OUT, "knowledge")

# Thematic groups → unit-number prefixes (kept <=10 bundles so it fits a Gemini Gem).
GROUPS = [
    ("00-index-overview", "강의 전체 지도·개요 (README + index)", {"files": ["README.md", "INDEX.md"]}),
    ("01-foundations", "집합·명제·공리 / 대수·군 / 함수 (1–4강)", {"units": ["01", "02", "03", "04"]}),
    ("02-linear-algebra", "선형대수학 1–4 (5–8강)", {"units": ["05", "06", "07", "08"]}),
    ("03-calculus-differentiation", "미분·다변수 미분 (9–10강)", {"units": ["09", "10"]}),
    ("04-calculus-integration", "적분·다변수 FTC: 그래디언트·회전·발산 (11–14강)", {"units": ["11", "12", "13", "14"]}),
    ("05-advanced-geometry-stats", "미분기하·복소해석·통계의 기하 (15–17강)", {"units": ["15", "16", "17"]}),
    ("06-anki-drills", "계산 드릴 Anki 카드 (문제/해답)", {"anki": True}),
]

# Source/disclaimer notice the deployed assistant delivers on the first message.
FIRST_NOTICE = (
    "\n## First-message notice (출처·면책 고지 — 대화 첫 메시지에 1회만)\n"
    "At the very start of the FIRST message of a conversation, before your opening, deliver this notice "
    "once (keep the links), in Korean. Do not repeat it on later turns.\n"
    "> 📌 이 자료는 **수학의 즐거움(Enjoying Math)** 커뮤니티·채널의 \"직장인과 문과생을 위한 수학교실\"을 "
    "AI로 정리한 것입니다 — 유튜브 https://www.youtube.com/@enjoyingmath9346 · 플레이리스트 "
    "https://youtube.com/playlist?list=PL4m4z_pFWq2pHnFFpE25LT4kR6_3jv5CY · 디스코드 https://discord.gg/tRrHCcJQ. "
    "**제작자가 검수하지 않아 수리적 오류나 강의의 의도·맥락과 다른 부분이 있을 수 있으니**, 중요한 내용은 "
    "직접 계산·정의로 확인해 주세요. 모든 권리는 위 커뮤니티와 커뮤니티 지기 \"geonheecho\"에게 있습니다.\n"
    "Then continue naturally with your normal opening.\n"
)


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def clean(text):
    """Drop local-asset references that won't resolve once uploaded; keep the prose,
    LaTeX, Mermaid, and each figure's Korean caption (as a plain note)."""
    out = []
    for ln in text.split("\n"):
        m = re.match(r"\s*!\[(.*?)\]\(<?[^)>]*\.svg>?\)\s*$", ln)
        if m:
            out.append(f"(그림: {m.group(1)})")
            continue
        if re.match(r"\s*> ?(🔧|🧮)", ln):           # interactive/notebook callouts → drop
            continue
        out.append(ln)
    return "\n".join(out)


def unit_files(prefix):
    files = []
    for d in glob.glob(os.path.join(ROOT, f"{prefix}-*/")):
        for f in sorted(glob.glob(os.path.join(d, "*.md"))):
            if "anki" not in os.path.basename(f).lower():
                files.append(f)
    return files


def collect(spec):
    files = []
    for fn in spec.get("files", []):
        p = os.path.join(ROOT, fn)
        if os.path.isfile(p):
            files.append(p)
    for u in spec.get("units", []):
        files += unit_files(u)
    if spec.get("anki"):
        files += sorted(glob.glob(os.path.join(ROOT, "[0-9][0-9]-*", "*anki*.md")))
    seen, uniq = set(), []
    for f in files:
        if f not in seen:
            seen.add(f); uniq.append(f)
    return uniq


def instruction_from_persona(path, drop_sections, header):
    text = read(path)
    body = text[text.index("\n## "):]            # cut title + intro blockquote
    for sec in drop_sections:
        body = re.sub(rf"\n## {re.escape(sec)}.*?(?=\n## |\Z)", "\n", body, flags=re.S)
    return header + body.strip() + "\n"


def main():
    os.makedirs(KN, exist_ok=True)
    manifest = []

    for slug, title, spec in GROUPS:
        files = collect(spec)
        parts = [f"# 지식 번들: {title}\n\n포함 파일 {len(files)}개. 각 블록 머리에 원본 경로가 주석으로 있습니다.\n"]
        for f in files:
            parts.append(f"\n\n<!-- ───────── FILE: {os.path.relpath(f, ROOT)} ───────── -->\n\n" + clean(read(f)).strip())
        outp = os.path.join(KN, f"{slug}.bundle.md")
        with open(outp, "w", encoding="utf-8") as o:
            o.write("\n".join(parts) + "\n")
        manifest.append((f"knowledge/{slug}.bundle.md", len(files), os.path.getsize(outp)))

    # full personas as one knowledge file (the complete spec is always available)
    pp = ["# 페르소나(전체 규격) — 튜터 / 퀴즈마스터\n"]
    for pf in sorted(glob.glob(os.path.join(ROOT, "agents/personas/*.persona.md"))):
        pp.append(f"\n\n<!-- ───────── FILE: {os.path.relpath(pf, ROOT)} ───────── -->\n\n" + read(pf).strip())
    personap = os.path.join(KN, "_personas.bundle.md")
    with open(personap, "w", encoding="utf-8") as o:
        o.write("\n".join(pp) + "\n")
    manifest.append(("knowledge/_personas.bundle.md", 2, os.path.getsize(personap)))

    # tutor instruction = the tracked, hand-authored condensed web version (asset) → copy in
    tutor = read(os.path.join(ASSET_DIR, "instructions-tutor.txt")) + FIRST_NOTICE
    with open(os.path.join(OUT, "instructions-tutor.txt"), "w", encoding="utf-8") as o:
        o.write(tutor)
    # quiz instruction = stripped from the persona
    quiz = instruction_from_persona(
        os.path.join(ROOT, "agents/personas/quiz-master.persona.md"),
        drop_sections=["Per-platform usage"],
        header=('계산 훈련 진행자 — "직장인과 문과생을 위한 수학교실"\n'
                "지식 출처는 업로드된 Anki 덱·노트입니다(저장소·다운로드 언급은 무시). 기본 언어는 한국어.\n"),
    ) + FIRST_NOTICE
    with open(os.path.join(OUT, "instructions-quiz.txt"), "w", encoding="utf-8") as o:
        o.write(quiz)
    tutor_chars, quiz_chars = len(tutor), len(quiz)

    setup = f"""# 세 플랫폼에 올리기 (Custom GPT · Claude Project · Gemini Gem)

이 `build/` 폴더 = 업로드 준비된 한 벌. 세 플랫폼 모두 **① 지침 + ② 지식 파일(`knowledge/*.bundle.md`)** 만 있으면 됩니다. 같은 재료를 세 곳에 동일하게 씁니다.

## 들어 있는 것
- **지식 번들** `knowledge/` — {len(manifest)}개 파일(전사본·영상 정리노트·Anki·페르소나 전체 규격을 주제별로 합본; Gemini Gem 10개 한도에 맞춰 ≤10개):
{chr(10).join(f"  - `{m[0]}`  ({m[1]} files, {m[2]//1024} KB)" for m in manifest)}
- **지침(붙여넣기용)**:
  - `instructions-tutor.txt` — 튜터(현대수학 직관). 웹 UI 압축본, {tutor_chars}자 (Custom GPT 8000자 한도 내).
  - `instructions-quiz.txt` — 퀴즈마스터(계산 훈련). {quiz_chars}자.
  - (튜터의 **전체 규격**은 지식의 `_personas.bundle.md`에 들어 있어 모델이 언제든 참조.)

## A. Custom GPT (ChatGPT) — 지침 8000자·지식 20파일 한도
1. ChatGPT → **GPT 탐색 → 만들기 → 구성(Configure)** 탭.
2. 이름/설명 입력. **Instructions** 에 `instructions-tutor.txt` 전체 붙여넣기(퀴즈 GPT는 `instructions-quiz.txt`).
3. **Knowledge** 에 `knowledge/*.bundle.md` **전부 업로드**(8개, 20파일 한도 내).
4. **Capabilities**: *Code Interpreter & Data Analysis* **켜기**(라이브 계산·플롯).
5. 저장.

## B. Claude Project (claude.ai)
1. **Projects → 새 프로젝트**.
2. **custom instructions** 에 `instructions-tutor.txt`(또는 quiz). (한도 넉넉 — 더 길게 원하면 `agents/personas/math-tutor.persona.md` 전체도 가능.)
3. **Project knowledge** 에 `knowledge/*.bundle.md` 업로드. 끝.

## C. Gemini Gem
1. Gemini → **Gems → 새 Gem**.
2. **Instructions** 에 `instructions-tutor.txt`(또는 quiz).
3. **Knowledge** 에 `knowledge/*.bundle.md` 업로드(**Gem 지식 10파일 한도** — 그래서 ≤10개로 합쳤습니다).
4. 저장.

## 메모
- 각 합본 블록 머리에 `<!-- FILE: 원본경로 -->` 주석으로 출처 추적.
- 시각화 산출물(SVG/HTML/ipynb)은 로컬 파일이라 이 번들엔 **그림이 캡션 텍스트로만** 들어갑니다.
- 재생성: `knowledge-bundle` 스킬 또는 `python3 agents/skills/knowledge-bundle/scripts/build_knowledge_bundle.py`. (`build/`는 gitignored — 추적 소스에서 항상 재생성됨.)
"""
    with open(os.path.join(OUT, "SETUP.md"), "w", encoding="utf-8") as o:
        o.write(setup)

    print(f"repo root: {ROOT}")
    print(f"tutor instruction: {tutor_chars} chars  (GPT 8000: {'OK' if tutor_chars <= 8000 else 'OVER'})")
    print(f"quiz  instruction: {quiz_chars} chars  (GPT 8000: {'OK' if quiz_chars <= 8000 else 'OVER'})")
    print(f"knowledge bundles: {len(manifest)} files (Gemini Gem 10: {'OK' if len(manifest) <= 10 else 'OVER'})")
    for m in manifest:
        print(f"  {m[0]:48s} {m[1]:>3} files  {m[2]//1024:>5} KB")


if __name__ == "__main__":
    main()
