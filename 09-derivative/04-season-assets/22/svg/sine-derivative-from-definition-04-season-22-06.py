#!/usr/bin/env python3
"""Static figure for 09강 4기 22강 §6 — "왜 (sin x)' = cos x 인가" 를 미분계수의
정의로 돌아가 보이는 그림. 한 점 x0 에서 sin 의 할선(secant)이 h -> 0 일 때
접선(tangent)으로 수렴하고, 그 접선 기울기가 정확히 cos(x0) 임을 보인다.
Renders next to itself as an SVG embedded by the note.

Reproduce:  uv run --with matplotlib --with numpy python sine-derivative-from-definition-04-season-22-06.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).with_suffix(".svg")

x0 = 1.0                      # base point
slope_true = np.cos(x0)      # the derivative we want to *show* equals cos(x0)

xs = np.linspace(-0.4, 3.4, 600)

fig, ax = plt.subplots(figsize=(6.6, 4.6))

# the curve y = sin x
ax.plot(xs, np.sin(xs), color="#1f6feb", lw=2.4, zorder=4, label=r"$y=\sin x$")

# secant lines for shrinking h, fading toward the tangent
hs = [1.4, 0.9, 0.5]
greys = ["#c4ccd6", "#9aa7b8", "#6e7781"]
for h, c in zip(hs, greys):
    x1 = x0 + h
    m = (np.sin(x1) - np.sin(x0)) / h           # secant slope = difference quotient
    line = np.sin(x0) + m * (xs - x0)
    keep = (xs >= x0 - 0.35) & (xs <= x1 + 0.25)
    ax.plot(xs[keep], line[keep], color=c, lw=1.5, zorder=2)
    ax.scatter([x1], [np.sin(x1)], s=24, color=c, zorder=5)
    ax.annotate(rf"$h={h:.1f}$", (x1, np.sin(x1)),
                textcoords="offset points", xytext=(6, -12),
                fontsize=9, color="#57606a")

# the limiting tangent line, slope = cos(x0)
tan = np.sin(x0) + slope_true * (xs - x0)
keep = (xs >= x0 - 0.9) & (xs <= x0 + 1.4)
ax.plot(xs[keep], tan[keep], color="#d1242f", lw=2.4, zorder=3)

# base point and helpers
ax.scatter([x0], [np.sin(x0)], s=40, color="#24292f", zorder=6)
ax.annotate(r"$(x_0,\ \sin x_0)$", (x0, np.sin(x0)),
            textcoords="offset points", xytext=(-78, 8), fontsize=11, color="#24292f")

# difference-quotient bracket: rise over run for the largest h
hx = x0 + hs[0]
ax.plot([x0, hx], [np.sin(x0), np.sin(x0)], color="#8c959f", lw=1.0, ls=":", zorder=1)
ax.plot([hx, hx], [np.sin(x0), np.sin(hx)], color="#8c959f", lw=1.0, ls=":", zorder=1)
ax.text((x0 + hx) / 2, np.sin(x0) - 0.16, r"$h$", ha="center", fontsize=10, color="#57606a")
ax.text(hx + 0.05, (np.sin(x0) + np.sin(hx)) / 2,
        r"$\sin(x_0{+}h){-}\sin x_0$", fontsize=9, color="#57606a", va="center")

# the formula being illustrated
ax.text(0.02, 0.965,
        r"$f'(x_0)=\lim_{h\to0}\dfrac{\sin(x_0{+}h)-\sin x_0}{h}=\cos x_0$",
        transform=ax.transAxes, fontsize=12.5, color="#24292f", va="top")
ax.text(x0 - 0.85, np.sin(x0) + slope_true * (-0.85) - 0.02,
        r"tangent, slope $=\cos x_0$", color="#d1242f", fontsize=10,
        rotation=np.degrees(np.arctan(slope_true)), rotation_mode="anchor")

ax.axhline(0, color="#d0d7de", lw=0.8, zorder=0)
ax.set_xlim(-0.4, 3.4)
ax.set_ylim(-0.6, 1.45)
ax.set_xticks([x0], [r"$x_0$"])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.legend(loc="lower left", frameon=False, fontsize=11)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")

# numeric sanity check: difference quotients should approach cos(x0)
print(f"cos(x0) = {slope_true:.6f}")
for h in [0.5, 0.1, 0.01, 0.001]:
    dq = (np.sin(x0 + h) - np.sin(x0)) / h
    print(f"  h={h:<6}  difference quotient = {dq:.6f}")
print(f"wrote {OUT}")
