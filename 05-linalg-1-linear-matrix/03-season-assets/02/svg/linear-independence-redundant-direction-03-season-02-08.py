#!/usr/bin/env python3
"""Static figure for 05강 3기 02강 — why (1,0),(0,1),(1,1) is linearly
DEPENDENT while (1,0),(0,1) is an independent basis of R^2 (lecture §4, §5, §8).

Two panels:
  (left)  the basis e1=(1,0), e2=(0,1): two different directions; mixing them
          a*e1 + b*e2 reaches every point of the plane, and the only way to get
          the zero vector is a=b=0  ->  independent + spanning = a basis.
  (right) add a third vector v3=(1,1). It is already the diagonal of the unit
          square, i.e. v3 = e1 + e2, so 1*e1 + 1*e2 - 1*v3 = 0 is a NON-trivial
          relation: the triple still spans the plane but is linearly dependent
          (a redundant direction).

Reproduce: uv run --with matplotlib --with numpy python \
           linear-independence-redundant-direction-03-season-02-08.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon

OUT = Path(__file__).with_suffix(".svg")

e1 = np.array([1.0, 0.0])
e2 = np.array([0.0, 1.0])
v3 = np.array([1.0, 1.0])

# sanity: the dependence relation that makes the triple dependent
relation = 1.0 * e1 + 1.0 * e2 - 1.0 * v3  # must be the zero vector

GRID = "#d0d7de"
INK = "#24292f"
BLUE = "#1f6feb"
RED = "#d1242f"
GREEN = "#0b8457"
GREY = "#57606a"


def arrow(ax, tail, head, color, lw=2.4, scale=18, z=6):
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
    ax.scatter([0], [0], s=16, color=INK, zorder=7)
    ax.text(-0.22, -0.22, r"$O$", fontsize=11, color=INK)


fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.2, 5.4))

# ---------------- LEFT: independent basis spans the plane ----------------
frame(axL)
# a couple of sample linear combinations to suggest "reaches everywhere"
for a, b in [(1.4, 0.7), (-0.8, 1.3), (1.1, -1.2)]:
    p = a * e1 + b * e2
    axL.scatter([p[0]], [p[1]], s=20, color="#9aa7b8", zorder=2)
arrow(axL, (0, 0), e1, BLUE)
arrow(axL, (0, 0), e2, GREEN)
axL.text(e1[0] + 0.06, e1[1] - 0.26, r"$v_1=(1,0)$", color=BLUE, fontsize=12)
axL.text(e2[0] - 0.30, e2[1] + 0.12, r"$v_2=(0,1)$", color=GREEN, fontsize=12)
axL.set_title(r"independent basis:  $a\,v_1+b\,v_2=0 \Rightarrow a=b=0$"
              "\n"
              r"two different directions $\to$ span all of $\mathbb{R}^2$",
              fontsize=12, color=INK)

# ---------------- RIGHT: adding v3=(1,1) makes it dependent ----------------
frame(axR)
# unit square / parallelogram showing v3 = e1 + e2
sq = Polygon([[0, 0], e1, v3, e2], closed=True, facecolor="#1f6feb",
             alpha=0.08, edgecolor=BLUE, lw=1.0, ls=(0, (5, 4)), zorder=1)
axR.add_patch(sq)
# e1, e2 translated to show the head-to-tail sum reaching v3
arrow(axR, (0, 0), e1, BLUE)
arrow(axR, (0, 0), e2, GREEN)
arrow(axR, e1, v3, GREEN, lw=1.6, scale=14)   # e2 carried from tip of e1
arrow(axR, e2, v3, BLUE, lw=1.6, scale=14)    # e1 carried from tip of e2
arrow(axR, (0, 0), v3, RED, lw=2.6)           # v3 itself = the diagonal
axR.text(e1[0] + 0.04, e1[1] - 0.26, r"$v_1=(1,0)$", color=BLUE, fontsize=12)
axR.text(e2[0] - 0.30, e2[1] + 0.10, r"$v_2=(0,1)$", color=GREEN, fontsize=12)
axR.text(v3[0] + 0.06, v3[1] + 0.04, r"$v_3=(1,1)=v_1+v_2$", color=RED, fontsize=12)
axR.set_title(r"redundant direction:  $1\,v_1+1\,v_2-1\,v_3=0$"
              "\n"
              r"spans $\mathbb{R}^2$ but linearly DEPENDENT (non-trivial relation)",
              fontsize=12, color=INK)

fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}")
print(f"  dependence relation 1*v1+1*v2-1*v3 = {tuple(relation)}  (should be (0.0, 0.0))")
print(f"  v1+v2 = {tuple(e1 + e2)}  == v3 ? {np.allclose(e1 + e2, v3)}")
