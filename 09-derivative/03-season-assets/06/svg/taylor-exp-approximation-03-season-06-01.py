#!/usr/bin/env python3
"""Static figure for 09강 3기 6강 — building the Taylor series of e^x by peeling
off terms one degree at a time (lecture §1).

Overlay e^x with its Taylor partial sums about x = 0:
    T1 = 1 + x
    T2 = 1 + x + x^2/2
    T3 = 1 + x + x^2/2 + x^3/6
    T10 = sum_{n=0}^{10} x^n/n!
Each extra term hugs e^x over a WIDER window around the center, yet every finite
polynomial eventually peels away far from 0 — exactly the note's point that more
terms widen the good range but a finite degree always diverges in the end.

Reproduce:
  uv run --with matplotlib --with numpy python taylor-exp-approximation-03-season-06-01.py
"""
from pathlib import Path
from math import factorial
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).with_suffix(".svg")


def taylor(x, deg):
    return sum(x**n / factorial(n) for n in range(deg + 1))


x = np.linspace(-3.0, 3.0, 800)
exact = np.exp(x)

fig, ax = plt.subplots(figsize=(6.6, 5.0))

# e^x itself (thick reference curve)
ax.plot(x, exact, color="#24292f", lw=2.8, label=r"$e^x$", zorder=6)

# partial sums, lighter -> they fan away from e^x as degree drops
curves = [
    (1, "#d1242f", r"$T_1=1+x$"),
    (2, "#e3690b", r"$T_2=1+x+\frac{x^2}{2}$"),
    (3, "#1f6feb", r"$T_3=1+x+\frac{x^2}{2}+\frac{x^3}{6}$"),
    (10, "#0b8457", r"$T_{10}=\sum_{n=0}^{10}\frac{x^n}{n!}$"),
]
for deg, color, lbl in curves:
    ax.plot(x, taylor(x, deg), color=color, lw=1.8,
            ls=(0, (6, 3)) if deg < 10 else "-", label=lbl, zorder=4)

# the expansion center (0, 1): all partial sums pass through it and match slope 1
ax.scatter([0], [1], s=45, color="#24292f", zorder=7)
ax.annotate(r"center $(0,1)$, slope $1$", (0, 1), textcoords="offset points",
            xytext=(10, -22), fontsize=10.5, color="#24292f")

# shade the window where even T3 stays close (|x| <= 1, the note's -1<=x<=1)
ax.axvspan(-1, 1, color="#1f6feb", alpha=0.06, zorder=0)
ax.text(0, 18.5, r"$-1\leq x\leq 1$: good fit", ha="center", fontsize=10,
        color="#3a5a8c")

ax.set_xlim(-3.0, 3.0)
ax.set_ylim(-4.0, 21.0)
ax.axhline(0, color="#d0d7de", lw=0.8, zorder=0)
ax.axvline(0, color="#d0d7de", lw=0.8, zorder=0)
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_title(r"Taylor partial sums of $e^x$ about $x=0$: more terms, wider fit",
             fontsize=11.5)
ax.legend(loc="upper left", fontsize=9.5, framealpha=0.9)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}")

# sanity checks: partial sums match e^x increasingly well near 0, diverge far out
for xv in (0.0, 0.5, 1.0, 2.5):
    print(f"x={xv:>4}: e^x={np.exp(xv):8.4f}  "
          f"T1={taylor(xv,1):8.4f}  T2={taylor(xv,2):8.4f}  "
          f"T3={taylor(xv,3):8.4f}  T10={taylor(xv,10):8.4f}")
