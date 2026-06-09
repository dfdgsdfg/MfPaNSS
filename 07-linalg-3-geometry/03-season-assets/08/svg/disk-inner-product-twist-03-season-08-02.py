#!/usr/bin/env python3
"""Static figure for 07강 3기 8강 — "디스크의 반지름은 정말 1인가" (lecture §2).

The "unit ball" {v : <v,v> <= 1} is drawn for two different inner products on the
SAME set R^2.  With the standard inner product (dot product, metric M = I) it is the
ordinary circle.  With a twisted inner product that declares ||(1,0)|| = 2 and
||(0,1)|| = 1 (metric M = diag(4, 1)) the very same "disk" is a squashed ellipse.
Same points, same vectors — only the choice of inner product changed.

Reproduce:  uv run --with matplotlib --with numpy python disk-inner-product-twist-03-season-08-02.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).with_suffix(".svg")

# Unit ball of an inner product with metric M = diag(a^2, b^2):
#   <v,v> = a^2 x^2 + b^2 y^2 <= 1   <=>   (x/(1/a))^2 + (y/(1/b))^2 <= 1
# so the ball is an ellipse with semi-axes (1/a, 1/b).
t = np.linspace(0, 2 * np.pi, 400)

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(9.6, 4.9))

BLUE, RED, GREY, INK = "#1f6feb", "#d1242f", "#9aa7b8", "#24292f"


def setup(ax, title):
    ax.set_aspect("equal")
    ax.axhline(0, color="#d0d7de", lw=0.9, zorder=0)
    ax.axvline(0, color="#d0d7de", lw=0.9, zorder=0)
    ax.set_xlim(-1.35, 2.45)
    ax.set_ylim(-1.45, 1.55)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(title, fontsize=13, color=INK)
    ax.scatter([0], [0], s=16, color=INK, zorder=6)


def arrow(ax, p, color):
    ax.annotate("", xy=p, xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.2,
                                mutation_scale=16, shrinkA=0, shrinkB=0), zorder=5)


# ---- left: standard inner product, M = I  -> the disk is a circle ----
a, b = 1.0, 1.0
ax0_x, ax0_y = (1 / a) * np.cos(t), (1 / b) * np.sin(t)
setup(ax0, r"standard inner product   $M=I$")
ax0.fill(ax0_x, ax0_y, color=BLUE, alpha=0.12, zorder=1)
ax0.plot(ax0_x, ax0_y, color=BLUE, lw=2.0, zorder=2)
arrow(ax0, (1, 0), RED)
arrow(ax0, (0, 1), "#0b8457")
ax0.text(1.02, -0.22, r"$(1,0)$", color=RED, fontsize=12)
ax0.text(0.06, 1.06, r"$(0,1)$", color="#0b8457", fontsize=12)
ax0.text(-1.25, 1.28, r"$\|(1,0)\|=\|(0,1)\|=1$", color=INK, fontsize=11)
ax0.text(0.40, -1.30, r"$\{v:\langle v,v\rangle\leq 1\}=$ circle", color=BLUE, fontsize=11)

# ---- right: twisted inner product, M = diag(4,1) -> ||(1,0)||=2 -> squashed ellipse ----
a, b = 2.0, 1.0
ax1_x, ax1_y = (1 / a) * np.cos(t), (1 / b) * np.sin(t)
setup(ax1, r"twisted inner product   $M=\mathrm{diag}(4,1)$")
ax1.fill(ax1_x, ax1_y, color=RED, alpha=0.12, zorder=1)
ax1.plot(ax1_x, ax1_y, color=RED, lw=2.0, zorder=2)
arrow(ax1, (1, 0), RED)
arrow(ax1, (0, 1), "#0b8457")
ax1.text(1.02, -0.22, r"$(1,0)$", color=RED, fontsize=12)
ax1.text(0.06, 1.06, r"$(0,1)$", color="#0b8457", fontsize=12)
ax1.text(-1.25, 1.28, r"$\|(1,0)\|=2,\ \ \|(0,1)\|=1$", color=INK, fontsize=11)
ax1.text(0.30, -1.30, r"same set, now a squashed ellipse", color=RED, fontsize=11)

fig.suptitle(r"the same disk $\mathbb{R}^2$ — its 'radius 1' depends on the inner product",
             fontsize=13.5, color=INK, y=1.0)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")

# sanity check: (1,0) has norm sqrt(M[0,0]) under each metric
for label, M in (("M=I", np.diag([1, 1])), ("M=diag(4,1)", np.diag([4, 1]))):
    e1 = np.array([1.0, 0.0])
    n = np.sqrt(e1 @ M @ e1)
    print(f"{label}: ||(1,0)|| = {n:.2f}")
print(f"wrote {OUT}")
