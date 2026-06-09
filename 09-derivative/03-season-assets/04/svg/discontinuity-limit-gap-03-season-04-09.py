#!/usr/bin/env python3
"""Static figure for 09강 3기 04강 — why lim_{h->0} f(x+h) = f(x) means
"continuity" (lecture section 9). The curve approaches 2 at x=1 from both
sides, but the function value is f(1)=1 (a separate dot), so the limit (2)
and the value (1) disagree: not continuous. Renders next to itself as an SVG.

Reproduce:
  uv run --with matplotlib --with numpy python discontinuity-limit-gap-03-season-04-09.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).with_suffix(".svg")

# A smooth curve whose value at x=1 we will *override* to create a hole.
# Use g(x) = 2 + 0.6*(x-1) so that g(1) = 2 (the limit), slope is gentle.
def g(x):
    return 2.0 + 0.6 * (x - 1.0)

xL = np.linspace(0.0, 1.0, 200)   # left branch, up to (but not incl.) x=1
xR = np.linspace(1.0, 2.0, 200)   # right branch, from x=1 on

fig, ax = plt.subplots(figsize=(6.2, 5.0))

# the curve heading toward 2 from both sides
ax.plot(xL, g(xL), color="#1f6feb", lw=2.4, zorder=3)
ax.plot(xR, g(xR), color="#1f6feb", lw=2.4, zorder=3)

# the limit point (2): open circle — the curve approaches it but the value
# is defined elsewhere
ax.scatter([1], [2.0], facecolors="white", edgecolors="#1f6feb",
           s=110, lw=2.2, zorder=5)
# the actual function value f(1)=1: a separate filled dot below
ax.scatter([1], [1.0], facecolors="#d1242f", edgecolors="#d1242f",
           s=110, zorder=6)

# guide lines marking the gap between limit (2) and value (1) at x=1
ax.plot([1, 1], [1.0, 2.0], color="#6e7781", lw=1.4, ls=(0, (3, 3)), zorder=2)
ax.annotate("", xy=(1, 2.0), xytext=(1, 1.0),
            arrowprops=dict(arrowstyle="<->", color="#8250df", lw=1.6))
ax.text(1.06, 1.5, "gap", color="#8250df", fontsize=12.5, weight="bold")

# horizontal dashes to the y-axis for the two values
for y, c in [(2.0, "#1f6feb"), (1.0, "#d1242f")]:
    ax.plot([0, 1], [y, y], color=c, lw=0.9, ls=":", zorder=1)

# annotations: the limit and the value
ax.text(0.18, 2.18, r"$\lim_{h\to 0} f(1+h) = 2$", color="#1f6feb", fontsize=13)
ax.text(1.08, 0.92, r"$f(1) = 1$", color="#d1242f", fontsize=13)
ax.text(0.30, 0.30,
        r"limit $\neq$ value  $\Rightarrow$  not continuous at $x=1$",
        color="#24292f", fontsize=12.5)

# tick at x=1
ax.scatter([1], [0], s=14, color="#24292f", zorder=4)
ax.text(0.97, -0.22, r"$1$", fontsize=12, color="#24292f")

ax.set_xlim(0.0, 2.0)
ax.set_ylim(-0.4, 3.0)
ax.set_xlabel("x")
ax.set_ylabel("y", rotation=0, labelpad=10)
ax.axhline(0, color="#d0d7de", lw=0.8, zorder=0)
ax.axvline(0, color="#d0d7de", lw=0.8, zorder=0)
ax.set_xticks([0, 1, 2])
ax.set_yticks([1, 2])
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}  (limit at x=1 -> {g(1.0):.1f}, value f(1)=1.0, gap=1.0)")
