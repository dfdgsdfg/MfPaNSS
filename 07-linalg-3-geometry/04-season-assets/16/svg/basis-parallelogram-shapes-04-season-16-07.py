#!/usr/bin/env python3
"""Static figure for 07강 4기 16강 — the basis vectors (1,0),(0,1) fix only the
linear structure, NOT a size or an angle (lecture §7). The same two basis vectors
can span a square (the Euclidean convention) OR any other parallelogram once we are
free to choose their lengths and the angle between them. Renders next to itself as
an SVG embedded by the note.

Reproduce:  uv run --with matplotlib --with numpy python basis-parallelogram-shapes-04-season-16-07.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch, Arc

OUT = Path(__file__).with_suffix(".svg")

# Three readings of the SAME pair of basis vectors e1=(1,0), e2=(0,1).
# Each panel chooses a (length of e1, length of e2, angle of e2) — none of which
# linearity alone can decide.
panels = [
    ("Euclidean convention\n|e1|=|e2|=1,  angle=90 deg", 1.0, 1.0, 90.0, "#1f6feb"),
    ("rescaled\n|e1|=sqrt(2), |e2|=sqrt(3), angle=90 deg", np.sqrt(2), np.sqrt(3), 90.0, "#0b8457"),
    ("sheared\n|e1|=1.4, |e2|=1.4, angle=60 deg", 1.4, 1.4, 60.0, "#d1242f"),
]

fig, axes = plt.subplots(1, 3, figsize=(11.0, 4.0))


def arrow(ax, p, color, lw=2.4):
    ax.add_patch(FancyArrowPatch((0, 0), p, arrowstyle="-|>", mutation_scale=15,
                                 lw=lw, color=color, shrinkA=0, shrinkB=0, zorder=5))


for ax, (title, l1, l2, ang, color) in zip(axes, panels):
    a = np.radians(ang)
    e1 = np.array([l1, 0.0])                      # first basis vector along x
    e2 = np.array([l2 * np.cos(a), l2 * np.sin(a)])  # second basis vector at given angle

    # parallelogram O, e1, e1+e2, e2
    poly = np.array([[0, 0], e1, e1 + e2, e2])
    ax.add_patch(Polygon(poly, closed=True, facecolor=color, alpha=0.13,
                         edgecolor=color, lw=1.6, zorder=2))

    arrow(ax, e1, color)
    arrow(ax, e2, color)

    # angle arc between the two basis vectors
    ax.add_patch(Arc((0, 0), 0.7, 0.7, angle=0, theta1=0, theta2=ang,
                     color="#57606a", lw=1.2, zorder=4))

    ax.text(e1[0] + 0.06, e1[1] - 0.22, r"$e_1$", color=color, fontsize=13, weight="bold")
    ax.text(e2[0] - 0.30, e2[1] + 0.06, r"$e_2$", color=color, fontsize=13, weight="bold")

    ax.scatter([0], [0], s=14, color="#24292f", zorder=6)
    ax.set_title(title, fontsize=10.5)
    ax.set_xlim(-0.9, 2.3)
    ax.set_ylim(-0.6, 2.3)
    ax.set_aspect("equal")
    ax.axhline(0, color="#d0d7de", lw=0.8, zorder=0)
    ax.axvline(0, color="#d0d7de", lw=0.8, zorder=0)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

fig.suptitle(r"Same basis $e_1=(1,0),\ e_2=(0,1)$ — linearity fixes neither size nor angle",
             fontsize=12.5, y=1.02)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}")
for title, l1, l2, ang, _ in panels:
    a = np.radians(ang)
    e2 = np.array([l2 * np.cos(a), l2 * np.sin(a)])
    area = abs(l1 * e2[1])  # |e1 x e2| = base * height
    print(f"  {title.splitlines()[0]:<22}  |e1|={l1:.3f} |e2|={l2:.3f} angle={ang:g}  area={area:.3f}")
