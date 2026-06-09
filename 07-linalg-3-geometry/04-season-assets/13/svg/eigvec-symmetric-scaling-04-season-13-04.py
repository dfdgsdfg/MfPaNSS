#!/usr/bin/env python3
"""Static figure for 07강 4기 13강 — the symmetric matrix A = [[3,1],[1,3]]
acts on its two orthogonal eigenvectors by simple scaling (lecture §4).

Eigenvalues 2 and 4 with eigenvectors (1,-1) and (1,1): A only stretches
each eigen-direction by its eigenvalue, leaving the direction unchanged.
Renders next to itself as an SVG embedded by the note.

Reproduce:
  uv run --with matplotlib --with numpy python eigvec-symmetric-scaling-04-season-13-04.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

OUT = Path(__file__).with_suffix(".svg")

A = np.array([[3.0, 1.0], [1.0, 3.0]])

# eigen-pairs (verified): lambda=2 -> (1,-1), lambda=4 -> (1,1)
v2 = np.array([1.0, -1.0])
v4 = np.array([1.0, 1.0])
lam2, lam4 = 2.0, 4.0

# unit eigenvectors and their images under A (= lambda * unit eigenvector)
u2 = v2 / np.linalg.norm(v2)
u4 = v4 / np.linalg.norm(v4)
Au2 = A @ u2
Au4 = A @ u4
assert np.allclose(Au2, lam2 * u2) and np.allclose(Au4, lam4 * u4)

fig, ax = plt.subplots(figsize=(6.2, 5.6))


def arrow(p0, p1, color, lw=2.4, ls="-", scale=18, z=5):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=scale,
                                 lw=lw, color=color, ls=ls, shrinkA=0, shrinkB=0,
                                 zorder=z))


# eigen-axes (the parallelogram basis the matrix prefers), drawn faintly
for u, col in [(u2, "#0b8457"), (u4, "#1f6feb")]:
    t = np.linspace(-3.2, 3.2, 2)
    ax.plot(t * u[0], t * u[1], color=col, lw=0.9, ls=(0, (6, 4)),
            alpha=0.45, zorder=1)

# image arrows A v (long), then the unit eigenvectors v on top (short)
arrow((0, 0), Au4, "#1f6feb", lw=2.6)           # A on lambda=4 direction
arrow((0, 0), Au2, "#0b8457", lw=2.6)           # A on lambda=2 direction
arrow((0, 0), u4, "#0b3d91", lw=2.0)            # eigenvector v4 (unit)
arrow((0, 0), u2, "#06603d", lw=2.0)            # eigenvector v2 (unit)

# right-angle marker at origin between the two orthogonal eigenvectors
d1 = u2 * 0.28
d2 = u4 * 0.28
sq = np.array([d1, d1 + d2, d2])
ax.plot(sq[:, 0], sq[:, 1], color="#6e7781", lw=1.0, zorder=4)

# labels
ax.text(u4[0] + 0.08, u4[1] + 0.02, r"$v_2=(1,\,1)$",
        color="#0b3d91", fontsize=13)
ax.text(Au4[0] + 0.10, Au4[1] - 0.05, r"$A v_2 = 4\,v_2$",
        color="#1f6feb", fontsize=13, weight="bold")
ax.text(u2[0] + 0.10, u2[1] - 0.05, r"$v_1=(1,\,-1)$",
        color="#06603d", fontsize=13)
ax.text(Au2[0] + 0.12, Au2[1] - 0.18, r"$A v_1 = 2\,v_1$",
        color="#0b8457", fontsize=13, weight="bold")

ax.text(-3.5, 3.35,
        r"$A=[[3,1],[1,3]]$:  eigen-directions are only scaled"
        "\n" r"$\lambda_1=2$ along $(1,-1)$,   $\lambda_2=4$ along $(1,1)$  (orthogonal)",
        fontsize=12, color="#24292f")

ax.scatter([0], [0], s=20, color="#24292f", zorder=6)
ax.text(0.10, -0.30, r"$O$", fontsize=12, color="#24292f")

ax.set_xlim(-3.7, 3.7)
ax.set_ylim(-3.4, 3.9)
ax.set_aspect("equal")
ax.axhline(0, color="#d0d7de", lw=0.8, zorder=0)
ax.axvline(0, color="#d0d7de", lw=0.8, zorder=0)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}")
print(f"  lambda=2 eigvec (1,-1): A@u = {Au2}, 2*u = {lam2*u2}")
print(f"  lambda=4 eigvec (1, 1): A@u = {Au4}, 4*u = {lam4*u4}")
print(f"  orthogonal? u1.u2 = {u2 @ u4:.3f}")
