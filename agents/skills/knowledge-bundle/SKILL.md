---
name: knowledge-bundle
description: >-
  Build an upload-ready knowledge pack for deploying this repo as a **Custom GPT
  (ChatGPT) / Claude Project / Gemini Gem** — it consolidates the lecture
  markdown (전사본·영상 정리노트·Anki) into a few thematic bundle files that fit each
  platform's knowledge-file limit (Gemini Gem ~10, Custom GPT ~20) and assembles
  paste-ready persona instructions + a per-platform SETUP guide, all into the
  gitignored `build/` folder. Use whenever the user wants to turn these notes
  into a Custom GPT / Gem / Claude Project, build or regenerate the knowledge
  bundle / deploy pack, or refresh it after notes change — e.g. "custom gpt로
  만들어줘", "gem 만들기", "지식 번들 빌드", "deploy pack 다시 만들어줘", "build the
  knowledge pack for ChatGPT/Claude/Gemini".
---

# Knowledge bundle (Custom GPT · Claude Project · Gemini Gem deploy pack)

The three consumer UI products — **Custom GPT, Claude Project, Gemini Gem** — have **no creation API**; you build each by hand in its web UI (paste instructions + upload knowledge files). This skill prepares the *materials* so that's a 5-minute manual step on each platform, identical across all three.

## Run it

```bash
python3 agents/skills/knowledge-bundle/scripts/build_knowledge_bundle.py
```

Writes everything to the repo's **gitignored `build/`** (regenerable any time):

- `build/knowledge/*.bundle.md` — the repo's md **consolidated into ≤10 thematic bundles** (so it fits a Gemini Gem's 10-file limit): foundations / linear-algebra / calculus-differentiation / calculus-integration / advanced / anki-drills / index-overview / `_personas`. Each block is headed with a `<!-- FILE: <source path> -->` comment for provenance.
- `build/instructions-tutor.txt` — tutor instruction (condensed **web** version, < the Custom GPT 8000-char limit).
- `build/instructions-quiz.txt` — quiz-master instruction (stripped from the persona).
- `build/SETUP.md` — step-by-step upload guide for each of the three platforms.

Then follow `build/SETUP.md` to upload to ChatGPT / claude.ai / Gemini.

## How it's wired (regenerable from tracked sources)

`build/` is **gitignored** — never commit it; it rebuilds from:

- the repo's lecture `.md` (transcripts, video notes, Anki `.md`),
- `agents/personas/*.persona.md` (the quiz instruction is stripped from its persona; the full personas ship as the `_personas` knowledge bundle),
- **`agents/skills/knowledge-bundle/assets/instructions-tutor.txt`** — the one hand-authored file: the full math-tutor persona is 15.6 KB (> the GPT 8000 limit), so this is a condensed web-oriented version. The script copies it into `build/`. **Edit the tutor instruction here**, not in `build/`.

## Conventions baked in

- **Fit the smallest limit**: ≤10 bundle files (Gemini Gem cap); the script warns if it exceeds 10 files or if either instruction exceeds 8000 chars.
- **Clean for upload**: local-asset references (SVG embeds, 🔧/🧮 interactive·notebook callouts) are dropped from the bundles — figure captions are kept as `(그림: …)`, Mermaid and LaTeX are kept. The interactive HTML/ipynb don't travel as images.
- **One set of materials, three platforms**: the same instructions + bundles go to Custom GPT, Claude Project, and Gemini Gem unchanged.
