#!/usr/bin/env python3
"""Static figure for 05강 3기 06강 — matrix product IS the composition of linear
maps:  [g o f] = [g][f]  (lecture §9, §10).

We track the unit square (and the basis vectors e1,e2) through two successive
linear maps and show that applying f then g gives exactly the SAME image as the
single transformation by the product matrix C = G F.

  panel 1:  original unit square in R^2 with e1=(1,0), e2=(0,1).
  panel 2:  apply f  ->  F = [[1, 0.6],[0, 1]] (a shear).
  panel 3:  apply g to the result -> G = [[0, -1],[1, 0]] (a 90-deg rotation),
            i.e. the composite g o f.  Overlaid (dashed) is the unit square sent
            DIRECTLY through C = G F, which lands on top of it -> they coincide.

This makes the section's claim visual: the funny "rows-times-columns" rule and the
backwards order (right factor F acts first) are just "do f, then do g".

Reproduce: uv run --with matplotlib --with numpy python \
           matrix-product-is-composition-03-season-06-10.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon

OUT = Path(__file__).with_suffix(".svg")

GRID = "#d0d7de"
INK = "#24292f"
BLUE = "#1f6feb"
GREEN = "#0b8457"
RED = "#d1242f"
GREY = "#57606a"

# the two linear maps
F = np.array([[1.0, 0.6],
              [0.0, 1.0]])     # f : a shear
G = np.array([[0.0, -1.0],
              [1.0,  0.0]])    # g : a 90-degree rotation
C = G @ F                      # composite  g o f  ==  matrix product [g][f]

# sanity check: the product really is what "apply F then apply G" does
e1, e2 = np.array([1.0, 0.0]), np.array([0.0, 1.0])
assert np.allclose(C, np.column_stack([G @ (F @ e1), G @ (F @ e2)]))

# unit square corners (counter-clockwise)
SQ = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)


def arrow(ax, tail, head, color, lw=2.4, scale=17, z=6):
    ax.add_patch(FancyArrowPatch(tail, head, arrowstyle="-|>", mutation_scale=scale,
                                 lw=lw, color=color, shrinkA=0, shrinkB=0, zorder=z))


def frame(ax, lim=2.2):
    ax.axhline(0, color=GRID, lw=0.8, zorder=0)
    ax.axvline(0, color=GRID, lw=0.8, zorder=0)
    for k in range(-2, 3):
        ax.plot([k, k], [-lim, lim], color=GRID, lw=0.5, zorder=0)
        ax.plot([-lim, lim], [k, k], color=GRID, lw=0.5, zorder=0)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.scatter([0], [0], s=14, color=INK, zorder=7)


def draw_square(ax, M, facecolor, edgecolor, alpha=0.12, ls="-", lw=1.6, z=1):
    pts = SQ @ M.T
    ax.add_patch(Polygon(pts, closed=True, facecolor=facecolor, alpha=alpha,
                         edgecolor=edgecolor, lw=lw, ls=ls, zorder=z))


fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.8))
ax0, ax1, ax2 = axes

# ---------------- panel 1: original ----------------
frame(ax0)
draw_square(ax0, np.eye(2), BLUE, BLUE)
arrow(ax0, (0, 0), e1, BLUE)
arrow(ax0, (0, 0), e2, GREEN)
ax0.text(e1[0] + 0.05, e1[1] - 0.28, r"$e_1$", color=BLUE, fontsize=13)
ax0.text(e2[0] - 0.34, e2[1] + 0.06, r"$e_2$", color=GREEN, fontsize=13)
ax0.set_title(r"input:  unit square in $\mathbb{R}^2$", fontsize=12.5, color=INK)

# ---------------- panel 2: after f (= F) ----------------
frame(ax1)
draw_square(ax1, F, BLUE, BLUE)
arrow(ax1, (0, 0), F @ e1, BLUE)
arrow(ax1, (0, 0), F @ e2, GREEN)
ax1.text((F @ e1)[0] + 0.05, (F @ e1)[1] - 0.28, r"$f(e_1)$", color=BLUE, fontsize=12)
ax1.text((F @ e2)[0] - 0.10, (F @ e2)[1] + 0.10, r"$f(e_2)$", color=GREEN, fontsize=12)
ax1.set_title(r"apply $f$:   $F=[\,1\ 0.6\,;\,0\ 1\,]$  (shear)",
              fontsize=12.5, color=INK)

# ---------------- panel 3: after g (= composite g o f) ----------------
frame(ax2)
# direct route through the product C = G F, drawn dashed; it must coincide
draw_square(ax2, C, RED, RED, alpha=0.0, ls=(0, (6, 4)), lw=2.0, z=3)
# the staged route: g applied to the f-image
draw_square(ax2, C, GREEN, GREEN, alpha=0.14, ls="-", lw=1.6, z=1)
arrow(ax2, (0, 0), C @ e1, BLUE)
arrow(ax2, (0, 0), C @ e2, GREEN)
ax2.text((C @ e1)[0] - 0.10, (C @ e1)[1] + 0.10, r"$g(f(e_1))$", color=BLUE, fontsize=11)
ax2.text((C @ e2)[0] - 1.05, (C @ e2)[1] - 0.05, r"$g(f(e_2))$", color=GREEN, fontsize=11)
ax2.set_title(r"apply $g$ (90$^\circ$ rot.):   $g\circ f \;=\; [g][f]=GF$",
              fontsize=12.5, color=INK)
ax2.text(-2.05, -1.95,
         r"dashed = unit square sent DIRECTLY through $C=GF$  $\to$ same image",
         fontsize=10.5, color=RED)

fig.suptitle(r"matrix product is composition:   $[\,g\circ f\,]=[g][f]$   "
             r"(right factor $f$ acts first)", fontsize=14, color=INK, y=1.02)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}")
print(f"  F=\n{F}\n  G=\n{G}\n  C=GF=\n{C}")
print(f"  G(F e1)={G @ (F @ e1)}  C e1={C @ e1}  match={np.allclose(G @ (F @ e1), C @ e1)}")
print(f"  G(F e2)={G @ (F @ e2)}  C e2={C @ e2}  match={np.allclose(G @ (F @ e2), C @ e2)}")
