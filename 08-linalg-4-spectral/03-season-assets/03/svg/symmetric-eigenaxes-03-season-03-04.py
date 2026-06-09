#!/usr/bin/env python3
"""Static figure for 08강 3기 03강 — a real symmetric matrix's eigenvectors are
orthogonal and are exactly the major/minor axes of the level ellipse
z^T A z = 1 (lecture §4, using the worked example A = [[3,1],[1,3]] of §8).

Reproduce:  uv run --with matplotlib --with numpy python symmetric-eigenaxes-03-season-03-04.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

OUT = Path(__file__).with_suffix(".svg")

# the note's worked example: A = [[3,1],[1,3]]  (§8)
A = np.array([[3.0, 1.0], [1.0, 3.0]])
evals, evecs = np.linalg.eigh(A)          # ascending: lambda=2 then lambda=4
# order as the note states them: lambda1=4 with (1,1), lambda2=2 with (-1,1)
idx = np.argsort(evals)[::-1]
evals, evecs = evals[idx], evecs[:, idx]
q1, q2 = evecs[:, 0], evecs[:, 1]         # orthonormal eigenvectors
l1, l2 = evals                            # 4, 2

# level set z^T A z = 1 is an ellipse; semi-axis length along q_i is 1/sqrt(lambda_i)
phi = np.linspace(0, 2 * np.pi, 400)
a, b = 1.0 / np.sqrt(l1), 1.0 / np.sqrt(l2)
ellipse = (a * np.cos(phi)[:, None] * q1 + b * np.sin(phi)[:, None] * q2)

# for contrast: the standard unit circle x^2 + y^2 = 1
circle = np.stack([np.cos(phi), np.sin(phi)], axis=1)

fig, ax = plt.subplots(figsize=(6.0, 5.6))


def arrow(p, color, lw=2.4, label=None, dx=0.0, dy=0.0):
    ax.add_patch(FancyArrowPatch((0, 0), p, arrowstyle="-|>", mutation_scale=18,
                                 lw=lw, color=color, shrinkA=0, shrinkB=0, zorder=6))
    if label:
        ax.text(p[0] + dx, p[1] + dy, label, color=color, fontsize=13, weight="bold")


# standard unit circle (faint, for reference)
ax.plot(circle[:, 0], circle[:, 1], color="#c9d1d9", lw=1.2, ls=(0, (5, 4)),
        zorder=1, label=r"$x^2+y^2=1$  (standard circle)")

# the inner-product unit circle z^T A z = 1  (looks like an ellipse here)
ax.plot(ellipse[:, 0], ellipse[:, 1], color="#1f6feb", lw=2.2, zorder=2,
        label=r"$z^{T}\!Az=1$  (ellipse in standard view)")

# principal axes = eigenvector directions, scaled to the ellipse's semi-axes
ax.plot([-a * q1[0], a * q1[0]], [-a * q1[1], a * q1[1]],
        color="#0b8457", lw=1.0, ls=":", zorder=3)
ax.plot([-b * q2[0], b * q2[0]], [-b * q2[1], b * q2[1]],
        color="#d1242f", lw=1.0, ls=":", zorder=3)

# eigenvector arrows reaching the ellipse along each axis
arrow(a * q1, "#0b8457", label=r"$q_1\ (\lambda=4)$", dx=0.04, dy=0.10)
arrow(b * q2, "#d1242f", label=r"$q_2\ (\lambda=2)$", dx=-0.62, dy=0.10)

# right-angle marker showing q1 ⊥ q2 at the origin
s = 0.10
corner = s * q1 + s * q2
ax.plot([s * q1[0], corner[0], s * q2[0]], [s * q1[1], corner[1], s * q2[1]],
        color="#57606a", lw=1.1, zorder=5)

ax.scatter([0], [0], s=20, color="#24292f", zorder=7)
ax.text(0.04, -0.13, r"$O$", fontsize=12, color="#24292f")

ax.set_title(r"Symmetric $A=(3,1;1,3)$: eigenvectors $\perp$,"
             "\n" r"and they are the axes of $z^{T}\!Az=1$",
             fontsize=12.5)
ax.set_aspect("equal")
ax.axhline(0, color="#e1e4e8", lw=0.8, zorder=0)
ax.axvline(0, color="#e1e4e8", lw=0.8, zorder=0)
ax.set_xlim(-1.05, 1.05)
ax.set_ylim(-1.05, 1.05)
ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1])
ax.tick_params(labelsize=9)
ax.legend(loc="lower right", fontsize=9, framealpha=0.9)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")

# sanity checks printed to confirm the math
ortho = float(q1 @ q2)
print(f"wrote {OUT}")
print(f"eigenvalues = {l1:.3f}, {l2:.3f}  (expect 4, 2)")
print(f"q1.q2 = {ortho:.2e}  (expect ~0, orthogonal)")
print(f"semi-axes: 1/sqrt(4)={a:.4f} along q1, 1/sqrt(2)={b:.4f} along q2")
# verify a sample point lies on z^T A z = 1
zp = a * q1
print(f"check z^T A z at q1-tip = {zp @ A @ zp:.4f}  (expect 1.0)")
