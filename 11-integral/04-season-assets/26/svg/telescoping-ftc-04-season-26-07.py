#!/usr/bin/env python3
"""Static figure for 11강 4기 26강 — the telescoping sum that becomes the FTC
(lecture §7).  A smooth function f on [1, 10] is sampled at the integer
partition points; the total rise f(10) - f(1) is rebuilt as the telescoping
sum of the step rises  sum_k [ f(x_k) - f(x_{k-1}) ] ,  each step rise being
approximately the slope f'(x_{k-1}) times the width Δx.  Shrinking Δx → 0 turns
the sum into ∫ f'(x) dx = f(b) - f(a).

Renders next to itself as an SVG embedded by the note.

Reproduce:  uv run --with matplotlib --with numpy python telescoping-ftc-04-season-26-07.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).with_suffix(".svg")

a, b = 1.0, 10.0


def f(x):
    # a generic smooth, monotone-ish "differentiable curve" on [1, 10]
    return 0.9 + 0.55 * x + 1.7 * np.sin(0.45 * x + 0.3)


# partition points x_0 = a, ..., x_n = b  (Δx = 1, the integer marks in the note)
xs = np.arange(a, b + 1)            # 1, 2, ..., 10
ys = f(xs)

# smooth curve
xx = np.linspace(a, b, 400)
yy = f(xx)

fig, ax = plt.subplots(figsize=(7.2, 5.0))

# the differentiable curve y = f(x)
ax.plot(xx, yy, color="#1f6feb", lw=2.4, zorder=4, label=r"$y=f(x)$")

# telescoping staircase: for each panel, a horizontal "run" Δx and a vertical
# "rise" f(x_k) - f(x_{k-1}).  The rises stack to f(b) - f(a).
for k in range(1, len(xs)):
    x0, x1 = xs[k - 1], xs[k]
    y0, y1 = ys[k - 1], ys[k]
    # horizontal run at the lower function value
    ax.plot([x0, x1], [y0, y0], color="#9aa7b8", lw=1.1, ls=(0, (5, 3)), zorder=2)
    # vertical rise f(x_k) - f(x_{k-1})
    ax.plot([x1, x1], [y0, y1], color="#0b8457", lw=2.0, zorder=3)
    # little secant chord ~ slope f'(x_{k-1}) Δx over the panel
    ax.plot([x0, x1], [y0, y1], color="#d1242f", lw=1.0, ls=":", zorder=3)

# partition points on the curve
ax.scatter(xs, ys, s=26, color="#1f6feb", zorder=6)

# total rise f(b) - f(a) shown as a bracket on the right
xb = b + 0.45
ax.annotate("", xy=(xb, ys[-1]), xytext=(xb, ys[0]),
            arrowprops=dict(arrowstyle="<->", color="#24292f", lw=1.6))
ax.plot([b, xb], [ys[-1], ys[-1]], color="#bbb", lw=0.8, zorder=1)
ax.plot([b, xb], [ys[0], ys[0]], color="#bbb", lw=0.8, zorder=1)
ax.text(xb + 0.12, 0.5 * (ys[0] + ys[-1]),
        r"$f(b)-f(a)$", fontsize=13, color="#24292f",
        ha="left", va="center", rotation=90)

# endpoint labels a, b on the x-axis
ax.text(a, ys.min() - 0.9, r"$a=1$", fontsize=12, color="#24292f", ha="center")
ax.text(b, ys.min() - 0.9, r"$b=10$", fontsize=12, color="#24292f", ha="center")

# one labelled panel (the rising step between x=2 and x=3, lots of clear space):
#   the run Δx, the step rise f(x_k)-f(x_{k-1}), and the secant slope f'·Δx
kk = 2                      # panel from x_{kk}=2 to x_{kk+1}=3
xm = 0.5 * (xs[kk] + xs[kk + 1])
ax.text(xm, ys[kk] - 0.55, r"$\Delta x$", fontsize=12, color="#57606a", ha="center")
ax.text(xs[kk + 1] + 0.12, 0.5 * (ys[kk] + ys[kk + 1]),
        r"$f(x_k)-f(x_{k-1})$", fontsize=11, color="#0b8457", ha="left", va="center")
ax.text(xs[kk] - 0.15, 0.5 * (ys[kk] + ys[kk + 1]) + 0.05,
        r"$\approx f'(x_{k-1})\,\Delta x$", fontsize=10.5, color="#d1242f",
        ha="right", va="center")

# the FTC identity as the takeaway (mathtext has no \xrightarrow, so the
# "Δx → 0" condition rides just above a plain long arrow)
ax.text(a - 0.3, ys.max() + 1.55,
        r"$\sum_k [\,f(x_k)-f(x_{k-1})\,]=f(b)-f(a)$",
        fontsize=12.5, color="#24292f", ha="left", va="center")
ax.text(a - 0.3, ys.max() + 0.85,
        r"$\longrightarrow\quad \int_a^b f'(x)\,dx=f(b)-f(a)$",
        fontsize=12.5, color="#24292f", ha="left", va="center")
ax.text(a + 0.35, ys.max() + 1.18,
        r"$\Delta x\to 0$", fontsize=10, color="#57606a", ha="center", va="center")

ax.set_xlim(a - 0.7, b + 2.0)
ax.set_ylim(ys.min() - 1.3, ys.max() + 2.4)
ax.set_xticks(xs)
ax.set_xticklabels([str(int(x)) for x in xs])
ax.set_yticks([])
ax.axhline(ys.min() - 1.3, color="#d0d7de", lw=0.0)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#d0d7de")
ax.tick_params(axis="x", length=0, labelsize=10, colors="#57606a")
ax.legend(loc="lower right", frameon=False, fontsize=12)

fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
total = ys[-1] - ys[0]
tele = float(np.sum(np.diff(ys)))
print(f"wrote {OUT}  f(b)-f(a)={total:.4f}  telescoping sum={tele:.4f}  "
      f"match={np.isclose(total, tele)}")
