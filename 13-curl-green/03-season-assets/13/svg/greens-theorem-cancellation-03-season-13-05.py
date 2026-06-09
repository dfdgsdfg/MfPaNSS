#!/usr/bin/env python3
"""Static figure for 13강 3기 13강 — Green's theorem as "interior curl summed up =
boundary circulation" (lecture §5). When the region R is cut into a fine grid, each
small cell carries a counter-clockwise circulation; the contributions on every shared
inner edge cancel (two neighbours traverse it in opposite directions), and only the
outer boundary C survives. Renders next to itself as an SVG embedded by the note.

Reproduce:  uv run --with matplotlib --with numpy python greens-theorem-cancellation-03-season-13-05.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

OUT = Path(__file__).with_suffix(".svg")

N = 4                      # N x N grid of cells over the unit square
INNER = "#9aa7b8"
OUTER = "#1f6feb"
CELL = "#d1242f"

fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.2, 5.2))


def curved_arrow(ax, p0, p1, color, lw, rad=0.0, scale=11):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=scale,
                                 lw=lw, color=color, shrinkA=0, shrinkB=0,
                                 connectionstyle=f"arc3,rad={rad}", zorder=5))


def ccw_loop(ax, x0, y0, s, color, lw, scale=9):
    """Draw a counter-clockwise circulation around the cell [x0,x0+s] x [y0,y0+s]."""
    corners = [(x0, y0), (x0 + s, y0), (x0 + s, y0 + s), (x0, y0 + s), (x0, y0)]
    for (ax0, ay0), (ax1, ay1) in zip(corners[:-1], corners[1:]):
        mx, my = (ax0 + ax1) / 2, (ay0 + ay1) / 2
        dx, dy = ax1 - ax0, ay1 - ay0
        # short arrow centred on each edge, pointing along the CCW traversal
        curved_arrow(ax, (mx - 0.30 * dx, my - 0.30 * dy),
                     (mx + 0.30 * dx, my + 0.30 * dy), color, lw, scale=scale)


# ---- LEFT: every cell circulates CCW; inner edges carry opposing arrows ----
for i in range(N):
    for j in range(N):
        ccw_loop(axL, i, j, 1.0, CELL, 1.3)
# grid lines
for k in range(N + 1):
    axL.plot([0, N], [k, k], color=INNER, lw=0.8, zorder=1)
    axL.plot([k, k], [0, N], color=INNER, lw=0.8, zorder=1)
axL.set_title("Each cell circulates CCW\n(inner edges oppose -> cancel)", fontsize=12)

# ---- RIGHT: interior cancels, only the outer boundary survives ----
# faint grid for reference
for k in range(N + 1):
    axR.plot([0, N], [k, k], color="#e1e6eb", lw=0.7, zorder=0)
    axR.plot([k, k], [0, N], color="#e1e6eb", lw=0.7, zorder=0)
# outer boundary C, traversed CCW
bx = [0, N, N, 0, 0]
by = [0, 0, N, N, 0]
axR.plot(bx, by, color=OUTER, lw=2.4, zorder=2)
edges = [((0, 0), (N, 0)), ((N, 0), (N, N)),
         ((N, N), (0, N)), ((0, N), (0, 0))]
for (x0, y0), (x1, y1) in edges:
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    curved_arrow(axR, (mx - 0.18 * dx, my - 0.18 * dy),
                 (mx + 0.18 * dx, my + 0.18 * dy), OUTER, 2.4, scale=16)
axR.text(N / 2, -0.55, r"$\oint_C M\,dx + N\,dy$", ha="center", fontsize=12.5, color=OUTER)
axR.text(N / 2, N / 2, r"$\iint_R\!\left(\dfrac{\partial N}{\partial x}-\dfrac{\partial M}{\partial y}\right)dx\,dy$",
         ha="center", va="center", fontsize=11.5, color=CELL)
axR.set_title("Interior cancels -> boundary C remains", fontsize=12)

for ax in (axL, axR):
    ax.set_xlim(-0.7, N + 0.7)
    ax.set_ylim(-0.95, N + 0.7)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

fig.suptitle("Green's theorem: summed interior curl = boundary circulation", fontsize=13)
fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}  (grid {N}x{N}, {N*N} cells, inner edges cancel pairwise)")
