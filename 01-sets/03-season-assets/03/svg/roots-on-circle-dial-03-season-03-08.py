#!/usr/bin/env python3
"""Static figure for 01강 3기 03강 — roots on a circle as a rotating "dial"
(lecture §8). The roots of x^n - 2 = 0 sit at the vertices of a regular n-gon
on the circle of radius 2^(1/n) in the complex plane; rotating by 360/n degrees
maps the set to itself. We draw n = 2, 3, 4, 5 side by side so the rotational
symmetry (180, 120, 90, 72 degrees) is visible, and flag that n = 5 is where
the dial starts to "twist" — the reason a general quintic has no radical formula.
Renders next to itself as an SVG embedded by the note.

Reproduce:  uv run --with matplotlib --with numpy python roots-on-circle-dial-03-season-03-08.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyArrowPatch

OUT = Path(__file__).with_suffix(".svg")

BLUE, RED, GREEN, GREY, INK = "#1f6feb", "#d1242f", "#0b8457", "#6e7781", "#24292f"

ns = [2, 3, 4, 5]
fig, axes = plt.subplots(1, 4, figsize=(11.4, 3.4))

for ax, n in zip(axes, ns):
    r = 2.0 ** (1.0 / n)                      # |root| of x^n - 2 = 0
    # n-th roots of 2: r * exp(2*pi*i*k/n)
    ks = np.arange(n)
    ang = 2 * np.pi * ks / n
    xs, ys = r * np.cos(ang), r * np.sin(ang)

    twist = (n == 5)
    edge = RED if twist else BLUE
    fill = "#ffe9ea" if twist else "#e7f0ff"

    # the circle the roots live on
    th = np.linspace(0, 2 * np.pi, 256)
    ax.plot(r * np.cos(th), r * np.sin(th), color=GREY, lw=1.0, ls=(0, (5, 4)),
            zorder=1)

    # the regular n-gon through the roots (closed polygon)
    poly_x = np.append(xs, xs[0])
    poly_y = np.append(ys, ys[0])
    ax.fill(poly_x, poly_y, color=fill, zorder=1)
    ax.plot(poly_x, poly_y, color=edge, lw=1.6, zorder=2)

    # the roots themselves
    ax.scatter(xs, ys, s=46, color=edge, zorder=4, edgecolors="white", linewidths=0.8)

    # rotation arc + arrow from root 0 to root 1 (the 360/n step)
    deg = 360.0 / n
    ax.add_patch(Arc((0, 0), 1.15, 1.15, angle=0, theta1=0, theta2=deg,
                     color=GREEN, lw=1.6, zorder=3))
    a_mid = np.radians(deg)
    ax.add_patch(FancyArrowPatch((0.575, 0.0),
                                 (0.575 * np.cos(a_mid), 0.575 * np.sin(a_mid)),
                                 arrowstyle="-|>", mutation_scale=12,
                                 color=GREEN, lw=1.4,
                                 connectionstyle="arc3,rad=0.35", zorder=4))
    # angle label placed just outside the arc
    lab = np.radians(deg / 2)
    ax.text(0.92 * np.cos(lab), 0.92 * np.sin(lab),
            rf"${deg:.0f}^\circ$", color=GREEN, fontsize=12, ha="center",
            va="center", weight="bold")

    ax.scatter([0], [0], s=14, color=INK, zorder=5)
    sub = "  (twist!)" if twist else ""
    title_col = RED if twist else INK
    ax.set_title(rf"$x^{{{n}}}-2=0$" + sub, fontsize=12.5, color=title_col)

    lim = 1.55
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.axhline(0, color="#d0d7de", lw=0.7, zorder=0)
    ax.axvline(0, color="#d0d7de", lw=0.7, zorder=0)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

fig.suptitle(
    r"Roots of $x^n-2=0$ on a circle: rotation by $360^\circ/n$ maps the set to itself "
    r"($n=5$ is where the dial twists)",
    fontsize=12.5, color=INK, y=1.02)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
for n in ns:
    r = 2.0 ** (1.0 / n)
    print(f"n={n}: |root|={r:.4f}, rotation step={360.0/n:.1f} deg")
print(f"wrote {OUT}")
