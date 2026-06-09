#!/usr/bin/env python3
"""Static figure for 04강 3기 5강 (군의 관점에서 지수법칙) — §4.

The exponential f(x)=a^x carries the ADDITION of the domain to the MULTIPLICATION
of the codomain: f(x+y)=a^x a^y. Left panel shows a^x on a linear y-axis (equal
steps in x give a GROWING geometric jump in y); right panel shows the same curve
with a LOG-scaled y-axis, where it becomes a straight line — the visual of "두 군을
같게 본다" (§1:57:42): on a log axis, multiplication looks like addition.

Reproduce:
  uv run --with matplotlib --with numpy python exponential-add-to-mult-03-season-05-04.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).with_suffix(".svg")

a = 2.0
x = np.linspace(-0.6, 3.6, 400)
y = a ** x

# three equally-spaced domain points: x, x+1, x+2  ->  multiplicative steps in y
xs = np.array([0.0, 1.0, 2.0])
ys = a ** xs

fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.2, 4.6))

blue, red, green, grey = "#1f6feb", "#d1242f", "#0b8457", "#6e7781"

# ---------- left: linear y-axis ----------
axL.plot(x, y, color=blue, lw=2.4, zorder=4)
for xi, yi in zip(xs, ys):
    axL.plot([xi, xi], [0, yi], color=grey, lw=1.0, ls=(0, (4, 3)), zorder=2)
    axL.plot([-0.6, xi], [yi, yi], color=grey, lw=1.0, ls=(0, (4, 3)), zorder=2)
    axL.scatter([xi], [yi], s=42, color=red, zorder=6)

# brace-style annotations: equal +1 in x, but x2 in y
for xi in [0.5, 1.5]:
    axL.annotate("", xy=(xi + 0.5, -0.55), xytext=(xi - 0.5, -0.55),
                 arrowprops=dict(arrowstyle="<->", color=green, lw=1.4))
axL.text(1.0, -1.15, "+1            +1", color=green, fontsize=11, ha="center")
axL.text(1.0, -1.7, r"domain: equal $+1$ steps (addition)",
         color=green, fontsize=10.5, ha="center")

axL.annotate("", xy=(-0.45, ys[1]), xytext=(-0.45, ys[0]),
             arrowprops=dict(arrowstyle="<->", color=red, lw=1.4))
axL.annotate("", xy=(-0.25, ys[2]), xytext=(-0.25, ys[1]),
             arrowprops=dict(arrowstyle="<->", color=red, lw=1.4))
axL.text(-0.30, 1.4, r"$\times a$", color=red, fontsize=11, rotation=90, va="center")
axL.text(-0.10, 2.9, r"$\times a$", color=red, fontsize=11, rotation=90, va="center")

axL.set_title(r"$f(x)=a^{x}$  on a linear axis", fontsize=12.5)
axL.set_xlabel("x  (addition is uniform)")
axL.set_ylabel(r"$y=a^{x}$  (multiplication grows)")
axL.set_xlim(-0.75, 3.7)
axL.set_ylim(-1.9, a ** 3.6)
axL.axhline(0, color="#d0d7de", lw=0.8, zorder=0)
axL.grid(True, color="#eef1f4", lw=0.8)

# ---------- right: log y-axis -> straight line ----------
axR.plot(x, y, color=blue, lw=2.4, zorder=4)
for xi, yi in zip(xs, ys):
    axR.scatter([xi], [yi], s=42, color=red, zorder=6)
axR.set_yscale("log", base=a)
axR.set_title(r"same curve, $\log_a$-scaled $y$-axis", fontsize=12.5)
axR.set_xlabel("x")
axR.set_ylabel(r"$\log_a y = x$  (now a straight line)")
axR.set_xlim(-0.75, 3.7)
axR.grid(True, which="both", color="#eef1f4", lw=0.8)
axR.text(0.05, 0.93,
         r"$f(x{+}y)=a^{x}a^{y}=f(x)\,f(y)$",
         transform=axR.transAxes, fontsize=11.5, color="#24292f")
axR.text(0.05, 0.84,
         "log makes multiplication look like addition",
         transform=axR.transAxes, fontsize=10, color=green)

for ax in (axL, axR):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}  (a={a}, ys={ys.tolist()}, ratios={ (ys[1]/ys[0], ys[2]/ys[1]) })")
