#!/usr/bin/env python3
"""Static figure for 07강 4기 14강 — why the parallelogram spanned by (a,b) and
(c,d) has area ad - bc (lecture §2). The note's derivation rotates the side (a,b)
onto the x-axis, then reads off "base x height"; after rotation base = sqrt(a^2+b^2)
and height = the rotated y-component of (c,d), and base*height collapses to ad - bc.

Reproduce:
  uv run --with matplotlib --with numpy python parallelogram-area-determinant-04-season-14-02.py
"""
from pathlib import Path
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch

OUT = Path(__file__).with_suffix(".svg")

# the two column vectors (a,b) and (c,d)
a, b = 3.0, 1.0
c, d = 1.0, 2.5
v1 = np.array([a, b])
v2 = np.array([c, d])
det = a * d - b * c

# rotate by -theta so that v1 lands on the +x axis
L = math.hypot(a, b)
cos, sin = a / L, b / L
R = np.array([[cos, sin], [-sin, cos]])
r1 = R @ v1            # = (sqrt(a^2+b^2), 0)
r2 = R @ v2            # height = r2[1]
base, height = r1[0], r2[1]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 5.0))


def arrow(ax, p, color, lw=2.2):
    ax.add_patch(FancyArrowPatch((0, 0), p, arrowstyle="-|>", mutation_scale=16,
                                 lw=lw, color=color, shrinkA=0, shrinkB=0, zorder=5))


def setup(ax, xlim, ylim, title):
    ax.set_title(title, fontsize=12)
    ax.axhline(0, color="#d0d7de", lw=0.8, zorder=0)
    ax.axvline(0, color="#d0d7de", lw=0.8, zorder=0)
    ax.scatter([0], [0], s=16, color="#24292f", zorder=6)
    ax.text(-0.28, -0.30, r"$O$", fontsize=11, color="#24292f")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


# ----- left: the original parallelogram spanned by (a,b) and (c,d) -----
poly = np.array([[0, 0], v1, v1 + v2, v2])
ax1.add_patch(Polygon(poly, closed=True, facecolor="#cfe8d8",
                      edgecolor="#0b8457", lw=1.4, alpha=0.7, zorder=1))
arrow(ax1, v1, "#1f6feb")
arrow(ax1, v2, "#d1242f")
ax1.text(v1[0] + 0.08, v1[1] - 0.28, r"$(a,b)$", color="#1f6feb", fontsize=13, weight="bold")
ax1.text(v2[0] - 0.65, v2[1] + 0.12, r"$(c,d)$", color="#d1242f", fontsize=13, weight="bold")
ax1.text(2.0, 1.55, r"area $= ad-bc$", color="#0b8457", fontsize=12.5, ha="center")
setup(ax1, (-0.7, 4.6), (-0.7, 4.1), "spanned by (a,b), (c,d)")

# ----- right: rotated so (a,b) lies on the x-axis -> base x height -----
rpoly = np.array([[0, 0], r1, r1 + r2, r2])
ax2.add_patch(Polygon(rpoly, closed=True, facecolor="#cfe8d8",
                      edgecolor="#0b8457", lw=1.4, alpha=0.7, zorder=1))
arrow(ax2, r1, "#1f6feb")
arrow(ax2, r2, "#d1242f")
# height drop from r2 down to the base (x-axis)
ax2.plot([r2[0], r2[0]], [0, r2[1]], color="#6e7781", lw=1.3, ls=":", zorder=4)
# right-angle marker at the foot of the height
s = 0.18
ax2.plot([r2[0] - s, r2[0] - s, r2[0]], [0, s, s], color="#6e7781", lw=1.0, zorder=4)
# base bracket label
ax2.annotate("", xy=(r1[0], -0.45), xytext=(0, -0.45),
             arrowprops=dict(arrowstyle="<->", color="#1f6feb", lw=1.2))
ax2.text(r1[0] / 2, -0.85, r"base $=\sqrt{a^2+b^2}$", color="#1f6feb",
         fontsize=11.5, ha="center")
ax2.annotate("", xy=(r2[0] + 0.0, r2[1]), xytext=(r2[0] + 0.0, 0),
             arrowprops=dict(arrowstyle="<->", color="#d1242f", lw=1.2))
ax2.text(r2[0] + 0.18, r2[1] / 2, "height", color="#d1242f",
         fontsize=11.5, ha="left", va="center", rotation=90)
ax2.text(2.45, 2.7, r"area $=$ base $\times$ height $= ad-bc$",
         color="#0b8457", fontsize=12, ha="center")
setup(ax2, (-0.7, 4.6), (-1.2, 4.1), "rotate (a,b) onto x-axis")

fig.suptitle(r"Parallelogram area $= ad-bc$  (rotate, then base $\times$ height)",
             fontsize=13)
fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}")
print(f"  det = ad-bc = {det:.2f}")
print(f"  base = {base:.4f}, height = {height:.4f}, base*height = {base*height:.4f}")
