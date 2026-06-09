#!/usr/bin/env python3
"""Static figure for 06강 4기 17강 §9 — "same vectors, different inner product,
different size". A diagonal inner product M = diag(a, b) reads the SAME standard
basis e1=(1,0), e2=(0,1) with DIFFERENT magnitudes (sqrt(a), sqrt(b)) while they
stay orthogonal; its unit set {v : <v,v> = 1} is an ellipse with semi-axes
1/sqrt(a), 1/sqrt(b). Renders next to itself as an SVG embedded by the note.

Reproduce:
  uv run --with matplotlib --with numpy python inner-product-magnitude-04-season-17-09.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

OUT = Path(__file__).with_suffix(".svg")

e1 = np.array([1.0, 0.0])
e2 = np.array([0.0, 1.0])


def size(M, v):
    return float(np.sqrt(v @ M @ v))


fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.8))


def arrow(ax, p, color, lw=2.4):
    ax.add_patch(FancyArrowPatch((0, 0), p, arrowstyle="-|>", mutation_scale=16,
                                 lw=lw, color=color, shrinkA=0, shrinkB=0, zorder=5))


def panel(ax, M, title):
    a, b = M[0, 0], M[1, 1]
    # unit set of the inner product: x^2 * a + y^2 * b = 1  -> ellipse
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(th) / np.sqrt(a), np.sin(th) / np.sqrt(b),
            color="#8250df", lw=1.6, zorder=2,
            label=r"$\langle v,v\rangle=1$")
    # the two standard basis vectors (same in every panel)
    arrow(ax, e1, "#1f6feb")
    arrow(ax, e2, "#d1242f")
    s1, s2 = size(M, e1), size(M, e2)
    ax.text(e1[0] + 0.05, e1[1] + 0.07, r"$e_1$", color="#1f6feb",
            fontsize=13, weight="bold")
    ax.text(e2[0] + 0.07, e2[1] + 0.02, r"$e_2$", color="#d1242f",
            fontsize=13, weight="bold")
    ax.text(e1[0] + 0.04, e1[1] - 0.20, rf"$\|e_1\|={s1:.3f}$",
            color="#1f6feb", fontsize=11)
    ax.text(e2[0] - 0.05, e2[1] + 0.16, rf"$\|e_2\|={s2:.3f}$",
            color="#d1242f", fontsize=11)
    # right-angle marker: e1, e2 stay orthogonal under any diagonal M
    r = 0.12
    ax.plot([r, r, 0], [0, r, r], color="#57606a", lw=1.0, zorder=4)
    ax.scatter([0], [0], s=16, color="#24292f", zorder=6)
    ax.set_title(title, fontsize=13)
    ax.set_xlim(-1.4, 1.7)
    ax.set_ylim(-1.4, 1.7)
    ax.set_aspect("equal")
    ax.axhline(0, color="#d0d7de", lw=0.8, zorder=0)
    ax.axvline(0, color="#d0d7de", lw=0.8, zorder=0)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.tick_params(labelsize=9)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.legend(loc="upper right", fontsize=10, frameon=False)


panel(axes[0], np.diag([3.0, 2.0]),
      r"$M=\mathrm{diag}(3,2)$:  $\|e_1\|=\sqrt{3},\ \|e_2\|=\sqrt{2}$")
panel(axes[1], np.diag([2.0, 3.0]),
      r"$M=\mathrm{diag}(2,3)$:  $\|e_1\|=\sqrt{2},\ \|e_2\|=\sqrt{3}$")

fig.suptitle(
    r"Same vectors $e_1,e_2$ (still orthogonal) — different inner product, "
    r"different size",
    fontsize=12.5, y=0.99)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}")
for M in (np.diag([3.0, 2.0]), np.diag([2.0, 3.0])):
    print(f"  M=diag({int(M[0,0])},{int(M[1,1])}): "
          f"|e1|={size(M, e1):.4f}, |e2|={size(M, e2):.4f}")
