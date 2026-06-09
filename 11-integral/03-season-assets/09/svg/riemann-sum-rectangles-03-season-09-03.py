#!/usr/bin/env python3
"""Static figure for 11강 3기 9강 — the Riemann sum: filling the area under a
curve with rectangles of width Delta x and height f(x_{k-1}) (lecture §3).
Renders next to itself as an SVG embedded by the note.

Reproduce:  uv run --with matplotlib --with numpy python riemann-sum-rectangles-03-season-09-03.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).with_suffix(".svg")


def f(x):
    return x**2


a, b, n = 0.0, 1.0, 8
edges = np.linspace(a, b, n + 1)        # x_0, ..., x_n
left = edges[:-1]                        # x_{k-1} (left endpoints)
dx = (b - a) / n
heights = f(left)                        # f(x_{k-1})

riemann = np.sum(heights * dx)
exact = (b**3 - a**3) / 3.0

xs = np.linspace(a - 0.05, b + 0.08, 400)

fig, ax = plt.subplots(figsize=(6.4, 4.8))

# left-rectangle Riemann sum
ax.bar(left, heights, width=dx, align="edge",
       color="#9ecbff", edgecolor="#1f6feb", lw=1.1, alpha=0.55, zorder=2)

# the curve y = x^2
ax.plot(xs, f(xs), color="#d1242f", lw=2.4, zorder=4, label=r"$y=f(x)=x^2$")

# mark a representative subinterval [x_{k-1}, x_k] with width Delta x
k = 5
x0, x1 = edges[k], edges[k + 1]
y0 = f(x0)
ax.annotate("", xy=(x1, -0.085), xytext=(x0, -0.085),
            arrowprops=dict(arrowstyle="<->", color="#24292f", lw=1.3))
ax.text((x0 + x1) / 2, -0.16, r"$\Delta x$", ha="center", fontsize=12, color="#24292f")
ax.plot([x0, x0], [0, y0], color="#0b8457", lw=1.4, ls=":", zorder=5)
ax.annotate(r"$f(x_{k-1})$", xy=(x0, y0), xytext=(x0 - 0.30, y0 + 0.20),
            fontsize=11.5, color="#0b8457",
            arrowprops=dict(arrowstyle="->", color="#0b8457", lw=1.1))

# axis ticks at the partition points x_0 .. x_n
ax.set_xticks(edges)
ax.set_xticklabels([r"$x_0$"] + [""] * (n - 1) + [r"$x_n$"])
ax.set_yticks([0, 0.5, 1.0])

ax.set_xlim(a - 0.10, b + 0.12)
ax.set_ylim(-0.22, 1.12)
ax.set_xlabel(r"$x$   (partition $a=x_0<x_1<\cdots<x_n=b$)")
ax.set_ylabel(r"$y$")
ax.set_title(
    r"Riemann sum  $\sum_{k=1}^{n} f(x_{k-1})\,\Delta x \;\to\; \int_a^b f(x)\,dx$"
    + "\n"
    + rf"$n={n}$:  sum $\approx {riemann:.4f}$    exact $=\frac{{1}}{{3}}={exact:.4f}$",
    fontsize=11.5)

ax.axhline(0, color="#d0d7de", lw=0.8, zorder=1)
ax.legend(loc="upper left", fontsize=11, frameon=False)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}  (n={n}, riemann={riemann:.4f}, exact={exact:.4f})")
