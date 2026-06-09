#!/usr/bin/env python3
"""Static figure for 05강 4기 12강 — injective / surjective / bijective maps
between finite sets (lecture §3). Three side-by-side set-to-set arrow diagrams
make the definitions visible: injective = no two arrows share a target,
surjective = every target is hit, bijective = both. Renders next to itself as
an SVG embedded by the note.

Reproduce:  uv run --with matplotlib --with numpy python injective-surjective-bijective-04-season-12-03.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch

OUT = Path(__file__).with_suffix(".svg")

BLUE, RED, GREEN, GREY, INK = "#1f6feb", "#d1242f", "#0b8457", "#9aa7b8", "#24292f"

fig, axes = plt.subplots(1, 3, figsize=(11.2, 4.4))


def panel(ax, title, subtitle, A, B, edges, hit_color):
    """Draw a left set A and right set B with the given arrows (edges)."""
    xa, xb = 0.0, 1.0
    # element y-positions, evenly spread and vertically centered
    def ys(n):
        return list(np.linspace(0.78, 0.22, n))
    ya, yb = ys(len(A)), ys(len(B))
    pa = {a: (xa, ya[i]) for i, a in enumerate(A)}
    pb = {b: (xb, yb[i]) for i, b in enumerate(B)}

    # which targets are actually hit
    targets_hit = {t for _, t in edges}

    # set boundaries (ovals)
    ax.add_patch(Ellipse((xa, 0.5), 0.46, 0.92, fill=False, ec=GREY, lw=1.6))
    ax.add_patch(Ellipse((xb, 0.5), 0.46, 0.92, fill=False, ec=GREY, lw=1.6))
    ax.text(xa, 1.02, r"$A$", ha="center", fontsize=14, color=INK, weight="bold")
    ax.text(xb, 1.02, r"$B$", ha="center", fontsize=14, color=INK, weight="bold")

    # nodes
    for a, (x, y) in pa.items():
        ax.scatter([x], [y], s=140, color=INK, zorder=4)
        ax.text(x - 0.12, y, a, ha="right", va="center", fontsize=12, color=INK)
    for b, (x, y) in pb.items():
        c = hit_color if b in targets_hit else "#c4ccd6"
        ax.scatter([x], [y], s=140, color=c, zorder=4)
        ax.text(x + 0.12, y, b, ha="left", va="center", fontsize=12, color=INK)

    # arrows f: A -> B
    for s, t in edges:
        x0, y0 = pa[s]
        x1, y1 = pb[t]
        ax.add_patch(FancyArrowPatch((x0 + 0.045, y0), (x1 - 0.045, y1),
                                     arrowstyle="-|>", mutation_scale=13,
                                     lw=1.6, color=BLUE, shrinkA=0, shrinkB=0,
                                     zorder=3))

    ax.text(0.5, -0.07, title, ha="center", fontsize=13.5, color=INK, weight="bold")
    ax.text(0.5, -0.205, subtitle, ha="center", fontsize=10.5, color="#57606a")
    ax.set_xlim(-0.45, 1.45)
    ax.set_ylim(-0.30, 1.12)
    ax.set_aspect("equal")
    ax.axis("off")


# (1) injective, not surjective: distinct inputs -> distinct outputs, but b4 unhit
panel(axes[0], "injective",
      r"$a\neq a' \Rightarrow f(a)\neq f(a')$",
      ["a1", "a2", "a3"], ["b1", "b2", "b3", "b4"],
      [("a1", "b1"), ("a2", "b2"), ("a3", "b3")], GREEN)

# (2) surjective, not injective: every b hit, but b2 hit twice
panel(axes[1], "surjective",
      r"$\forall b\,\exists a:\ f(a)=b$",
      ["a1", "a2", "a3", "a4"], ["b1", "b2", "b3"],
      [("a1", "b1"), ("a2", "b2"), ("a3", "b2"), ("a4", "b3")], GREEN)

# (3) bijective = injective AND surjective: 1-to-1 correspondence
panel(axes[2], "bijective (1-to-1)",
      "injective + surjective",
      ["a1", "a2", "a3"], ["b1", "b2", "b3"],
      [("a1", "b2"), ("a2", "b1"), ("a3", "b3")], GREEN)

fig.suptitle(r"$f:A\to B$ — injective vs. surjective vs. bijective",
             fontsize=14, color=INK, y=1.0)
fig.tight_layout(rect=(0, 0, 1, 0.97))
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}")
