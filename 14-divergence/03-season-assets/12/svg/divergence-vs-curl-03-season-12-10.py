#!/usr/bin/env python3
"""Static figure for 14강 3기 12강 — distinguishing divergence from curl on the
same kind of vector field (lecture §10). Left: a pure radial outflow field
F=(x,y), which has positive divergence (div F = 2) and zero curl. Right: a pure
rotational field F=(-y,x), which has zero divergence and positive curl
(curl F = 2). Renders next to itself as an SVG embedded by the note.

Reproduce:  uv run --with matplotlib --with numpy python divergence-vs-curl-03-season-12-10.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).with_suffix(".svg")

# grid of sample points
g = np.linspace(-2.0, 2.0, 9)
X, Y = np.meshgrid(g, g)

# two model fields
U_div, V_div = X, Y          # radial outflow:  F = (x, y)   -> div = 2, curl = 0
U_rot, V_rot = -Y, X         # rotation:        F = (-y, x)  -> div = 0, curl = 2

# analytic check (constant over the plane for these linear fields)
div_div = 1.0 + 1.0          # d/dx(x) + d/dy(y)
curl_div = 0.0 - 0.0         # d/dx(y) - d/dy(x)
div_rot = 0.0 + 0.0          # d/dx(-y) + d/dy(x)
curl_rot = 1.0 - (-1.0)      # d/dx(x) - d/dy(-y)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 5.0))


def style(ax, title, sub):
    ax.set_aspect("equal")
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-2.6, 2.6)
    ax.axhline(0, color="#d0d7de", lw=0.8, zorder=0)
    ax.axvline(0, color="#d0d7de", lw=0.8, zorder=0)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(title, fontsize=13, weight="bold")
    ax.text(0, -3.15, sub, ha="center", va="top", fontsize=11.5, color="#24292f")


# left: divergence (radial outflow)
axL.quiver(X, Y, U_div, V_div, color="#1f6feb", angles="xy",
           scale_units="xy", scale=2.4, width=0.007, zorder=4)
# small dashed circle to suggest "flux out of a box/loop"
circ = plt.Circle((0, 0), 1.1, fill=False, color="#6e7781", lw=1.3, ls=(0, (5, 4)))
axL.add_patch(circ)
axL.scatter([0], [0], s=22, color="#d1242f", zorder=6)
style(axL, "Divergence:  F = (x, y)",
      r"div F $= \partial_x x + \partial_y y = %g$,   curl F $= %g$"
      % (div_div, curl_div) + "\n(net flow OUT through the loop)")

# right: curl (rotation)
axR.quiver(X, Y, U_rot, V_rot, color="#0b8457", angles="xy",
           scale_units="xy", scale=2.4, width=0.007, zorder=4)
circ2 = plt.Circle((0, 0), 1.1, fill=False, color="#6e7781", lw=1.3, ls=(0, (5, 4)))
axR.add_patch(circ2)
axR.scatter([0], [0], s=22, color="#d1242f", zorder=6)
style(axR, "Curl:  F = (-y, x)",
      r"div F $= %g$,   curl F $= \partial_x x - \partial_y(-y) = %g$"
      % (div_rot, curl_rot) + "\n(net circulation AROUND the loop)")

fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}")
print(f"radial field  F=(x,y):   div={div_div:g}, curl={curl_div:g}")
print(f"rotation field F=(-y,x): div={div_rot:g}, curl={curl_rot:g}")
