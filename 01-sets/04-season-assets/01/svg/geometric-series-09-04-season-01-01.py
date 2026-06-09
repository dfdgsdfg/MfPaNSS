#!/usr/bin/env python3
"""Static figure for 01강 4기 01강 — the partial sums of 0.9 + 0.09 + 0.009 + ...
(lecture §1, the "0.999... = 1?" debate). Each partial sum S_n = 1 - 10^{-n} is
strictly below 1 (the "1이 아니다" side) yet the gap 10^{-n} collapses to 0 as
n -> infinity (the "1이다" side). Renders next to itself as an SVG.

Reproduce:  uv run --with matplotlib --with numpy python geometric-series-09-04-season-01-01.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).with_suffix(".svg")

n = np.arange(1, 9)
S = 1 - 10.0 ** (-n)          # partial sums: 0.9, 0.99, 0.999, ...
gap = 10.0 ** (-n)            # distance to 1: each term strictly positive

# sanity: S_n = sum of first n terms of 0.9 * (1/10)^k, and S_n + gap = 1 exactly
parts = 0.9 * (1 / 10.0) ** np.arange(0, 8)
S_check = np.cumsum(parts)
assert np.allclose(S, S_check), "partial sums must match the geometric series"
assert np.allclose(S + gap, 1.0), "S_n + 10^{-n} must equal 1"

fig, ax = plt.subplots(figsize=(6.4, 4.4))

# the limit line y = 1
ax.axhline(1.0, color="#d1242f", lw=1.6, ls="--", zorder=2)
ax.text(8.15, 1.0, r"$1$", color="#d1242f", fontsize=13, va="center")

# partial sums climbing toward 1 (each one strictly below the line)
ax.plot(n, S, color="#1f6feb", lw=1.4, zorder=3)
ax.scatter(n, S, s=42, color="#1f6feb", zorder=4)

# annotate the first few values to make "each digit < 1" concrete
for k, (xx, yy) in enumerate(zip(n[:3], S[:3])):
    ax.annotate(f"{yy:.{k+1}f}", (xx, yy), textcoords="offset points",
                xytext=(2, -14), fontsize=10, color="#0b3d91")

# show the shrinking gap 10^{-n} as a vertical segment for one term
xg = 4
ax.annotate("", xy=(xg, 1.0), xytext=(xg, S[xg - 1]),
            arrowprops=dict(arrowstyle="<->", color="#0b8457", lw=1.4))
ax.text(xg + 0.12, (1.0 + S[xg - 1]) / 2,
        r"gap $=10^{-n}\to 0$", color="#0b8457", fontsize=11, va="center")

ax.set_xlabel(r"$n$  (number of 9's)", fontsize=12)
ax.set_ylabel(r"$S_n = 0.99\cdots9$  ($n$ nines)", fontsize=12)
ax.set_title(r"$S_n = 1 - 10^{-n}$ :  every $S_n < 1$,  yet  $S_n \to 1$",
             fontsize=12.5)
ax.set_xlim(0.5, 8.6)
ax.set_ylim(0.86, 1.03)
ax.set_xticks(n)
ax.grid(True, color="#eaeef2", lw=0.8)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}  (S_8={S[-1]:.8f}, gap_8={gap[-1]:.1e})")
