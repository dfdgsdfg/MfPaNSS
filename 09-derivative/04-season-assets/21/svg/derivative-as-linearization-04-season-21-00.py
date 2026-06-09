#!/usr/bin/env python3
"""Static figure for 09강 4기 21강 — the derivative as *linearization* of a
nonlinear function (lecture §0: "선형이 아닌 함수를 선형화하는 것이 미분").

A curve f is nonlinear; at the point a its tangent line is the best linear
approximation. A secant through (a, f(a)) and (a+h, f(a+h)) tilts toward that
tangent as h -> 0 — the limit that *extracts* the slope f'(a) (the 1x1 Jacobian).

All plotted text is ASCII/English (matplotlib default font has no Korean glyphs).

Reproduce:
  uv run --with matplotlib --with numpy python derivative-as-linearization-04-season-21-00.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).with_suffix(".svg")


def f(x):
    return 0.35 * x**2 + 0.2 * x + 0.6


def fp(x):
    return 0.70 * x + 0.2


a = 1.4                      # point of linearization
h = 1.9                      # secant offset (deliberately large, to show the tilt)
fa, fpa = f(a), fp(a)

xs = np.linspace(-1.2, 4.2, 400)

fig, ax = plt.subplots(figsize=(6.4, 5.0))

# the nonlinear function
ax.plot(xs, f(xs), color="#1f6feb", lw=2.4, label=r"$f(x)$  (nonlinear)", zorder=4)

# tangent line at a  ==  the linearization  L(x) = f(a) + f'(a)(x-a)
ax.plot(xs, fa + fpa * (xs - a), color="#0b8457", lw=2.0,
        label=r"tangent  $L(x)=f(a)+f'(a)(x-a)$", zorder=3)

# secant through (a, f(a)) and (a+h, f(a+h)) — approximates, tilts to tangent as h->0
xb = a + h
fb = f(xb)
sec_slope = (fb - fa) / h
ax.plot(xs, fa + sec_slope * (xs - a), color="#d1242f", lw=1.6,
        ls=(0, (6, 4)), label=r"secant  (slope $\frac{f(a+h)-f(a)}{h}$)", zorder=2)

# the rise/run triangle of the secant
ax.plot([a, xb], [fa, fa], color="#6e7781", lw=1.1, ls=":", zorder=2)
ax.plot([xb, xb], [fa, fb], color="#6e7781", lw=1.1, ls=":", zorder=2)
ax.text((a + xb) / 2, fa - 0.42, r"$h$", color="#6e7781", fontsize=12, ha="center")
ax.text(xb + 0.08, (fa + fb) / 2, r"$f(a+h)-f(a)$", color="#6e7781", fontsize=10.5,
        va="center")

# the two anchor points
for (px, py) in [(a, fa), (xb, fb)]:
    ax.scatter([px], [py], s=34, color="#24292f", zorder=6)
ax.text(a - 0.05, fa - 0.5, r"$(a,\,f(a))$", color="#24292f", fontsize=11, ha="center")
ax.text(xb + 0.05, fb + 0.18, r"$(a+h,\,f(a+h))$", color="#24292f", fontsize=10.5)

# the limit statement: secant slope -> tangent slope = derivative
ax.text(-1.05, 6.55,
        r"$f'(a)=\lim_{h\to 0}\dfrac{f(a+h)-f(a)}{h}$"
        "\n"
        r"secant slope $\;\longrightarrow\;$ tangent slope  (the $1\times1$ Jacobian)",
        fontsize=12, color="#24292f", va="top")

ax.set_xlim(-1.2, 4.2)
ax.set_ylim(-0.6, 7.4)
ax.axhline(0, color="#d0d7de", lw=0.8, zorder=0)
ax.axvline(0, color="#d0d7de", lw=0.8, zorder=0)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.legend(loc="lower right", fontsize=10, frameon=False)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}")
print(f"  a={a}, f(a)={fa:.3f}, f'(a)={fpa:.3f}, secant slope (h={h})={sec_slope:.3f}")
