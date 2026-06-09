#!/usr/bin/env python3
"""Static figure for 16강 3기 15강 — complex multiplication as "rotation + scaling"
(lecture section 4). Multiplying by z = r e^{iθ} rotates a vector by θ and scales
its length by r; the special case z = i is a 90° rotation. Renders next to itself
as an SVG embedded by the note.

Reproduce:
  uv run --with matplotlib --with numpy python complex-multiplication-rotation-scaling-03-season-15-04.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyArrowPatch

OUT = Path(__file__).with_suffix(".svg")

# w is the vector being multiplied; z = r e^{iθ} is the multiplier.
w = complex(2.4, 0.6)
r, theta = 1.4, np.deg2rad(55.0)
z = r * np.exp(1j * theta)
zw = z * w                      # the product: rotate w by θ, scale by r

# special case: i * w  (a clean 90° rotation, no scaling)
iw = 1j * w


def C(c):
    return (c.real, c.imag)


def arrow(ax, p, color, lw=2.3, ls="-", z_=5):
    ax.add_patch(FancyArrowPatch((0, 0), C(p), arrowstyle="-|>", mutation_scale=18,
                                 lw=lw, color=color, ls=ls, shrinkA=0, shrinkB=0, zorder=z_))


def ang(c):
    return np.rad2deg(np.angle(c))


def mag(c):
    return abs(c)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 5.0))

# ---- left panel: z = r e^{iθ} rotates by θ AND scales by r --------------------
arrow(ax1, w, "#1f6feb")                    # w
arrow(ax1, zw, "#d1242f")                   # z·w
# dashed circle arc showing rotation of the direction of w out to |w|
ax1.add_patch(Arc((0, 0), 2 * mag(w), 2 * mag(w), angle=0,
                  theta1=ang(w), theta2=ang(zw), color="#57606a", lw=1.2, ls=(0, (5, 4))))
# the scaling: pure rotation of w (same length) to the angle of z·w, then radial stretch
w_rot = mag(w) * np.exp(1j * np.angle(zw))   # w rotated by θ, same length
ax1.plot([w_rot.real, zw.real], [w_rot.imag, zw.imag],
         color="#0b8457", lw=2.0, ls=(0, (1, 2)), zorder=4)
ax1.scatter([w_rot.real], [w_rot.imag], s=16, color="#57606a", zorder=6)
# angle-θ arc near origin
ax1.add_patch(Arc((0, 0), 1.5, 1.5, angle=0, theta1=ang(w), theta2=ang(zw),
                  color="#8250df", lw=1.6))
ax1.text(1.02, 0.62, r"$\theta$", color="#8250df", fontsize=15)

ax1.text(w.real + 0.06, w.imag - 0.28, r"$w$", color="#1f6feb", fontsize=15, weight="bold")
ax1.text(zw.real + 0.05, zw.imag + 0.08, r"$z\,w$", color="#d1242f", fontsize=15, weight="bold")
ax1.text(0.45 * (w_rot.real + zw.real) + 0.05, 0.45 * (w_rot.imag + zw.imag) + 0.18,
         r"scale $\times r$", color="#0b8457", fontsize=11)
ax1.set_title(r"$z=r\,e^{i\theta}$:  rotate by $\theta$, scale by $r$",
              fontsize=13)
ax1.set_xlim(-0.6, 4.2)
ax1.set_ylim(-0.6, 4.2)

# ---- right panel: multiply by i  =>  pure 90° rotation -----------------------
arrow(ax2, w, "#1f6feb")                    # w
arrow(ax2, iw, "#bf3989")                   # i·w
ax2.add_patch(Arc((0, 0), 2 * mag(w), 2 * mag(w), angle=0,
                  theta1=ang(w), theta2=ang(iw), color="#57606a", lw=1.2, ls=(0, (5, 4))))
# right-angle marker at origin between w and i·w
d1 = (w / mag(w)) * 0.28
d2 = (iw / mag(iw)) * 0.28
sq = np.array([C(d1), C(d1 + d2), C(d2), (0, 0)])
ax2.plot(sq[:, 0], sq[:, 1], color="#6e7781", lw=1.1, zorder=3)
ax2.text(w.real + 0.06, w.imag - 0.28, r"$w$", color="#1f6feb", fontsize=15, weight="bold")
ax2.text(iw.real + 0.06, iw.imag + 0.05, r"$i\,w$", color="#bf3989", fontsize=15, weight="bold")
ax2.text(0.55, 1.35, r"$90^\circ$", color="#57606a", fontsize=13)
ax2.set_title(r"$z=i$:  pure $90^\circ$ rotation, $r=1$", fontsize=13)
ax2.set_xlim(-1.4, 3.0)
ax2.set_ylim(-0.6, 3.0)

for ax in (ax1, ax2):
    ax.scatter([0], [0], s=18, color="#24292f", zorder=7)
    ax.text(-0.26, -0.22, r"$O$", fontsize=12, color="#24292f")
    ax.set_aspect("equal")
    ax.axhline(0, color="#d0d7de", lw=0.9, zorder=0)
    ax.axvline(0, color="#d0d7de", lw=0.9, zorder=0)
    ax.set_xlabel("Re", fontsize=11)
    ax.set_ylabel("Im", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

fig.suptitle(r"Complex multiplication on $\mathbb{C}\cong\mathbb{R}^2$", fontsize=14)
fig.tight_layout(rect=(0, 0, 1, 0.97))
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}")
print(f"  |w|={mag(w):.4f}, arg(w)={ang(w):.2f}deg")
print(f"  |z·w|={mag(zw):.4f} (=r·|w|={r*mag(w):.4f}), "
      f"arg(z·w)-arg(w)={ang(zw)-ang(w):.2f}deg (=θ={np.rad2deg(theta):.2f}deg)")
print(f"  |i·w|={mag(iw):.4f} (=|w|), arg(i·w)-arg(w)={ang(iw)-ang(w):.2f}deg (=90deg)")
