#!/usr/bin/env python3
"""Static figure for 08강 4기 20강 — the meaning of A = Q D Q^{-1} as a three-step
pipeline "rotate axes -> stretch along eigen-axes -> rotate back" (lecture §4).

Uses the note's example #3, A = [[3,1],[1,3]], whose eigenvectors lie on the +-45
diagonals (eigenvalues lambda1=4 along (1,1), lambda2=2 along (-1,1)). The unit
circle (left) is mapped by A to an ellipse (right) whose principal axes ARE the
eigen-axes, stretched by lambda1 and lambda2. Renders next to itself as an SVG.

Reproduce:
  uv run --with matplotlib --with numpy python spectral-rotate-stretch-04-season-20-04.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

OUT = Path(__file__).with_suffix(".svg")

A = np.array([[3.0, 1.0], [1.0, 3.0]])
w, V = np.linalg.eigh(A)                 # w = [2, 4]; columns of V are unit eigenvectors
# order so that index 0 -> larger eigenvalue (for nicer labels)
order = np.argsort(w)[::-1]
lam = w[order]                          # [4, 2]
E = V[:, order]                         # eigenvectors as columns, unit length
e1, e2 = E[:, 0], E[:, 1]               # e1 along (1,1)/sqrt2, e2 along (-1,1)/sqrt2

theta = np.linspace(0, 2 * np.pi, 400)
circle = np.vstack([np.cos(theta), np.sin(theta)])     # unit circle
ellipse = A @ circle                                   # A maps it to an ellipse

fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.8))


def style(ax, lim):
    ax.set_aspect("equal")
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.axhline(0, color="#d0d7de", lw=0.8, zorder=0)
    ax.axvline(0, color="#d0d7de", lw=0.8, zorder=0)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def arrow(ax, p, color, lw=2.4):
    ax.add_patch(FancyArrowPatch((0, 0), p, arrowstyle="-|>", mutation_scale=16,
                                 lw=lw, color=color, shrinkA=0, shrinkB=0, zorder=5))


# ---- left: unit circle + eigen-axes (the axes we "swap in" via Q^{-1}) ----
ax = axes[0]
ax.plot(circle[0], circle[1], color="#1f6feb", lw=2.0, zorder=3)
for e, c in ((e1, "#0b8457"), (e2, "#bf3989")):
    ax.plot([-e[0], e[0]], [-e[1], e[1]], color=c, lw=1.2, ls=(0, (6, 4)), zorder=2)
arrow(ax, e1, "#0b8457")
arrow(ax, e2, "#bf3989")
ax.text(e1[0] + 0.06, e1[1] + 0.05, r"$v_1$", color="#0b8457", fontsize=13, weight="bold")
ax.text(e2[0] - 0.34, e2[1] + 0.05, r"$v_2$", color="#bf3989", fontsize=13, weight="bold")
ax.set_title("unit circle  +  eigen-axes\n(swap in axes via " r"$Q^{-1}$)", fontsize=12)
style(ax, 4.4)

# ---- right: ellipse = A(circle); axes stretched by lambda1, lambda2 ----
ax = axes[1]
ax.plot(ellipse[0], ellipse[1], color="#d1242f", lw=2.0, zorder=3)
ax.plot(circle[0], circle[1], color="#9aa7b8", lw=1.0, ls=(0, (2, 3)), zorder=1)
p1, p2 = lam[0] * e1, lam[1] * e2
for e, c in ((e1, "#0b8457"), (e2, "#bf3989")):
    ax.plot([-lam[0] * e[0] * (e is e1) - lam[1] * e[0] * (e is e2),
             lam[0] * e[0] * (e is e1) + lam[1] * e[0] * (e is e2)],
            [-lam[0] * e[1] * (e is e1) - lam[1] * e[1] * (e is e2),
             lam[0] * e[1] * (e is e1) + lam[1] * e[1] * (e is e2)],
            color=c, lw=1.2, ls=(0, (6, 4)), zorder=2)
arrow(ax, p1, "#0b8457")
arrow(ax, p2, "#bf3989")
ax.text(p1[0] + 0.06, p1[1] + 0.12, r"$\lambda_1 v_1=4\,v_1$",
        color="#0b8457", fontsize=12, weight="bold")
ax.text(p2[0] - 1.9, p2[1] + 0.12, r"$\lambda_2 v_2=2\,v_2$",
        color="#bf3989", fontsize=12, weight="bold")
ax.set_title(r"ellipse $= A(\mathrm{circle})$" "\nstretch by " r"$\lambda_1,\lambda_2$  then rotate back ("
             r"$Q$)", fontsize=12)
style(ax, 4.4)

fig.suptitle(r"$A=QDQ^{-1}$,  $A=[[3,1],[1,3]]$:"
             r"  rotate $\to$ stretch ($\lambda_1=4,\ \lambda_2=2$) $\to$ rotate back",
             fontsize=13, y=1.02)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}  (lambda={lam}, e1={e1}, e2={e2})")
