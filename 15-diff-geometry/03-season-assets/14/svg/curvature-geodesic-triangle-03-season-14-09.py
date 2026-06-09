#!/usr/bin/env python3
"""Static figure for 15강 3기 14강 — the three model geometries by curvature sign
and how a geodesic triangle's angle sum reads the curvature (lecture §8, §9):

    theta1 + theta2 + theta3 = pi + integral_T K dA.

Three panels: negative curvature (hyperbolic, angle sum < pi),
zero curvature (Euclidean plane, angle sum = pi),
positive curvature (sphere, angle sum > pi).

Reproduce:
  uv run --with matplotlib --with numpy python curvature-geodesic-triangle-03-season-14-09.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).with_suffix(".svg")

EDGE = "#1f6feb"
FILL = "#1f6feb"
VERT = "#24292f"
GUIDE = "#9aa7b8"

fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.2))


def interior_angles(P):
    """Sum of interior angles of a straight-edged triangle (for the flat panel)."""
    s = 0.0
    for i in range(3):
        a = P[(i - 1) % 3] - P[i]
        b = P[(i + 1) % 3] - P[i]
        c = (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))
        s += np.degrees(np.arccos(np.clip(c, -1, 1)))
    return s


# ----------------------------------------------------------------------------
# Panel 1: negative curvature K < 0 (hyperbolic) — edges bow INWARD,
# so the angle sum is strictly less than 180 deg.
# ----------------------------------------------------------------------------
ax = axes[0]
P = np.array([[0.10, 0.12], [0.90, 0.12], [0.50, 0.92]])


def bowed_edge(p, q, bulge):
    """Quadratic-Bezier-like arc bowed toward (bulge>0) or away from the centroid."""
    cen = P.mean(axis=0)
    mid = (p + q) / 2
    ctrl = mid + bulge * (cen - mid)
    t = np.linspace(0, 1, 60)[:, None]
    return (1 - t) ** 2 * p + 2 * (1 - t) * t * ctrl + t ** 2 * q


for i in range(3):
    arc = bowed_edge(P[i], P[(i + 1) % 3], 0.55)  # bow inward
    ax.plot(arc[:, 0], arc[:, 1], color=EDGE, lw=2.4, zorder=3)
ax.fill(*np.vstack([bowed_edge(P[i], P[(i + 1) % 3], 0.55) for i in range(3)]).T,
        color=FILL, alpha=0.07, zorder=1)
ax.set_title(r"$K<0$  hyperbolic", fontsize=13)
ax.text(0.5, -0.16, r"$\theta_1+\theta_2+\theta_3 < 180^\circ$",
        ha="center", fontsize=12.5, color=VERT)

# ----------------------------------------------------------------------------
# Panel 2: zero curvature K = 0 (Euclidean plane) — straight geodesics,
# angle sum exactly 180 deg.
# ----------------------------------------------------------------------------
ax = axes[1]
Pf = np.array([[0.10, 0.12], [0.90, 0.12], [0.50, 0.92]])
tri = np.vstack([Pf, Pf[0]])
ax.plot(tri[:, 0], tri[:, 1], color=EDGE, lw=2.4, zorder=3)
ax.fill(Pf[:, 0], Pf[:, 1], color=FILL, alpha=0.07, zorder=1)
ax.set_title(r"$K=0$  Euclidean plane", fontsize=13)
ax.text(0.5, -0.16, r"$\theta_1+\theta_2+\theta_3 = 180^\circ$",
        ha="center", fontsize=12.5, color=VERT)
assert abs(interior_angles(Pf) - 180.0) < 1e-6  # flat triangle: sum is exactly 180

# ----------------------------------------------------------------------------
# Panel 3: positive curvature K > 0 (sphere) — edges bow OUTWARD,
# angle sum strictly greater than 180 deg.
# ----------------------------------------------------------------------------
ax = axes[2]
Ps = np.array([[0.10, 0.12], [0.90, 0.12], [0.50, 0.92]])


def bowed_edge_s(p, q, bulge):
    cen = Ps.mean(axis=0)
    mid = (p + q) / 2
    ctrl = mid - bulge * (cen - mid)  # bow outward, away from centroid
    t = np.linspace(0, 1, 60)[:, None]
    return (1 - t) ** 2 * p + 2 * (1 - t) * t * ctrl + t ** 2 * q


# faint sphere outline to suggest a curved surface
circ = plt.Circle((0.5, 0.5), 0.52, fill=False, color=GUIDE, lw=1.0, ls=(0, (5, 4)))
ax.add_patch(circ)
for i in range(3):
    arc = bowed_edge_s(Ps[i], Ps[(i + 1) % 3], 0.45)
    ax.plot(arc[:, 0], arc[:, 1], color=EDGE, lw=2.4, zorder=3)
ax.fill(*np.vstack([bowed_edge_s(Ps[i], Ps[(i + 1) % 3], 0.45) for i in range(3)]).T,
        color=FILL, alpha=0.07, zorder=1)
ax.set_title(r"$K>0$  sphere", fontsize=13)
ax.text(0.5, -0.16, r"$\theta_1+\theta_2+\theta_3 > 180^\circ$",
        ha="center", fontsize=12.5, color=VERT)

# vertices + common styling for all panels
for ax, PP in zip(axes, (P, Pf, Ps)):
    ax.scatter(PP[:, 0], PP[:, 1], s=26, color=VERT, zorder=5)
    ax.set_xlim(-0.08, 1.08)
    ax.set_ylim(-0.30, 1.10)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

fig.suptitle(r"Geodesic triangle angle sum  $=\ \pi + \iint_T K\,dA$",
             fontsize=13.5, y=1.02)
fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")
print(f"wrote {OUT}  (flat-triangle angle sum = {interior_angles(Pf):.4f} deg)")
