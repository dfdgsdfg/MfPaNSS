#!/usr/bin/env python3
"""Static figure for 10강 3기 07강 — separating "spread" (divergence) from "spin"
(curl) on the two recurring example vector fields (lecture §10, also §4/§7):

    F(x,y) = (x, y)    pure source, div F = 2, curl F = 0
    F(x,y) = (-y, x)   pure rotation, div F = 0, curl F = 2

Renders next to itself as an SVG embedded by the note.

Reproduce:  uv run --with matplotlib --with numpy python divergence-vs-curl-fields-03-season-07-10.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).with_suffix(".svg")

# sample grid
g = np.linspace(-1.6, 1.6, 9)
X, Y = np.meshgrid(g, g)

# the two example fields from the note
fields = [
    ("F(x,y) = (x, y)", X, Y, "div F = 2,  curl F = 0", "source: arrows flow out", "#d1242f"),
    ("F(x,y) = (-y, x)", -Y, X, "div F = 0,  curl F = 2", "rotation: arrows circulate", "#1f6feb"),
]

fig, axes = plt.subplots(1, 2, figsize=(10.4, 5.2))

# verify the divergence / curl numerically (finite-difference on a fine grid)
def div_curl(fx, fy):
    h = 1e-4
    dFx_dx = (fx(X + h, Y) - fx(X - h, Y)) / (2 * h)
    dFy_dy = (fy(X, Y + h) - fy(X, Y - h)) / (2 * h)
    dFy_dx = (fy(X + h, Y) - fy(X - h, Y)) / (2 * h)
    dFx_dy = (fx(X, Y + h) - fx(X, Y - h)) / (2 * h)
    return (dFx_dx + dFy_dy), (dFy_dx - dFx_dy)

checks = [
    div_curl(lambda x, y: x, lambda x, y: y),
    div_curl(lambda x, y: -y, lambda x, y: x),
]

for ax, (title, U, V, tag, sub, color), (dv, cl) in zip(axes, fields, checks):
    ax.quiver(X, Y, U, V, color=color, angles="xy", scale_units="xy",
              scale=2.4, width=0.006, alpha=0.9, zorder=3)

    # a small test disk at the origin to read the local behaviour
    th = np.linspace(0, 2 * np.pi, 200)
    r = 0.7
    ax.plot(r * np.cos(th), r * np.sin(th), color="#57606a", lw=1.4,
            ls=(0, (5, 3)), zorder=4)
    ax.scatter([0], [0], s=16, color="#24292f", zorder=5)

    ax.set_title(f"{title}\n{tag}", fontsize=13)
    ax.text(0, -2.18, sub, ha="center", fontsize=11, color=color)
    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-2.0, 2.0)
    ax.set_aspect("equal")
    ax.axhline(0, color="#d0d7de", lw=0.8, zorder=0)
    ax.axvline(0, color="#d0d7de", lw=0.8, zorder=0)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.tick_params(labelsize=9)

fig.suptitle("Spread (divergence) vs spin (curl): same arrows, different questions",
             fontsize=13.5, y=1.0)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")

# print the numeric verification
print(f"wrote {OUT}")
print(f"  (x,y):  div={checks[0][0].mean():.3f}  curl={checks[0][1].mean():.3f}  (expect 2, 0)")
print(f"  (-y,x): div={checks[1][0].mean():.3f}  curl={checks[1][1].mean():.3f}  (expect 0, 2)")
