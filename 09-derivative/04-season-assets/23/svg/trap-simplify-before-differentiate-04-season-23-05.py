#!/usr/bin/env python3
"""Static figure for 09강 4기 23강 — the "trap" problem of lecture §5:
"어려운 문제가 아니라 어려운 답". The intimidating expression
    f(x) = sqrt(sin^2 x) + ln(e^(2x))
collapses, on x in [0, pi] where sin x >= 0, to the simple line-plus-wave
    f(x) = sin x + 2x,
whose derivative is f'(x) = cos x + 2 > 0 (always increasing).
The point: simplify first, then differentiate.

Reproduce:  uv run --with matplotlib --with numpy python trap-simplify-before-differentiate-04-season-23-05.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).with_suffix(".svg")

# Domain where sqrt(sin^2 x) = |sin x| = sin x  (sin x >= 0)
x = np.linspace(0, np.pi, 400)

# "Scary" form, evaluated literally, and the simplified form — they coincide here.
f_literal = np.sqrt(np.sin(x) ** 2) + np.log(np.exp(2 * x))   # = |sin x| + 2x
f_simple = np.sin(x) + 2 * x                                  # = sin x + 2x
fprime = np.cos(x) + 2                                        # f'(x) = cos x + 2

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.4))

# ---- Left: the function, scary form vs. simplified form ----
ax1.plot(x, f_literal, color="#d1242f", lw=6, alpha=0.30,
         label=r"$\sqrt{\sin^2 x}+\ln(e^{2x})$  (as written)")
ax1.plot(x, f_simple, color="#1f6feb", lw=2.0,
         label=r"$\sin x + 2x$  (simplified)")
ax1.set_title(r"$f(x)=\sqrt{\sin^2 x}+\ln(e^{2x})=\sin x+2x$",
              fontsize=12)
ax1.set_xlabel(r"$x$")
ax1.set_ylabel(r"$f(x)$")
ax1.legend(loc="upper left", fontsize=9.5, framealpha=0.9)
ax1.grid(True, color="#e1e4e8", lw=0.7)
ax1.set_xlim(0, np.pi)
ax1.set_xticks([0, np.pi / 2, np.pi])
ax1.set_xticklabels(["0", r"$\pi/2$", r"$\pi$"])

# ---- Right: the derivative cos x + 2 ----
ax2.plot(x, fprime, color="#0b8457", lw=2.2,
         label=r"$f'(x)=\cos x + 2$")
ax2.axhline(0, color="#959da5", lw=0.9)
ax2.fill_between(x, 0, fprime, color="#0b8457", alpha=0.10)
ax2.set_title(r"$f'(x)=\cos x + 2 > 0$  (always increasing)",
              fontsize=12)
ax2.set_xlabel(r"$x$")
ax2.set_ylabel(r"$f'(x)$")
ax2.legend(loc="upper right", fontsize=10, framealpha=0.9)
ax2.grid(True, color="#e1e4e8", lw=0.7)
ax2.set_xlim(0, np.pi)
ax2.set_ylim(0, 3.2)
ax2.set_xticks([0, np.pi / 2, np.pi])
ax2.set_xticklabels(["0", r"$\pi/2$", r"$\pi$"])

fig.suptitle("Simplify first, then differentiate  (a hard answer, not a hard problem)",
             fontsize=12.5, y=1.0)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")

# sanity check: the two forms agree on [0, pi]
err = np.max(np.abs(f_literal - f_simple))
print(f"wrote {OUT}  (max|literal-simplified| on [0,pi] = {err:.2e}, "
      f"f'>0 everywhere: {bool(np.all(fprime > 0))})")
