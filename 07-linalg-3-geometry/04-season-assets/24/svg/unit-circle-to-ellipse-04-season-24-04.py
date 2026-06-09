#!/usr/bin/env python3
"""Static figure for 07강 4기 24강 — "내적을 도입하면 단위원이 타원이 된다" (lecture §4).

An inner product on R^2 is a symmetric positive-definite 2x2 matrix M; its unit
ball  { v : v^T M v = 1 }  is the set of vectors of length 1.  Three choices of M
give three pictures, exactly as described in the note:
  (1) M = I (standard / Euclidean): e1=(1,0), e2=(0,1) both length 1, orthogonal
        -> the UNIT CIRCLE.
  (2) M = diag(1/2, 1/3): the two axis vectors are stretched to lengths sqrt(2),
        sqrt(3) while staying orthogonal  -> an axis-aligned ELLIPSE.
  (3) a non-diagonal SPD M: the basis vectors are no longer orthogonal
        -> a TILTED ELLIPSE.

All in-figure text is ASCII/English (matplotlib default font has no Korean glyphs).

Reproduce:
  uv run --with matplotlib --with numpy python unit-circle-to-ellipse-04-season-24-04.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

OUT = Path(__file__).with_suffix(".svg")

# unit circle parameterization in the standard plane
t = np.linspace(0, 2 * np.pi, 400)
circle = np.vstack([np.cos(t), np.sin(t)])


def unit_ball(M):
    """Return points v with v^T M v = 1, drawn as L^{-1} applied to the unit circle
    where M = L L^T (Cholesky).  These are the length-1 vectors of the inner product M."""
    L = np.linalg.cholesky(M)
    return np.linalg.solve(L.T, circle)


# the three inner products (SPD matrices)
I = np.array([[1.0, 0.0], [0.0, 1.0]])                  # standard -> unit circle
D = np.array([[1.0 / 2.0, 0.0], [0.0, 1.0 / 3.0]])      # ||e1||=sqrt2, ||e2||=sqrt3
T = np.array([[0.5, 0.28], [0.28, 0.34]])               # off-diagonal -> tilted ellipse

panels = [
    (I, "M = I  (standard)", "unit circle\n||e1||=||e2||=1,  e1 _|_ e2", "#1f6feb"),
    (D, r"M = diag(1/2, 1/3)", "ellipse\n||e1||=sqrt2, ||e2||=sqrt3,  e1 _|_ e2", "#0b8457"),
    (T, "M off-diagonal (SPD)", "tilted ellipse\ne1, e2 not orthogonal", "#d1242f"),
]

fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.1))

for ax, (M, title, sub, col) in zip(axes, panels):
    pts = unit_ball(M)
    ax.fill(pts[0], pts[1], color=col, alpha=0.10, zorder=1)
    ax.plot(pts[0], pts[1], color=col, lw=2.3, zorder=4)

    # the two basis vectors e1, e2 *rescaled to length 1 under this inner product*,
    # i.e. they touch the unit ball -> show how the frame deforms.
    # length-1 vector along a coordinate axis e_i: v = e_i / sqrt(M_ii)
    e1 = np.array([1.0, 0.0]) / np.sqrt(M[0, 0])
    e2 = np.array([0.0, 1.0]) / np.sqrt(M[1, 1])
    for v, lbl in ((e1, "e1"), (e2, "e2")):
        ax.add_patch(FancyArrowPatch((0, 0), v, arrowstyle="-|>", mutation_scale=14,
                                     lw=2.0, color="#57606a", shrinkA=0, shrinkB=0, zorder=5))
        ax.annotate(lbl, xy=v, xytext=(v[0] * 1.12 + 0.05, v[1] * 1.12 + 0.05),
                    color="#24292f", fontsize=11)

    ax.scatter([0], [0], s=14, color="#24292f", zorder=6)
    ax.set_title(title, fontsize=12, pad=10)
    ax.text(0.5, -0.20, sub, transform=ax.transAxes, ha="center", va="top",
            fontsize=9.5, color="#57606a")
    ax.set_xlim(-2.1, 2.1)
    ax.set_ylim(-2.1, 2.1)
    ax.set_aspect("equal")
    ax.axhline(0, color="#d0d7de", lw=0.8, zorder=0)
    ax.axvline(0, color="#d0d7de", lw=0.8, zorder=0)
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_yticks([-2, -1, 0, 1, 2])
    ax.tick_params(labelsize=7, colors="#8b949e")
    for s in ax.spines.values():
        s.set_visible(False)

fig.suptitle(r"Unit ball  $\{\,v : v^{\top} M\, v = 1\,\}$  of the inner product  $M$",
             fontsize=13, y=1.0)
fig.tight_layout(rect=(0, 0.02, 1, 0.97))
fig.savefig(OUT, format="svg", bbox_inches="tight")

# sanity check: report axis-vector lengths under each M
for M, title, *_ in panels:
    l1 = np.sqrt(np.array([1, 0]) @ M @ np.array([1, 0]))
    l2 = np.sqrt(np.array([0, 1]) @ M @ np.array([0, 1]))
    ip = np.array([1, 0]) @ M @ np.array([0, 1])
    print(f"{title:24s}  ||e1||_M={l1:.3f}  ||e2||_M={l2:.3f}  <e1,e2>_M={ip:+.3f}")
print(f"wrote {OUT}")
