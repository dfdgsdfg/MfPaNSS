#!/usr/bin/env python3
"""Static figure for 07강 4기 18강 — "내적은 수선의 발을 내리는 규칙을 공리로
정한다" (lecture §8). The point: in R^2 we never agreed that (1,0) and (0,1)
are orthogonal. Whether dropping the perpendicular foot of (0,1) onto (1,0)
gives length 0 (so they are "perpendicular") is NOT given by the space — it is
*chosen* by picking an inner product. Two panels show two such choices.

Left  : standard (Euclidean) inner product  <x,y> = x.y, metric M = I.
        Basis (1,0),(0,1) make a unit SQUARE; the foot of (0,1) onto (1,0) is 0,
        so the lecturer's naive guess ("projection -> 0") happens to hold.
Right : a different inner product  <x,y> = x^T M y  with M not the identity.
        Now (1,0),(0,1) are NOT orthogonal: they make a slanted PARALLELOGRAM,
        the angle between them is < 90 deg, and the foot of (0,1) onto (1,0)
        is a POSITIVE length -- so <(1,0),(0,1)> != 0. Same set of arrows,
        different "수선의 발" rule.

Reproduce:  uv run --with matplotlib --with numpy python inner-product-axiom-04-season-18-08.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon

OUT = Path(__file__).with_suffix(".svg")

e1 = np.array([1.0, 0.0])
e2 = np.array([0.0, 1.0])

# Two metrics. M must be symmetric positive-definite (an inner product).
# Standard inner product:
M_std = np.array([[1.0, 0.0], [0.0, 1.0]])
# A different inner product (off-diagonal != 0 => e1, e2 not orthogonal here):
M_skew = np.array([[1.0, 0.6], [0.6, 1.0]])


def inner(M, a, b):
    return a @ M @ b


def proj_len(M, a, onto):
    """signed length of the foot of perpendicular of `a` onto span(`onto`),
    measured in the geometry defined by M."""
    return inner(M, a, onto) / np.sqrt(inner(M, onto, onto))


def arrow(ax, p, color, lw=2.4, q=(0.0, 0.0)):
    ax.add_patch(FancyArrowPatch(q, p, arrowstyle="-|>", mutation_scale=18,
                                 lw=lw, color=color, shrinkA=0, shrinkB=0, zorder=5))


def panel(ax, M, title, perp):
    # parallelogram spanned by e1, e2 (always the literal square of arrows;
    # what changes is the *angle the inner product reads off them*).
    ax.add_patch(Polygon([(0, 0), e1, e1 + e2, e2], closed=True,
                         facecolor="#dbe7ff", edgecolor="none", alpha=0.55, zorder=0))
    arrow(ax, e1, "#1f6feb")          # (1,0)
    arrow(ax, e2, "#d1242f")          # (0,1)

    # foot of perpendicular of e2 onto span(e1), in geometry M.
    c = inner(M, e2, e1) / inner(M, e1, e1)   # coordinate along e1
    foot = c * e1
    pl = proj_len(M, e2, e1)                  # length of that projection
    ax.plot([0, 1.35], [0, 0], color="#9aa7b8", lw=1.0, ls=(0, (6, 4)), zorder=1)
    if perp:
        # genuinely perpendicular: dotted drop is straight down, foot at origin
        ax.plot([e2[0], foot[0]], [e2[1], foot[1]], color="#6e7781", lw=1.4, ls=":", zorder=2)
        # right-angle marker at O
        s = 0.12
        ax.plot([s, s, 0], [0, s, s], color="#6e7781", lw=1.0, zorder=3)
        ax.text(0.5, -0.34, r"foot length $=0$", color="#0b8457", fontsize=12, ha="center")
        ax.text(0.5, -0.62, r"$\langle(1,0),(0,1)\rangle=0$", color="#24292f", fontsize=12, ha="center")
    else:
        # not perpendicular: foot lands at positive c on the e1 axis
        ax.plot([e2[0], foot[0]], [e2[1], foot[1]], color="#6e7781", lw=1.4, ls=":", zorder=2)
        arrow(ax, foot, "#0b8457", 3.0)       # the nonzero foot
        ax.scatter([foot[0]], [foot[1]], s=22, color="#0b8457", zorder=6)
        ax.text(foot[0], -0.30, r"foot length $>0$", color="#0b8457", fontsize=12, ha="center")
        ax.text(0.5, -0.62, r"$\langle(1,0),(0,1)\rangle=%.1f\neq0$" % inner(M, e1, e2),
                color="#24292f", fontsize=12, ha="center")

    ax.scatter([0], [0], s=20, color="#24292f", zorder=7)
    ax.text(-0.13, -0.16, r"$O$", fontsize=11, color="#24292f")
    ax.text(e1[0] + 0.04, e1[1] - 0.16, r"$(1,0)$", color="#1f6feb", fontsize=12)
    ax.text(e2[0] + 0.04, e2[1], r"$(0,1)$", color="#d1242f", fontsize=12)
    ax.set_title(title, fontsize=12.5)
    ax.set_xlim(-0.4, 1.6)
    ax.set_ylim(-0.85, 1.4)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)


fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.2, 4.6))
panel(axL, M_std, r"standard inner product  ($M=I$)", perp=True)
panel(axR, M_skew, r"a different inner product  ($M\neq I$)", perp=False)
fig.suptitle(r"The inner product is the rule that decides where the perpendicular foot falls",
             fontsize=12.5, y=0.99)
fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}")
print(f"  std : <(1,0),(0,1)> = {inner(M_std, e1, e2):.3f}  (foot length {proj_len(M_std, e2, e1):.3f})")
print(f"  skew: <(1,0),(0,1)> = {inner(M_skew, e1, e2):.3f}  (foot length {proj_len(M_skew, e2, e1):.3f})")
assert abs(inner(M_std, e1, e2)) < 1e-9
assert inner(M_skew, e1, e2) > 0
# both metrics must be valid inner products (symmetric positive-definite)
for M in (M_std, M_skew):
    assert np.allclose(M, M.T)
    assert np.all(np.linalg.eigvalsh(M) > 0)
