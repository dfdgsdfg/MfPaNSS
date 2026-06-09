#!/usr/bin/env python3
"""Static figure for 01강 3기 02강 — "같다"는 말에는 기준이 필요하다 (lecture §6).
The lecture's anchoring example: N and Z have the *same size* under the criterion
of a one-to-one correspondence (일대일 대응), even though Z "contains" N. We draw
the explicit bijection N -> Z that zig-zags 0, 1, -1, 2, -2, ... and pairs every
natural number with exactly one integer (and vice versa). Renders next to itself
as an SVG embedded by the note.

Reproduce:  uv run --with matplotlib --with numpy python bijection-natural-integer-03-season-02-06.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

OUT = Path(__file__).with_suffix(".svg")

# The bijection f: N -> Z,  f(n) = n/2 if n even, -(n+1)/2 if n odd.
#   n :  0  1  2  3  4  5  6 ...
#  f(n):  0  -1  1  -2  2  -3  3 ...  (we order Z as 0, +1, -1, +2, -2, ...)
N = 7
naturals = list(range(N))


def f(n):
    return n // 2 if n % 2 == 0 else -(n + 1) // 2


images = [f(n) for n in naturals]

# Lay Z on the top row ordered the way the correspondence reaches them,
# so the matching lines stay tidy and the pairing is visually clear.
z_order = [0, -1, 1, -2, 2, -3, 3]          # = images, in reach order

BLUE, RED, GREEN, GREY, INK = "#1f6feb", "#d1242f", "#0b8457", "#6e7781", "#24292f"

fig, ax = plt.subplots(figsize=(7.4, 3.6))

dx = 1.0
x = [j * dx for j in range(N)]
y_top, y_bot = 1.0, 0.0

# top row: integers Z (reached order), bottom row: naturals N
for j in range(N):
    # integer node
    ax.scatter([x[j]], [y_top], s=560, facecolor="#eaf2ff", edgecolor=BLUE,
               lw=1.6, zorder=3)
    label = f"+{z_order[j]}" if z_order[j] > 0 else str(z_order[j])
    ax.text(x[j], y_top, label, ha="center", va="center", fontsize=12.5,
            color=BLUE, weight="bold", zorder=4)
    # natural node
    ax.scatter([x[j]], [y_bot], s=560, facecolor="#eafaf0", edgecolor=GREEN,
               lw=1.6, zorder=3)
    ax.text(x[j], y_bot, str(naturals[j]), ha="center", va="center",
            fontsize=12.5, color=GREEN, weight="bold", zorder=4)
    # the matching arrow n -> f(n)  (straight up: column order == reach order)
    ax.add_patch(FancyArrowPatch((x[j], y_bot + 0.16), (x[j], y_top - 0.16),
                                 arrowstyle="-|>", mutation_scale=12, lw=1.5,
                                 color=GREY, shrinkA=0, shrinkB=0, zorder=2))

# trailing ellipses on both rows
ax.text(x[-1] + dx * 0.7, y_top, r"$\cdots$", fontsize=14, color=BLUE, va="center")
ax.text(x[-1] + dx * 0.7, y_bot, r"$\cdots$", fontsize=14, color=GREEN, va="center")

# set labels
ax.text(-0.95, y_top, r"$\mathbb{Z}$", fontsize=16, color=BLUE, va="center", weight="bold")
ax.text(-0.95, y_bot, r"$\mathbb{N}$", fontsize=16, color=GREEN, va="center", weight="bold")

# the rule and the conclusion
ax.text(x[3], y_top + 0.78,
        r"$f:\mathbb{N}\to\mathbb{Z},\quad "
        r"f(n)=\dfrac{n}{2}\ (n\ \mathrm{even}),\ \ -\dfrac{n+1}{2}\ (n\ \mathrm{odd})$",
        ha="center", va="center", fontsize=12.5, color=INK)
ax.text(x[3], y_bot - 0.72,
        r"one-to-one and onto  $\Rightarrow\ |\mathbb{N}| = |\mathbb{Z}|$  "
        r"(same size, even though $\mathbb{N}\subsetneq\mathbb{Z}$)",
        ha="center", va="center", fontsize=12.5, color=RED, weight="bold")

ax.set_xlim(-1.6, x[-1] + dx * 1.5)
ax.set_ylim(y_bot - 1.15, y_top + 1.15)
ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")

# sanity check: f is injective on the shown range and hits each listed integer once
assert images == z_order, (images, z_order)
assert len(set(images)) == len(images)
print(f"wrote {OUT}  (N->Z: {list(zip(naturals, images))})")
