#!/usr/bin/env python3
"""Static figure for 11강 3기 10강 — why "first non-vanishing Taylor term" decides
the local shape at the origin (lecture §5, also §0). x^4 (even leading term) gives a
local min; x^3 (odd leading term) flips sign across 0 -> inflection, not an extremum.
Both have f''(0)=0, so "f''=0" alone cannot decide. Renders next to itself as an SVG.

Reproduce:  uv run --with matplotlib --with numpy python even-vs-odd-leading-term-03-season-10-05.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).with_suffix(".svg")

x = np.linspace(-1.25, 1.25, 401)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 4.2), sharey=False)

# ---- left: x^4, even leading term -> local minimum at 0 ----
ax1.plot(x, x**4, color="#1f6feb", lw=2.6, zorder=4)
ax1.scatter([0], [0], s=42, color="#0b8457", zorder=6)
ax1.annotate("local min\n(both sides go UP)", xy=(0, 0), xytext=(-1.18, 1.05),
             fontsize=10.5, color="#0b8457",
             arrowprops=dict(arrowstyle="->", color="#0b8457", lw=1.1))
ax1.set_title(r"$y=x^4$   (first non-zero term: even, $+$)" + "\n"
              r"$f''(0)=0$  but stays a min", fontsize=11)

# ---- right: x^3, odd leading term -> sign flips -> inflection, not extremum ----
ax2.plot(x, x**3, color="#d1242f", lw=2.6, zorder=4)
ax2.scatter([0], [0], s=42, color="#8250df", zorder=6)
ax2.annotate("inflection\n(left DOWN, right UP)", xy=(0, 0), xytext=(-1.2, 1.15),
             fontsize=10.5, color="#8250df",
             arrowprops=dict(arrowstyle="->", color="#8250df", lw=1.1))
ax2.set_title(r"$y=x^3$   (first non-zero term: odd)" + "\n"
              r"$f''(0)=0$  and sign flips", fontsize=11)

for ax in (ax1, ax2):
    ax.axhline(0, color="#d0d7de", lw=0.9, zorder=1)
    ax.axvline(0, color="#d0d7de", lw=0.9, zorder=1)
    ax.set_xlim(-1.3, 1.3)
    ax.set_xticks([-1, 0, 1])
    ax.set_xlabel(r"$x$")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
ax1.set_ylim(-0.15, 1.7)
ax2.set_ylim(-1.7, 1.7)
ax1.set_yticks([0, 1])
ax2.set_yticks([-1, 0, 1])

fig.suptitle("First non-vanishing term's parity decides the local shape",
             fontsize=12.5, y=1.02)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}")
print(f"x^4 at +/-0.5: {0.5**4:.4f} (both > 0 -> min)")
print(f"x^3 at -0.5, +0.5: {(-0.5)**3:.4f}, {0.5**3:.4f} (sign flips -> inflection)")
