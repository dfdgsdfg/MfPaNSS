#!/usr/bin/env python3
"""Static figure for 07강 4기 19강 — the inner product as "orthogonal projection
× two magnitudes" (lecture §8). Renders next to itself as an SVG embedded by the note.

Reproduce:  uv run --with matplotlib --with numpy python 19-inner-product-projection.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyArrowPatch

OUT = Path(__file__).with_suffix(".svg")

u = np.array([3.2, 0.9])
v = np.array([1.3, 2.5])
proj = (u @ v) / (u @ u) * u          # foot of perpendicular of v onto span(u)
ulen, vlen = np.linalg.norm(u), np.linalg.norm(v)
cos = (u @ v) / (ulen * vlen)
theta = np.degrees(np.arctan2(*u[::-1])), np.degrees(np.arctan2(*v[::-1]))

fig, ax = plt.subplots(figsize=(6.2, 5.0))


def arrow(p, color, lw=2.2):
    ax.add_patch(FancyArrowPatch((0, 0), p, arrowstyle="-|>", mutation_scale=18,
                                 lw=lw, color=color, shrinkA=0, shrinkB=0, zorder=5))


# span(u) line, the two vectors, the projection drop
t = np.linspace(-0.2, 1.25, 2)
ax.plot(t * u[0], t * u[1], color="#9aa7b8", lw=1.0, ls=(0, (6, 4)), zorder=1)
arrow(u, "#1f6feb")          # u
arrow(v, "#d1242f")          # v
arrow(proj, "#0b8457", 2.6)  # proj_u v (the part of v along u)
ax.plot([v[0], proj[0]], [v[1], proj[1]], color="#6e7781", lw=1.4, ls=":", zorder=2)

# right-angle marker at the foot
d1 = (u / ulen) * 0.18
d2 = ((v - proj) / np.linalg.norm(v - proj)) * 0.18
sq = np.array([proj + d1, proj + d1 + d2, proj + d2, proj])
ax.plot(sq[:, 0], sq[:, 1], color="#6e7781", lw=1.0, zorder=3)

# angle arc between u and v
ax.add_patch(Arc((0, 0), 1.4, 1.4, angle=0, theta1=theta[0], theta2=theta[1],
                 color="#57606a", lw=1.3))
ax.text(0.95, 0.55, r"$\theta$", color="#57606a", fontsize=14)

# labels
ax.text(u[0] + 0.06, u[1] - 0.18, r"$u$", color="#1f6feb", fontsize=15, weight="bold")
ax.text(v[0] + 0.08, v[1], r"$v$", color="#d1242f", fontsize=15, weight="bold")
ax.text(proj[0] - 0.15, proj[1] - 0.34, r"$\mathrm{proj}_u\,v$", color="#0b8457", fontsize=12)

ax.text(0.05, -0.62,
        r"$\langle u,v\rangle \;=\; \|u\|\,\|v\|\cos\theta \;=\; \|u\|\cdot(\|v\|\cos\theta)$"
        "\n" r"$=$ (length of $u$) $\times$ (projection of $v$ onto $u$)",
        fontsize=12.5, color="#24292f")

ax.scatter([0], [0], s=18, color="#24292f", zorder=6)
ax.text(-0.28, -0.16, r"$O$", fontsize=12, color="#24292f")
ax.set_xlim(-0.7, 3.9)
ax.set_ylim(-0.95, 3.0)
ax.set_aspect("equal")
ax.axhline(0, color="#d0d7de", lw=0.8, zorder=0)
ax.axvline(0, color="#d0d7de", lw=0.8, zorder=0)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}  (⟨u,v⟩={u @ v:.2f}, ‖u‖={ulen:.2f}, ‖v‖={vlen:.2f}, cosθ={cos:.3f})")
