#!/usr/bin/env python3
"""Static figure for 17. The Beauty of Geometry in Statistics-03강 3기 17강 — the
correspondence between normal distributions and points of the upper half-plane
(lecture §6). Left: several bell curves P_{mu,sigma}. Right: each curve becomes the
point (mu, sigma) in the upper half-plane {sigma > 0}. Renders next to itself as an
SVG embedded by the note.

Reproduce:  uv run --with matplotlib --with numpy python normal-to-half-plane-03-season-17-06.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

OUT = Path(__file__).with_suffix(".svg")


def normal(x, mu, sigma):
    return 1.0 / (np.sqrt(2 * np.pi) * sigma) * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))


# four normal distributions: (mu, sigma, color, label)
dists = [
    (-1.5, 0.5, "#1f6feb", r"$(\mu,\sigma)=(-1.5,\,0.5)$"),
    (0.0, 0.5, "#0b8457", r"$(0,\,0.5)$"),
    (0.0, 1.2, "#9a4dff", r"$(0,\,1.2)$"),
    (1.8, 0.9, "#d1242f", r"$(1.8,\,0.9)$"),
]

fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.0, 5.0),
                               gridspec_kw={"width_ratios": [1.05, 1.0]})

# ---- left panel: the bell curves themselves --------------------------------
x = np.linspace(-4.5, 4.5, 600)
for mu, sigma, color, _ in dists:
    y = normal(x, mu, sigma)
    axL.plot(x, y, color=color, lw=2.2)
    axL.fill_between(x, y, color=color, alpha=0.07)
    # mark the peak (at x = mu)
    axL.plot([mu], [normal(mu, mu, sigma)], "o", color=color, ms=5)

axL.set_title(r"Normal distributions $P_{\mu,\sigma}(x)"
              r"=\frac{1}{\sqrt{2\pi}\,\sigma}e^{-(x-\mu)^2/2\sigma^2}$",
              fontsize=12)
axL.set_xlabel(r"$x$", fontsize=12)
axL.set_ylabel("density", fontsize=11)
axL.axhline(0, color="#d0d7de", lw=0.8)
axL.set_xlim(-4.5, 4.5)
axL.set_ylim(-0.03, 0.9)
axL.spines[["top", "right"]].set_visible(False)

# ---- right panel: the upper half-plane of parameters -----------------------
axR.axhspan(0, 3.0, color="#eef3f8", zorder=0)            # the region sigma > 0
axR.axhline(0, color="#24292f", lw=1.6, zorder=2)         # boundary sigma = 0
for mu, sigma, color, label in dists:
    axR.plot([mu], [sigma], "o", color=color, ms=10, zorder=5)
    axR.annotate(label, (mu, sigma), textcoords="offset points",
                 xytext=(8, 8), fontsize=10, color=color)

# illustrate the hyperbolic metric ds^2 = (dmu^2 + dsigma^2)/sigma^2:
# the SAME coordinate step in mu is "longer" where sigma is small.
# draw a unit-mu bar low (small sigma) and high (large sigma).
for sigma0, note in [(0.5, "small  $\\sigma$:\nsame $\\Delta\\mu$ = LARGE distance"),
                     (2.2, "large  $\\sigma$:\nsame $\\Delta\\mu$ = small distance")]:
    x0 = -3.2
    axR.add_patch(FancyArrowPatch((x0, sigma0), (x0 + 1.0, sigma0),
                                  arrowstyle="<->", mutation_scale=12,
                                  lw=1.2 + 2.0 / sigma0, color="#57606a", zorder=4))
    axR.text(x0 - 0.05, sigma0 + 0.18, note, fontsize=8.5, color="#57606a")

axR.set_title(r"Upper half-plane $\mathbb{H}^2=\{(\mu,\sigma):\sigma>0\}$"
              "\n" r"metric $ds^2=(d\mu^2+d\sigma^2)/\sigma^2$",
              fontsize=12)
axR.set_xlabel(r"$\mu$  (mean)", fontsize=12)
axR.set_ylabel(r"$\sigma$  (std. dev.)", fontsize=12)
axR.set_xlim(-4.5, 4.5)
axR.set_ylim(-0.25, 3.0)
axR.spines[["top", "right"]].set_visible(False)

# big mapping arrow between panels
fig.text(0.505, 0.5, r"$P_{\mu,\sigma}\;\longleftrightarrow\;(\mu,\sigma)$",
         ha="center", va="center", fontsize=13, color="#24292f")

fig.suptitle("Each normal distribution = one point of the upper half-plane",
             fontsize=13, weight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}")
# sanity check: densities integrate to ~1
xx = np.linspace(-30, 30, 20000)
for mu, sigma, _, _ in dists:
    area = np.trapezoid(normal(xx, mu, sigma), xx)
    print(f"  (mu={mu:+.1f}, sigma={sigma:.1f}) integral = {area:.4f}")
