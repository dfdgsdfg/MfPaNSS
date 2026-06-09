#!/usr/bin/env python3
"""Static figure for 05강 3기 07강 — the determinant ad-bc read as the SIGNED
AREA of the parallelogram spanned by the two COLUMN vectors of a 2x2 matrix
(lecture §6, the closing 떡밥).

Two panels:
  (left)  an invertible A = [[2,1],[1,2]]: the columns u=(2,1), v=(1,2) are two
          different directions, so they span a parallelogram of area det A = 3 > 0.
          The plane can be undone -> the inverse exists.
  (right) a singular A = [[2,1],[2,1]]: the columns u=(2,2), v=(1,1) are PARALLEL
          (v = (1/2)u), the parallelogram collapses to a segment, area = 0, the
          unit square is squashed onto a line -> not invertible.

So  det A = ad - bc = 0  <=>  u || v  <=>  area = 0  <=>  no inverse.

Reproduce: uv run --with matplotlib --with numpy python \
           determinant-parallelogram-area-03-season-07-06.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon

OUT = Path(__file__).with_suffix(".svg")

GRID = "#d0d7de"
INK = "#24292f"
BLUE = "#1f6feb"
RED = "#d1242f"
FILL = "#0b8457"
GREY = "#57606a"


def det2(a, b, c, d):
    return a * d - b * c


def arrow(ax, tail, head, color, lw=2.4, scale=18, z=6):
    ax.add_patch(FancyArrowPatch(tail, head, arrowstyle="-|>", mutation_scale=scale,
                                 lw=lw, color=color, shrinkA=0, shrinkB=0, zorder=z))


def frame(ax, lim=3.4):
    ax.axhline(0, color=GRID, lw=0.8, zorder=0)
    ax.axvline(0, color=GRID, lw=0.8, zorder=0)
    for k in range(-3, 4):
        ax.plot([k, k], [-lim, lim], color=GRID, lw=0.5, zorder=0)
        ax.plot([-lim, lim], [k, k], color=GRID, lw=0.5, zorder=0)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.scatter([0], [0], s=16, color=INK, zorder=7)
    ax.text(-0.27, -0.27, r"$O$", fontsize=11, color=INK)


fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.4, 5.6))

# ---------------- LEFT: invertible -> nonzero parallelogram area ----------------
a, b, c, d = 2.0, 1.0, 1.0, 2.0          # A = [[a,b],[c,d]]
u = np.array([a, c])                      # first column
v = np.array([b, d])                      # second column
area = det2(a, b, c, d)                   # signed area of the (u,v) parallelogram

frame(axL)
pgram = Polygon([[0, 0], u, u + v, v], closed=True, facecolor=FILL,
                alpha=0.16, edgecolor=FILL, lw=1.2, zorder=1)
axL.add_patch(pgram)
arrow(axL, (0, 0), u, BLUE)
arrow(axL, (0, 0), v, RED)
axL.text(u[0] + 0.06, u[1] - 0.28, r"$u=(a,c)=(2,1)$", color=BLUE, fontsize=11.5)
axL.text(v[0] - 0.30, v[1] + 0.12, r"$v=(b,d)=(1,2)$", color=RED, fontsize=11.5)
axL.text((u[0] + v[0]) / 2 - 0.35, (u[1] + v[1]) / 2,
         r"area $=ad-bc=3$", color=INK, fontsize=12)
axL.set_title(r"$\det A = ad-bc = 3 \neq 0$"
              "\n"
              r"$u,v$ span area $\to$ $A^{-1}$ exists",
              fontsize=12.5, color=INK)

# ---------------- RIGHT: singular -> collapsed area = 0 ----------------
a2, b2, c2, d2 = 2.0, 1.0, 2.0, 1.0      # A = [[2,1],[2,1]]
u2 = np.array([a2, c2])                   # (2,2)
v2 = np.array([b2, d2])                   # (1,1)  = (1/2) u2  -> parallel
area2 = det2(a2, b2, c2, d2)             # = 0

frame(axR)
# the "parallelogram" is degenerate: both columns lie on the same line y=x
axR.plot([-3.2, 3.2], [-3.2, 3.2], color=GREY, lw=1.1, ls=(0, (6, 4)), zorder=1)
arrow(axR, (0, 0), u2, BLUE)
arrow(axR, (0, 0), v2, RED)
axR.text(u2[0] + 0.08, u2[1] - 0.30, r"$u=(a,c)=(2,2)$", color=BLUE, fontsize=11.5)
axR.text(v2[0] - 1.85, v2[1] + 0.20, r"$v=(b,d)=(1,1)=\frac{1}{2}u$", color=RED, fontsize=11.5)
axR.text(-3.2, -2.0, r"area $=ad-bc=0$", color=INK, fontsize=12)
axR.set_title(r"$\det A = ad-bc = 0,\ \ u \parallel v$"
              "\n"
              r"area collapses $\to$ no $A^{-1}$",
              fontsize=12.5, color=INK)

fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}")
print(f"  LEFT  A=[[2,1],[1,2]]  det=ad-bc={area:.1f}  (u,v not parallel, area>0)")
print(f"  RIGHT A=[[2,1],[2,1]]  det=ad-bc={area2:.1f}  (u||v, area=0)")
print(f"  cross-check via numpy: {np.linalg.det([[2,1],[1,2]]):.1f}, "
      f"{np.linalg.det([[2,1],[2,1]]):.1f}")
