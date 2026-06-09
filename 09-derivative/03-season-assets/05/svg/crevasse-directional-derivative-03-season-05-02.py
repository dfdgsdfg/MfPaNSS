#!/usr/bin/env python3
"""Static figure for 09강 3기 5강 — the "crevasse" counterexample (lecture §2).

Top-down view of a function on R^2 that is 1 everywhere except inside a thin
slit pinched between the x-axis and the parabola y = x^2, where it is 0. Any
STRAIGHT line through the origin escapes the slit immediately (so every
directional derivative is 0, making the directional-derivative "definition"
think f is smooth) yet a CURVE can stay inside the slit and reach the origin
through f = 0 values — so f is discontinuous at O. This is exactly why the
line-definition fails and the disk-shrinking definition (§6) is needed.
Renders next to itself as an SVG.

Reproduce:  uv run --with matplotlib --with numpy python crevasse-directional-derivative-03-season-05-02.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

OUT = Path(__file__).with_suffix(".svg")

# The slit region: 0 < y < x^2  (pinched between the x-axis and the parabola).
# f = 0 inside the slit, f = 1 outside. A line y = m x through O has, for small
# x>0, m x > x^2 (when m>0) so it sits ABOVE the parabola, outside the slit;
# the x-axis (y=0) is the slit's lower boundary, also outside. So along EVERY
# straight line f = 1 near O. A parabola y = x^2/2 stays strictly inside.
def f(x, y):
    inside = (x > 0) & (y > 0) & (y < x**2)
    return np.where(inside, 0.0, 1.0)


xs = np.linspace(-0.9, 1.5, 900)
ys = np.linspace(-0.7, 1.0, 700)
X, Y = np.meshgrid(xs, ys)
Z = f(X, Y)

fig, ax = plt.subplots(figsize=(6.6, 4.7))

# floor (f = 1) vs slit (f = 0):  green = slit, light = floor
ax.contourf(X, Y, Z, levels=[-0.5, 0.5, 1.5],
            colors=["#0b8457", "#dbe7df"])

# slit boundary: parabola y = x^2 (upper) and the x-axis (lower), for x >= 0
xc = np.linspace(0, 1.22, 400)
ax.plot(xc, xc**2, color="#0b8457", lw=1.6)
ax.plot([0, 1.5], [0, 0], color="#0b8457", lw=1.6)

# straight lines through O (fixed directions D): all escape the slit -> f = 1 near O.
# slopes m>0 sit above the parabola near O; m<=0 sit on/below the x-axis.
for m in (1.4, 0.55, -0.35):
    xl = np.array([-0.9, 1.5])
    ax.plot(xl, m * xl, color="#1f6feb", lw=1.3, ls=(0, (6, 4)), zorder=3)

# a CURVE that stays inside the slit (y = 0.5 x^2) and reaches O through f = 0
xk = np.linspace(0, 1.18, 200)
ax.plot(xk, 0.5 * xk**2, color="#d1242f", lw=2.6, zorder=4)
ax.add_patch(FancyArrowPatch((xk[110], 0.5 * xk[110]**2), (xk[55], 0.5 * xk[55]**2),
                             arrowstyle="-|>", mutation_scale=16, color="#d1242f",
                             lw=2.6, shrinkA=0, shrinkB=0, zorder=4))

# origin + the ant standing there
ax.scatter([0], [0], s=42, color="#24292f", zorder=6)
ax.text(-0.13, -0.10, r"$O$", fontsize=13, color="#24292f", zorder=6)

# labels (ASCII / math only — matplotlib has no Korean glyph)
ax.text(0.84, 0.86, r"straight lines $hD$" "\n" r"escape: $f\equiv 1$ near $O$",
        color="#1f6feb", fontsize=10.5, ha="left", va="center")
ax.text(0.50, 0.50, r"curve stays in slit:" "\n" r"$f\equiv 0\to$ discontinuous at $O$",
        color="#d1242f", fontsize=10.5, ha="left", va="center")
ax.text(0.74, 0.16, r"$f=0$", color="#eaf3ee", fontsize=12, ha="center",
        va="center", zorder=5)
ax.text(-0.55, 0.65, r"$f=1$", color="#3a6b53", fontsize=12)
ax.text(0.10, -0.30, r"slit: $\{\,0<y<x^2\,\}$", color="#0b8457", fontsize=10.5)

ax.set_xlim(-0.9, 1.5)
ax.set_ylim(-0.7, 1.0)
ax.set_aspect("equal")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_title(r"Crevasse function: lines miss the slit, a curve dives in",
             fontsize=12)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}")

# sanity checks: slit is 0 < y < x^2
print("f(0.1, 0)    =", float(f(np.array(0.1), np.array(0.0))),   "(on x-axis, boundary -> 1)")
print("f(0.1, 0.005)=", float(f(np.array(0.1), np.array(0.005))), "(inside slit 0<0.005<0.01 -> 0)")
print("f(0.1, 0.05) =", float(f(np.array(0.1), np.array(0.05))),  "(above parabola -> 1)")
# along y = m x: for m>0, m x > x^2 once x < m, so f = 1 near O for every direction.
for m in (0.55, -0.35, 1.4):
    x_small = 0.001
    print(f"  line m={m:>5}: f(x={x_small}) =",
          float(f(np.array(x_small), np.array(m * x_small))), "(near O -> 1)")
# along the inside curve y = x^2/2: 0 < x^2/2 < x^2, so f = 0 all the way to O.
for x_small in (0.5, 0.05, 0.005):
    print(f"  curve y=x^2/2 at x={x_small}: f =",
          float(f(np.array(x_small), np.array(x_small**2 / 2))), "(in slit -> 0)")
