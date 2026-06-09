#!/usr/bin/env python3
"""Static figure for 04강 3기 5강 (군의 관점에서 지수법칙) — §16 (갈루아 예시).

The roots of x^3=1 sit on the unit circle, 120° apart; the roots of y^3=2 sit on a
circle of radius 2^(1/3), also 120° apart. The Galois group of Q(roots of y^3-2)
permutes these roots while fixing Q and preserving +,× — exactly 6 such maps, with
the structure of S_3.

Reproduce:
  uv run --with matplotlib --with numpy python cube-roots-complex-plane-03-season-05-16.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

OUT = Path(__file__).with_suffix(".svg")

blue, red, green, grey = "#1f6feb", "#d1242f", "#0b8457", "#6e7781"

# cube roots of unity:  e^{2πik/3}
k = np.array([0, 1, 2])
unit = np.exp(2j * np.pi * k / 3)                 # x^3 = 1
two = (2.0 ** (1 / 3)) * np.exp(2j * np.pi * k / 3)   # y^3 = 2  (real cube root x roots of unity)

R = 2.0 ** (1 / 3)

fig, ax = plt.subplots(figsize=(6.4, 6.0))

# circles
ax.add_patch(Circle((0, 0), 1.0, fill=False, color=blue, lw=1.6, ls=(0, (5, 4))))
ax.add_patch(Circle((0, 0), R, fill=False, color=red, lw=1.6, ls=(0, (5, 4))))

# axes
ax.axhline(0, color="#d0d7de", lw=0.9, zorder=0)
ax.axvline(0, color="#d0d7de", lw=0.9, zorder=0)

# roots of x^3 = 1
for z in unit:
    ax.scatter([z.real], [z.imag], s=70, color=blue, zorder=6)
ax.annotate(r"$1$", (unit[0].real, unit[0].imag), textcoords="offset points",
            xytext=(8, -12), color=blue, fontsize=12)
ax.annotate(r"$\omega$", (unit[1].real, unit[1].imag), textcoords="offset points",
            xytext=(6, 6), color=blue, fontsize=12)
ax.annotate(r"$\omega^2$", (unit[2].real, unit[2].imag), textcoords="offset points",
            xytext=(6, -16), color=blue, fontsize=12)

# roots of y^3 = 2
for z in two:
    ax.scatter([z.real], [z.imag], s=70, color=red, zorder=6)
ax.annotate(r"$\sqrt[3]{2}$", (two[0].real, two[0].imag), textcoords="offset points",
            xytext=(8, -14), color=red, fontsize=12)
ax.annotate(r"$\sqrt[3]{2}\,\omega$", (two[1].real, two[1].imag),
            textcoords="offset points", xytext=(6, 8), color=red, fontsize=12)
ax.annotate(r"$\sqrt[3]{2}\,\omega^{2}$", (two[2].real, two[2].imag),
            textcoords="offset points", xytext=(-44, -16), color=red, fontsize=12)

# 120° angle marker on the unit circle
for ang in (0, 120, 240):
    pass
arc_r = 0.34
th = np.linspace(0, 2 * np.pi / 3, 40)
ax.plot(arc_r * np.cos(th), arc_r * np.sin(th), color=grey, lw=1.2)
ax.text(0.30, 0.20, r"$120^\circ$", color=grey, fontsize=11)

# a permutation arrow: a Galois map rotates the three roots (omega <-> omega^2 etc.)
def curved(p, q, color):
    ax.add_patch(FancyArrowPatch(p, q, connectionstyle="arc3,rad=0.28",
                                 arrowstyle="-|>", mutation_scale=14,
                                 lw=1.6, color=color, zorder=7))

curved((two[1].real, two[1].imag), (two[2].real, two[2].imag), green)
curved((two[2].real, two[2].imag), (two[1].real, two[1].imag), green)
ax.text(-1.55, 1.25,
        "Galois group permutes the roots\n"
        r"(fix $\mathbb{Q}$, preserve $+,\times$): $6$ maps $\cong S_3$",
        color=green, fontsize=10.5)

ax.set_xlim(-1.75, 1.95)
ax.set_ylim(-1.75, 1.95)
ax.set_aspect("equal")
ax.set_xlabel("Re")
ax.set_ylabel("Im")
ax.set_title(r"roots of $x^3=1$ (unit circle) and $y^3=2$ (radius $\sqrt[3]{2}$)",
             fontsize=12.5)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}  R={R:.4f}  unit-roots check sum={unit.sum():.2e}  "
      f"two-roots check |z|={np.abs(two)}")
