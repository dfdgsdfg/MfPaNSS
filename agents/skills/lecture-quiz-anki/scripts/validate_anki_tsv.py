#!/usr/bin/env python3
"""Anki 임포트용 TSV 형식 점검기.

Anki 임포트가 깨지는 흔한 원인을 잡는다:
 - 디렉티브(#separator:tab 등) 누락
 - 데이터 행의 필드 수가 3(Front/Back/Tags)이 아님 (탭 개수 != 2)
 - 수식에 $...$ 사용 (Anki 기본 렌더 안 됨 → \\( ... \\) 써야 함)
 - \\( 와 \\) 개수 불일치
 - Front/Back 빈 값

사용:  python validate_anki_tsv.py <deck.tsv>
종료코드 0 = 통과, 1 = 문제 있음.
"""
import sys, re

path = sys.argv[1]
lines = open(path, encoding="utf-8").read().split("\n")

directives = [l for l in lines if l.startswith("#")]
data = [l for l in lines if l and not l.startswith("#")]

problems = []

if not any(l.lower().startswith("#separator:") for l in directives):
    problems.append("디렉티브 누락: #separator:tab")
if not any("tab" in l.lower() for l in directives if l.lower().startswith("#separator:")):
    problems.append("#separator 가 tab 이 아님")

dollar = bal = badfields = empty = 0
for i, l in enumerate(data, 1):
    nf = l.count("\t") + 1
    if nf != 3:
        badfields += 1
        if badfields <= 5:
            problems.append(f"[행 {i}] 필드 {nf}개 (3이어야): {l[:60]}…")
    parts = l.split("\t")
    if len(parts) >= 2 and (not parts[0].strip() or not parts[1].strip()):
        empty += 1
    if "$" in l:
        dollar += 1
        if dollar <= 5:
            problems.append(f"[행 {i}] '$' 발견 — Anki는 \\( \\) 를 써야 함: {l[:60]}…")
    if l.count(r"\(") != l.count(r"\)"):
        bal += 1
        if bal <= 5:
            problems.append(f"[행 {i}] \\( \\) 개수 불일치: {l[:60]}…")

print(f"디렉티브 {len(directives)}줄, 카드 {len(data)}장")
print(f"  필드오류 {badfields} · '$'수식 {dollar} · 괄호불일치 {bal} · 빈필드 {empty}")
if problems:
    print("\n문제:")
    for p in problems[:30]:
        print("  -", p)
    sys.exit(1)
print("✅ 통과")
