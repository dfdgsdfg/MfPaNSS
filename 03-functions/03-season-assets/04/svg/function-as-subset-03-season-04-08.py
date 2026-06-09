#!/usr/bin/env python3
"""Static figure for 03강 3기 04강 — a function as a subset of A x B (lecture §8).

A function f: A -> B is a subset of the product set A x B in which, for every
a in A, the pair (a, b) exists for exactly one b (existence + uniqueness). The
figure contrasts a valid function with two failing relations: one input with no
output (existence fails) and one input with two outputs (uniqueness fails).

Renders next to itself as an SVG embedded by the note.

Reproduce:
    uv run --with matplotlib --with numpy python function-as-subset-03-season-04-08.py
"""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = Path(__file__).with_suffix(".svg")

A = ["a1", "a2", "a3", "a4"]   # domain elements -> x axis
B = ["b1", "b2", "b3"]         # codomain elements -> y axis

# (a_index, b_index) chosen points for each panel
GOOD = [(0, 0), (1, 2), (2, 1), (3, 2)]            # one output per input: a function
NO_OUTPUT = [(0, 0), (1, 2), (3, 1)]               # a2 has no output -> not a function
TWO_OUTPUT = [(0, 0), (1, 2), (1, 0), (2, 1), (3, 2)]  # a2 -> two outputs -> not

BLUE, RED, GREEN, GRID = "#1f6feb", "#d1242f", "#0b8457", "#d0d7de"

fig, axes = plt.subplots(1, 3, figsize=(11.0, 4.0))


def draw_grid(ax, title, color, points, bad_col=None):
    nx, ny = len(A), len(B)
    # cell grid for the product set A x B
    for i in range(nx):
        for j in range(ny):
            ax.add_patch(Rectangle((i - 0.5, j - 0.5), 1, 1, fill=False,
                                   edgecolor=GRID, lw=0.8, zorder=1))
    # plot the chosen pairs (the relation as a subset of A x B)
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.scatter(xs, ys, s=190, color=color, zorder=4, edgecolors="white", linewidths=1.4)
    # highlight the offending column for the failing panels
    if bad_col is not None:
        ax.add_patch(Rectangle((bad_col - 0.5, -0.5), 1, ny, fill=True,
                               facecolor=RED, alpha=0.10, edgecolor="none", zorder=0))
    ax.set_xticks(range(nx)); ax.set_xticklabels(A)
    ax.set_yticks(range(ny)); ax.set_yticklabels(B)
    ax.set_xlim(-0.6, nx - 0.4); ax.set_ylim(-0.6, ny - 0.4)
    ax.set_xlabel("A  (domain)"); ax.set_ylabel("B  (codomain)")
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=12, pad=8)
    for s in ax.spines.values():
        s.set_edgecolor(GRID)
    ax.tick_params(length=0)


draw_grid(axes[0], "a function:\none point per column", GREEN, GOOD)
draw_grid(axes[1], "not a function:\na2 has NO output", RED, NO_OUTPUT, bad_col=1)
draw_grid(axes[2], "not a function:\na2 has TWO outputs", RED, TWO_OUTPUT, bad_col=1)

fig.suptitle(r"A function $f:A\to B$ is a subset of $A\times B$ "
             r"with exactly one $(a,b)$ per $a$", fontsize=13, y=1.04)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}")
print(f"  panel 1 (function):      {len(GOOD)} points, one per column of {len(A)} -> valid")
print(f"  panel 2 (no output):     a2 column empty -> existence fails")
print(f"  panel 3 (two outputs):   a2 column has 2 points -> uniqueness fails")
