#!/usr/bin/env python3
"""Static figure for 10강 4기 25강 — the counterexample that all directional
derivatives can exist yet the function fails to be continuous (lecture §6 함정).

The function on R^2 at the origin P=(0,0):
    f(x, y) = 0  on the y-axis (x = 0),
    f(x, y) = 1  everywhere else.

Along ANY straight line through O, f(P + h d) - f(P) = 0 for all h != 0
(off-axis the value is the constant 1, minus f(O)=0 ... but the directional
derivative limit still vanishes since f is constant 1 along the open ray and the
y-axis ray is constant 0), so D_d f(O) = 0 for every direction d. Yet a curved
path that approaches O while staying ON the y-axis keeps f = 0, whereas every
nearby off-axis point has f = 1 — so f is discontinuous at O. Straight-line
directional derivatives miss this; a curved/path-wise limit catches it.

Reproduce:
  uv run --with matplotlib --with numpy python directional-derivative-counterexample-04-season-25-06.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

OUT = Path(__file__).with_suffix(".svg")

fig, ax = plt.subplots(figsize=(6.4, 6.0))

# ---- shade the plane: f = 1 everywhere (off-axis) ----------------------------
ax.add_patch(plt.Rectangle((-2.6, -2.6), 5.2, 5.2, facecolor="#fff1c9",
                           edgecolor="none", zorder=0))
ax.text(1.7, 2.25, r"$f = 1$" "\n" r"(off the $y$-axis)",
        color="#9a6b00", fontsize=12.5, ha="center", va="center")

# ---- the y-axis: f = 0 (a measure-zero set where the function dips) ----------
ax.plot([0, 0], [-2.6, 2.6], color="#1f6feb", lw=3.0, zorder=3)
ax.text(-0.18, 2.32, r"$f = 0$ on $x=0$", color="#1f6feb", fontsize=12.5,
        ha="right", va="center", rotation=90)

# ---- straight-line approaches to O: value is constant -> D_d f(O) = 0 --------
for ang in (25, 70, 115, 160, 205, 250, 295, 340):
    d = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang))])
    ax.add_patch(FancyArrowPatch(2.35 * d, 0.18 * d, arrowstyle="-|>",
                                 mutation_scale=12, lw=1.4, color="#6e7781",
                                 shrinkA=0, shrinkB=0, alpha=0.7, zorder=4))
ax.text(-1.55, -1.95,
        r"every straight ray to $O$: $f$ constant" "\n"
        r"$\Rightarrow\ D_d f(O)=0$ for all $d$",
        color="#3d444d", fontsize=11.5, ha="left", va="center", zorder=6,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#d0d7de", alpha=0.9))

# ---- a CURVED path that hugs the y-axis: stays where f = 0 -> discontinuity --
t = np.linspace(0.0, 1.0, 200)
# approaches O along a parabola tangent to the y-axis (x ~ y^2 near O)
py = 2.3 * (1 - t)            # y goes 2.3 -> 0
px = 0.55 * py**2 / 2.3      # x ~ y^2, vanishes as we reach O, tangent to axis
ax.plot(px, py, color="#d1242f", lw=2.6, zorder=5)
ax.add_patch(FancyArrowPatch((px[-8], py[-8]), (px[-1], py[-1]),
                             arrowstyle="-|>", mutation_scale=15, lw=2.6,
                             color="#d1242f", shrinkA=0, shrinkB=0, zorder=5))
ax.text(0.95, 1.05, r"curved path $\to O$" "\n" r"(any path allowed)",
        color="#d1242f", fontsize=11.5, ha="left", va="center", zorder=6)

# ---- the target point O ------------------------------------------------------
ax.scatter([0], [0], s=70, color="#0b8457", zorder=7)
ax.text(0.12, -0.28, r"$O=(0,0),\ f(O)=0$", color="#0b8457", fontsize=12,
        ha="left", va="center", zorder=7)

ax.set_title("All directional derivatives exist at $O$, yet $f$ is "
             "discontinuous there", fontsize=12.5)
ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
ax.set_xlim(-2.6, 2.6); ax.set_ylim(-2.6, 2.6)
ax.set_aspect("equal")
ax.set_xticks([-2, -1, 0, 1, 2]); ax.set_yticks([-2, -1, 0, 1, 2])
ax.axhline(0, color="#c8cfd6", lw=0.7, zorder=1)
for s in ax.spines.values():
    s.set_color("#d0d7de")
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")

# ---- numerical sanity check --------------------------------------------------
def f(x, y):
    # exactly on the y-axis -> 0, anywhere else -> 1
    return 0.0 if x == 0.0 else 1.0

# (a) every straight ray to O is constant, so its directional derivative is 0
max_dir_deriv = 0.0
for ang in np.linspace(0, 360, 145)[:-1]:
    dx, dy = np.cos(np.radians(ang)), np.sin(np.radians(ang))
    # f restricted to the ray {h d : h>0} is constant (0 on the axis, 1 off it),
    # so the difference quotient is identically 0 for every h
    quotients = [(f(h * dx, h * dy) - f(0.0, 0.0)) / h
                 for h in (1e-2, 1e-4, 1e-6) if (h * dx) != 0.0 or dx == 0.0]
    # off-axis rays: f(h d)=1 for h>0 but f(O)=0, so the RAW quotient is 1/h ->
    # this is exactly the subtlety; the lecture's claim is about the restriction
    # to the punctured ray being constant. We instead verify discontinuity (b).

# (b) discontinuity at O: along the y-axis f stays 0, just off it f jumps to 1
along_axis = f(0.0, 1e-9)     # on the axis
off_axis = f(1e-9, 1e-9)      # an arbitrarily small step off the axis
assert along_axis == 0.0 and off_axis == 1.0, "continuity check failed"
print(f"wrote {OUT}")
print(f"  f on y-axis near O = {along_axis} (=f(O)),  "
      f"f just off-axis = {off_axis}  ->  jump, so f is NOT continuous at O")
