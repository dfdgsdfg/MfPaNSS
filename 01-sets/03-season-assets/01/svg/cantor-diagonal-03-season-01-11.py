#!/usr/bin/env python3
"""Static figure for 01강 3기 01강 — Cantor's diagonal argument (lecture §11):
why the reals cannot be listed (번호 매기기) the way N, Z, Q can. We lay out a
hypothetical enumeration r_1, r_2, ... of reals in [0,1], highlight the diagonal
digits, and build a new number d that differs from r_n in the n-th place — so d
is not on the list. Renders next to itself as an SVG embedded by the note.

Reproduce:  uv run --with matplotlib --with numpy python cantor-diagonal-03-season-01-11.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = Path(__file__).with_suffix(".svg")

# A hypothetical enumeration of reals in [0,1] by their decimal digits.
# Row i = r_i, column j = j-th digit after the point.
N = 6
rng = np.random.default_rng(1)
digits = rng.integers(0, 10, size=(N, N))
# pin the diagonal to a readable set of values
diag = np.array([4, 1, 7, 0, 5, 9])
for i in range(N):
    digits[i, i] = diag[i]

# diagonal rule: new digit d_i = diagonal digit + 1 (mod 10) -> differs in place i
new = (diag + 1) % 10

BLUE, RED, GREEN, GREY, INK = "#1f6feb", "#d1242f", "#0b8457", "#6e7781", "#24292f"

fig, ax = plt.subplots(figsize=(6.6, 5.0))

x0, dx = 1.55, 0.62          # first digit column x, column spacing
y_top, dy = N - 0.0, 1.0     # first row y, row spacing


def cell_xy(i, j):
    return x0 + j * dx, y_top - i * dy


# row labels  r_1 ... r_N  and the leading "0."
for i in range(N):
    _, y = cell_xy(i, 0)
    ax.text(0.15, y, rf"$r_{{{i+1}}}=$", fontsize=13, color=INK, va="center")
    ax.text(x0 - 0.55, y, "0.", fontsize=13, color=INK, va="center")
    for j in range(N):
        x, _ = cell_xy(i, j)
        if i == j:  # diagonal digit gets a highlight box
            ax.add_patch(Rectangle((x - 0.26, y - 0.34), 0.52, 0.68,
                                   facecolor="#fff1c2", edgecolor=RED,
                                   lw=1.6, zorder=1))
        col = RED if i == j else INK
        wt = "bold" if i == j else "normal"
        ax.text(x, y, str(digits[i, j]), fontsize=14, color=col,
                ha="center", va="center", weight=wt, zorder=2)
    # trailing ellipsis
    ax.text(x0 + N * dx - 0.18, y, r"$\cdots$", fontsize=13, color=GREY, va="center")

ax.text(0.15, y_top - N * dy + 0.05, r"$\vdots$", fontsize=15, color=GREY, ha="left")

# the constructed number d, one row below the table
yd = y_top - N * dy - 0.15
ax.text(0.15, yd, r"$d=$", fontsize=13, color=GREEN, va="center")
ax.text(x0 - 0.55, yd, "0.", fontsize=13, color=GREEN, va="center")
for j in range(N):
    x, _ = cell_xy(0, j)
    ax.text(x, yd, str(new[j]), fontsize=14, color=GREEN, ha="center",
            va="center", weight="bold")
ax.text(x0 + N * dx - 0.18, yd, r"$\cdots$", fontsize=13, color=GREEN, va="center")

# arrows: each new digit differs from the boxed diagonal digit above it
for j in range(N):
    x, ytop = cell_xy(j, j)
    ax.annotate("", xy=(x, yd + 0.34), xytext=(x, ytop - 0.36),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.2,
                                shrinkA=0, shrinkB=0, alpha=0.7))

# captions / the rule
ax.text(x0 + N * dx + 0.30, (y_top + yd) / 2 + 0.2,
        "diagonal rule:\n" r"$d_n \neq r_n$'s $n$-th digit",
        fontsize=11.5, color=RED, va="center")
ax.text(0.15, yd - 1.05,
        r"$d$ differs from every $r_n$ in place $n$, so $d$ is on no row:",
        fontsize=12, color=INK)
ax.text(0.15, yd - 1.70,
        r"the reals $\mathbb{R}$ cannot be listed $\Rightarrow\ |\mathbb{R}| > |\mathbb{N}|$.",
        fontsize=12.5, color=INK, weight="bold")

ax.set_xlim(0, x0 + N * dx + 2.5)
ax.set_ylim(yd - 2.1, y_top + 0.7)
ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}  (diagonal={diag.tolist()}, d={new.tolist()})")
