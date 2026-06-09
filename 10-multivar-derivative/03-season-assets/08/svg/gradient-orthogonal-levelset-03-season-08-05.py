#!/usr/bin/env python3
"""Static figure for 10강 3기 8강 — gradient is orthogonal to the level set
(lecture §5). On the circle F(x,y)=x^2+y^2-1=0, the gradient grad F = (2x, 2y)
points radially outward (perpendicular to the curve), and the tangent direction
(dx, dy) satisfying F_x dx + F_y dy = 0 runs along the curve. Renders next to
itself as an SVG embedded by the note.

Reproduce:
  uv run --with matplotlib --with numpy python gradient-orthogonal-levelset-03-season-08-05.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

OUT = Path(__file__).with_suffix(".svg")

fig, ax = plt.subplots(figsize=(6.0, 5.6))

# ---- the level set F = x^2 + y^2 - 1 = 0 (a unit circle) -------------------
phi = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(phi), np.sin(phi), color="#1f6feb", lw=2.4, zorder=3)

# faint background level sets F = c for a few c (the contour family) ----------
for c in (-0.55, 0.8, 2.0):
    r = np.sqrt(1 + c)
    if np.isfinite(r):
        ax.plot(r * np.cos(phi), r * np.sin(phi),
                color="#c7d2e0", lw=1.0, ls=(0, (5, 4)), zorder=1)

# ---- point on the circle ---------------------------------------------------
a = np.deg2rad(52.0)
p = np.array([np.cos(a), np.sin(a)])         # point on F = 0

grad = np.array([2 * p[0], 2 * p[1]])        # grad F = (2x, 2y), radial
grad_hat = grad / np.linalg.norm(grad)
tang_hat = np.array([-grad_hat[1], grad_hat[0]])   # tangent: F_x dx + F_y dy = 0

g_end = p + 0.75 * grad_hat                    # gradient arrow tip
t1 = p + 0.78 * tang_hat                        # tangent arrow tips (both ways)
t2 = p - 0.78 * tang_hat


def arrow(start, end, color, lw=2.4, scale=18):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=scale,
                                 lw=lw, color=color, shrinkA=0, shrinkB=0, zorder=6))


# gradient (normal) and tangent direction (both senses)
arrow(p, g_end, "#d1242f")                     # grad F : normal to the level set
arrow(p, t1, "#0b8457")                         # tangent direction (dx, dy)
arrow(p, t2, "#0b8457")

# right-angle marker between gradient and tangent at p -----------------------
s = 0.16
sq = np.array([p + s * tang_hat,
               p + s * tang_hat + s * grad_hat,
               p + s * grad_hat,
               p])
ax.plot(sq[:, 0], sq[:, 1], color="#57606a", lw=1.1, zorder=5)

# ---- labels ----------------------------------------------------------------
ax.scatter(*p, s=34, color="#24292f", zorder=7)
ax.text(p[0] + 0.06, p[1] + 0.05, r"$(x,y)$", fontsize=12, color="#24292f")

ax.text(g_end[0] + 0.03, g_end[1] + 0.04,
        r"$\nabla F=(F_x,F_y)$", color="#d1242f", fontsize=12.5, weight="bold")
ax.text(t1[0] + 0.04, t1[1] - 0.02,
        r"$(dx,dy)$", color="#0b8457", fontsize=12.5, weight="bold")

ax.text(0.30, 1.18, r"$F=x^2+y^2-1=0$", color="#1f6feb", fontsize=12.5)
ax.text(-1.86, -1.62,
        r"$\langle\nabla F,\,(dx,dy)\rangle = F_x\,dx + F_y\,dy = 0$",
        fontsize=13, color="#24292f")

# ---- axes cosmetics --------------------------------------------------------
ax.scatter([0], [0], s=16, color="#6e7781", zorder=4)
ax.set_xlim(-1.85, 1.95)
ax.set_ylim(-1.75, 1.6)
ax.set_aspect("equal")
ax.axhline(0, color="#d0d7de", lw=0.8, zorder=0)
ax.axvline(0, color="#d0d7de", lw=0.8, zorder=0)
ax.set_xticks([]); ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_visible(False)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")

dot = float(grad @ tang_hat)
print(f"wrote {OUT}  (grad.tangent = {dot:.2e}  ->  orthogonal)")
