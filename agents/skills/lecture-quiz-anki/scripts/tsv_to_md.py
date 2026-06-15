#!/usr/bin/env python3
"""Anki TSV → 문제/해답 분리 Markdown.

같은 폴더에 `<같은 이름>.md` 를 만든다. 카드 하나가 한 항목이 되고, 형식은:

    ## 문제
    ### 1. <지시문>
    - <문제 식>

    ## 해답
    ### 1. <지시문>
    - <문제 식>
    - <답><br><풀이>

문제를 보며 답은 아래 `## 해답`에서 같은 번호로 찾는다. 태그(3번째 열)는 넣지 않는다.
- Front 를 첫 `<br>` 기준으로 **지시문**(헤딩)과 **문제 식**(불릿)으로 가른다.
  `<br>` 가 없으면(문장형 문제) Front 전체를 헤딩으로 두고 식 불릿은 없다.
- 헤딩 끝의 `.`/`:` 는 떼어 깔끔하게 한다.
- 수식은 Anki MathJax `\\( \\)`/`\\[ \\]` 를 Markdown `$…$`/`$$…$$` 로 바꾼다(델리미터
  안쪽 패딩 공백은 제거 — GitHub 수식 파서가 `$ x $` 형태를 렌더링하지 않음).

사용:  python tsv_to_md.py <deck.tsv> [deck2.tsv ...]
"""
import sys, os, re

_BLOCK = re.compile(r"\\\[(.*?)\\\]")
_INLINE = re.compile(r"\\\((.*?)\\\)")

def conv(s):
    # Anki MathJax \(..\)/\[..\] -> Markdown $..$/$$..$$, trimming the padding
    # spaces just inside the delimiters: GitHub's math parser ignores a `$..$`
    # whose opening `$` is followed by — or closing `$` preceded by — a space,
    # so `\( x \)` must become `$x$`, not `$ x $`.
    s = _BLOCK.sub(lambda m: "$$" + m.group(1).strip() + "$$", s)
    s = _INLINE.sub(lambda m: "$" + m.group(1).strip() + "$", s)
    # fallback for any unbalanced stragglers the paired regexes missed
    s = s.replace(r"\[", "$$").replace(r"\]", "$$")
    s = s.replace(r"\(", "$").replace(r"\)", "$")
    return s.strip()

def split_front(front):
    if "<br>" in front:
        head, rest = front.split("<br>", 1)
        bodies = [conv(b) for b in rest.split("<br>") if b.strip()]
        return conv(head).rstrip(" .:"), bodies
    return conv(front).rstrip(), []

def one(inp):
    lines = open(inp, encoding="utf-8").read().split("\n")
    cards = [l for l in lines if l.strip() and not l.startswith("#")]
    base = os.path.splitext(os.path.basename(inp))[0]
    probs, answs = [], []
    n = 0
    for c in cards:
        p = c.split("\t")
        if len(p) < 2:
            continue
        n += 1
        head, bodies = split_front(p[0])
        ans = conv(p[1])
        qbul = "".join(f"- {b}\n" for b in bodies)
        probs.append(f"### {n}. {head}\n{qbul}".rstrip() + "\n")
        answs.append(f"### {n}. {head}\n{qbul}- {ans}\n")
    md = (f"# {base}\n\n## 문제\n\n" + "\n".join(probs)
          + "\n## 해답\n\n" + "\n".join(answs))
    out = os.path.splitext(inp)[0] + ".md"
    open(out, "w", encoding="utf-8").write(md)
    print(f"{n:3d}문제 -> {out}")

if __name__ == "__main__":
    for f in sys.argv[1:]:
        one(f)
