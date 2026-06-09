#!/usr/bin/env python3
"""Static figure for 17강 3기 16강 — the Central Limit Theorem punchline (lecture §10).

Two populations that are NOT bell-shaped at all (a U-shaped / arcsine population and a
heavily skewed exponential population) still produce a Gaussian when we repeatedly draw a
sample and plot the distribution of the *sample mean*. Renders next to itself as an SVG
embedded by the note.

Reproduce:  uv run --with matplotlib --with numpy python clt-sampling-distribution-03-season-16-10.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).with_suffix(".svg")
rng = np.random.default_rng(7)

N_SAMPLES = 40000   # number of repeated samplings (each gives one sample mean)
SAMPLE_N = 30       # size of one sample (drawn from the population)

# --- Population 1: U-shaped (arcsine on [0,1]) — extreme, definitely not Gaussian ---
def draw_u(size):
    return np.sin(rng.uniform(0, np.pi / 2, size)) ** 2  # arcsine-distributed on [0,1]

# --- Population 2: exponential — heavily skewed, long right tail, finite variance (CLT holds) ---
# (A power-law with exponent in (2,3) is the lecture's CLT *exception*, so we use a
#  skewed-but-finite-variance population here to honestly show "non-bell -> Gaussian mean".)
LAM = 1.0
def draw_power(size):
    return rng.exponential(1.0 / LAM, size)

xs_u = np.linspace(0.012, 0.988, 400)                      # trim the singular endpoints
pdf_u = 1.0 / (np.pi * np.sqrt(xs_u * (1 - xs_u)))          # arcsine PDF (U-shape)

xs_p = np.linspace(0, 6, 400)
pdf_p = LAM * np.exp(-LAM * xs_p)                           # exponential PDF, skewed

# --- Sample means: repeat "draw a sample of SAMPLE_N, take its mean" many times ---
means_u = draw_u((N_SAMPLES, SAMPLE_N)).mean(axis=1)
means_p = draw_power((N_SAMPLES, SAMPLE_N)).mean(axis=1)


def gaussian(x, mu, sig):
    return np.exp(-0.5 * ((x - mu) / sig) ** 2) / (np.sqrt(2 * np.pi) * sig)


fig, axes = plt.subplots(2, 2, figsize=(8.4, 6.0))
POP = "#1f6feb"
MEAN = "#0b8457"
GAUSS = "#d1242f"

# top-left: U-shaped population
ax = axes[0, 0]
ax.plot(xs_u, pdf_u, color=POP, lw=2.2)
ax.fill_between(xs_u, pdf_u, color=POP, alpha=0.12)
ax.set_title("Population A: U-shaped (NOT Gaussian)", fontsize=11)
ax.set_xlabel("x"); ax.set_ylabel("density")
ax.set_ylim(0, 3.2)

# bottom-left: distribution of the sample mean for U-shaped
ax = axes[1, 0]
ax.hist(means_u, bins=60, density=True, color=MEAN, alpha=0.55,
        label="sample-mean histogram")
mu, sig = means_u.mean(), means_u.std()
g = np.linspace(means_u.min(), means_u.max(), 300)
ax.plot(g, gaussian(g, mu, sig), color=GAUSS, lw=2.2, label="Gaussian fit")
ax.set_title(r"Distribution of $\bar{X}$  ($n=%d$)  $\to$  Gaussian" % SAMPLE_N, fontsize=11)
ax.set_xlabel(r"sample mean $\bar{X}$"); ax.set_ylabel("density")
ax.legend(fontsize=8, loc="upper right")

# top-right: power-law population
ax = axes[0, 1]
ax.plot(xs_p, pdf_p, color=POP, lw=2.2)
ax.fill_between(xs_p, pdf_p, color=POP, alpha=0.12)
ax.set_title("Population B: skewed / long tail (NOT Gaussian)", fontsize=11)
ax.set_xlabel("x"); ax.set_ylabel("density")
ax.set_ylim(0, 1.1)

# bottom-right: distribution of the sample mean for power-law
ax = axes[1, 1]
ax.hist(means_p, bins=60, density=True, color=MEAN, alpha=0.55,
        label="sample-mean histogram")
mu, sig = means_p.mean(), means_p.std()
g = np.linspace(means_p.min(), means_p.max(), 300)
ax.plot(g, gaussian(g, mu, sig), color=GAUSS, lw=2.2, label="Gaussian fit")
ax.set_title(r"Distribution of $\bar{X}$  ($n=%d$)  $\to$  Gaussian" % SAMPLE_N, fontsize=11)
ax.set_xlabel(r"sample mean $\bar{X}$"); ax.set_ylabel("density")
ax.legend(fontsize=8, loc="upper right")

fig.suptitle("Central Limit Theorem: any population's sample mean becomes Gaussian",
             fontsize=12.5, weight="bold")
for ax in axes.ravel():
    ax.grid(alpha=0.18)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}")
print(f"  U-shaped  : sample-mean mean={means_u.mean():.4f} std={means_u.std():.4f}")
print(f"  power-law : sample-mean mean={means_p.mean():.4f} std={means_p.std():.4f}")
