#!/usr/bin/env python3
"""YouTube 자동자막(VTT) → 깨끗한 텍스트.

YouTube 자동자막은 각 cue가 앞 줄을 반복하며 단어별 인라인 타임스탬프(<00:..><c>..</c>)를
붙이는 '롤링' 형식이라 그대로 읽으면 중복투성이다. 이 스크립트는 인라인 타임스탬프가 있는
줄만 골라 태그를 제거하고 연속 중복을 합쳐, 사람이 읽을 수 있는 평문과 타임스탬프본을 만든다.

사용:  python clean_vtt.py <input.ko.vtt> [out_prefix]
기본 출력:  <id>.transcript_clean.txt  (평문, 한 덩어리)
            <id>.transcript_timed.txt  ([HH:MM:SS] 세그먼트별)
  - out_prefix를 생략하면 입력 파일명 <id>.ko.vtt 에서 <id>를 따와
    입력과 같은 폴더에 <id>.transcript_*.txt 로 저장한다(같은 폴더에 여러 영상이 있어도 안 섞임).
  - out_prefix를 주면 <out_prefix>_clean.txt / <out_prefix>_timed.txt 로 저장.
"""
import re, sys, os

inp = sys.argv[1]
if len(sys.argv) > 2:
    prefix = sys.argv[2]
else:
    base = re.sub(r"\.(ko\.)?vtt$", "", os.path.basename(inp))
    prefix = os.path.join(os.path.dirname(inp), f"{base}.transcript")

segs, times, block_time = [], [], None
for line in open(inp, encoding="utf-8"):
    line = line.rstrip("\n")
    m = re.match(r"^(\d\d:\d\d:\d\d)\.\d+ -->", line)
    if m:
        block_time = m.group(1)
        continue
    if "<c>" in line or re.search(r"<\d\d:\d\d:\d\d", line):
        txt = re.sub(r"<[^>]+>", "", line).strip()
        if txt:
            segs.append(txt)
            times.append(block_time)

clean, ts, prev = [], [], None
for t, tm in zip(segs, times):
    if t != prev:
        clean.append(t)
        ts.append(tm)
        prev = t

full = re.sub(r"\s+", " ", " ".join(clean)).strip()
open(f"{prefix}_clean.txt", "w", encoding="utf-8").write(full)
with open(f"{prefix}_timed.txt", "w", encoding="utf-8") as f:
    for t, tm in zip(clean, ts):
        f.write(f"[{tm}] {t}\n")

print(f"segments={len(clean)}  chars={len(full)}")
print(f"-> {prefix}_clean.txt, {prefix}_timed.txt")
