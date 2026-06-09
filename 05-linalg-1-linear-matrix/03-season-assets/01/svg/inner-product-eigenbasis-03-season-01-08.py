#!/usr/bin/env python3
"""Static figure for 05강 3기 01강 — the inner product matrix A = [[3,1],[1,3]]
reshapes the geometry of R^2 (lecture §2, §6, §8).

Two panels:
  (left)  the standard basis e1=(1,0), e2=(0,1): in this inner product each has
          length sqrt(3) and they meet at ~70.5 deg (NOT a right angle), so the
          set x^2+y^2=1 looks like a tilted ellipse, and the *unit ball* of the
          new inner product (<v,v>=1) is an ellipse whose axes are the eigenvectors.
  (right) the eigenvectors v1=(1,1), v2=(1,-1): they ARE orthogonal in the new
          inner product (<v1,v2>=0) -> the "good basis" that restores an
          orthogonal x/y-axis picture.

Reproduce: uv run --with matplotlib --with numpy python inner-product-eigenbasis-03-season-01-08.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyArrowPatch

OUT = Path(__file__).with_suffix(".svg")

A = np.array([[3.0, 1.0], [1.0, 3.0]])


def anorm(p):
    return float(np.sqrt(p @ A @ p))


def adot(p, q):
    return float(p @ A @ q)


def angle_between(p, q):
    return np.degrees(np.arccos(adot(p, q) / (anorm(p) * anorm(q))))


def arrow(ax, p, color, lw=2.3, scale=18):
    ax.add_patch(FancyArrowPatch((0, 0), p, arrowstyle="-|>", mutation_scale=scale,
                                 lw=lw, color=color, shrinkA=0, shrinkB=0, zorder=6))


# unit ball of the new inner product: { v : <v,v> = 1 }.
# v = r(theta)*(cos,sin) with r = 1/sqrt(<dir,dir>_A)
th = np.linspace(0, 2 * np.pi, 400)
dirs = np.stack([np.cos(th), np.sin(th)])
rad = 1.0 / np.sqrt(np.einsum("it,ij,jt->t", dirs, A, dirs))
ball = dirs * rad  # 2 x 400, the ellipse <v,v>=1

fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.2, 5.4))

GRID = "#d0d7de"
INK = "#24292f"


def frame(ax, lim=2.4):
    ax.axhline(0, color=GRID, lw=0.8, zorder=0)
    ax.axvline(0, color=GRID, lw=0.8, zorder=0)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.scatter([0], [0], s=16, color=INK, zorder=7)


# ---------------- LEFT: standard basis is NOT orthogonal here ----------------
frame(axL)
axL.plot(ball[0], ball[1], color="#d1242f", lw=2.0, zorder=4)
axL.text(1.15, 1.12, r"$\langle v,v\rangle=1$", color="#d1242f", fontsize=12)

e1 = np.array([1.0, 0.0]); e2 = np.array([0.0, 1.0])
arrow(axL, e1, "#1f6feb")
arrow(axL, e2, "#1f6feb")
axL.text(e1[0] + 0.08, e1[1] - 0.22, r"$e_1=(1,0)$", color="#1f6feb", fontsize=12)
axL.text(e2[0] - 0.34, e2[1] + 0.12, r"$e_2=(0,1)$", color="#1f6feb", fontsize=12)

# angle arc between e1 and e2 (Euclidean drawing, but labelled with new-IP angle)
ang = angle_between(e1, e2)
axL.add_patch(Arc((0, 0), 0.7, 0.7, angle=0, theta1=0, theta2=90, color="#57606a", lw=1.3))
axL.text(0.30, 0.30, r"$70.5^\circ$", color="#57606a", fontsize=11)

axL.set_title(r"standard basis under $A=[[3,1],[1,3]]$"
              "\n"
              r"$\|e_1\|=\|e_2\|=\sqrt{3},\ \ \cos\theta=\frac{1}{3}\ (\theta\approx70.5^\circ)$",
              fontsize=12, color=INK)

# ---------------- RIGHT: eigenvectors are orthogonal in the new inner product --
frame(axR)
axR.plot(ball[0], ball[1], color="#d1242f", lw=1.6, alpha=0.45, zorder=4)

v1 = np.array([1.0, 1.0]); v2 = np.array([1.0, -1.0])
# draw eigen-axes lines through origin
for vec, col in [(v1, "#0b8457"), (v2, "#8250df")]:
    s = np.linspace(-1.0, 1.0, 2)
    axR.plot(s * vec[0] * 1.7, s * vec[1] * 1.7, color=col, lw=1.0,
             ls=(0, (6, 4)), zorder=1)
arrow(axR, v1, "#0b8457")
arrow(axR, v2, "#8250df")
axR.text(v1[0] + 0.05, v1[1] + 0.08, r"$v_1=(1,1),\ \lambda=4$", color="#0b8457", fontsize=11)
axR.text(v2[0] + 0.05, v2[1] - 0.20, r"$v_2=(1,-1),\ \lambda=2$", color="#8250df", fontsize=11)

# right-angle marker AT origin between v1 and v2 (they are A-orthogonal;
# here they also happen to be Euclidean-perpendicular, so the square is honest)
u1 = v1 / np.linalg.norm(v1) * 0.26
u2 = v2 / np.linalg.norm(v2) * 0.26
sq = np.array([u1, u1 + u2, u2])
axR.plot(sq[:, 0], sq[:, 1], color="#57606a", lw=1.1, zorder=5)
axR.text(0.34, 0.02, r"$\langle v_1,v_2\rangle=0$", color="#57606a", fontsize=11)

axR.set_title(r"eigenvectors = the good (orthogonal) basis"
              "\n"
              r"$\langle v_1,v_1\rangle=8,\ \langle v_2,v_2\rangle=4,\ \langle v_1,v_2\rangle=0$",
              fontsize=12, color=INK)

fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}")
print(f"  ||e1||={anorm(e1):.4f} ||e2||={anorm(e2):.4f} angle(e1,e2)={angle_between(e1,e2):.3f} deg")
print(f"  <v1,v2>={adot(v1,v2):.4f} <v1,v1>={adot(v1,v1):.4f} <v2,v2>={adot(v2,v2):.4f}")
