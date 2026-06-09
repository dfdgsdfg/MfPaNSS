#!/usr/bin/env python3
"""Static figure for 12강 3기 11강 — the fundamental theorem of line integrals
for a gradient field (lecture §10, §11):

    f(x,y) = x^2 + y^2     (a bowl / paraboloid height function)
    F = grad f = (2x, 2y)  (the gradient vector field)

Two different paths from A=(-1.4,-0.9) to B=(1.5,1.0) and one closed loop are
drawn over the gradient field. For grad f the line integral depends only on the
endpoints:

    integral_C grad f . dr  =  f(B) - f(A)        (same for every path C),
    closed loop             =  0.

The two open paths therefore accumulate the SAME value f(B)-f(A); the closed
loop accumulates 0. Renders next to itself as an SVG embedded by the note.

Reproduce:
    uv run --with matplotlib --with numpy python \
        gradient-line-integral-path-independence-03-season-11-10.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

OUT = Path(__file__).with_suffix(".svg")


def f(x, y):
    return x ** 2 + y ** 2


def grad_f(x, y):
    return 2 * x, 2 * y


# --- background gradient field on a grid --------------------------------------
g = np.linspace(-2.0, 2.0, 11)
X, Y = np.meshgrid(g, g)
U, V = grad_f(X, Y)

# faint level circles f = const (the height function's contours)
levels = [0.5, 1.5, 3.0, 5.0, 7.5]

A = np.array([-1.4, -0.9])
B = np.array([1.5, 1.0])


def line_integral(path):
    """Numerically integrate F . dr along a sampled path (2,N)."""
    fx, fy = grad_f(path[0], path[1])
    dx = np.gradient(path[0])
    dy = np.gradient(path[1])
    return np.sum(fx * dx + fy * dy)


# Path 1: a straight segment A -> B
t = np.linspace(0, 1, 4000)
p1 = np.array([A[0] + t * (B[0] - A[0]), A[1] + t * (B[1] - A[1])])

# Path 2: a curved detour A -> B (a big arc bulging up-left)
mid = np.array([-1.6, 1.7])
p2 = np.array([
    (1 - t) ** 2 * A[0] + 2 * (1 - t) * t * mid[0] + t ** 2 * B[0],
    (1 - t) ** 2 * A[1] + 2 * (1 - t) * t * mid[1] + t ** 2 * B[1],
])

# Closed loop: a circle of radius 0.9 about (0.2, -0.1)
c = np.array([0.2, -0.1])
ang = np.linspace(0, 2 * np.pi, 4000)
loop = np.array([c[0] + 0.9 * np.cos(ang), c[1] + 0.9 * np.sin(ang)])

# numeric verification
I1, I2 = line_integral(p1), line_integral(p2)
Iloop = line_integral(loop)
exact = f(*B) - f(*A)

fig, ax = plt.subplots(figsize=(6.8, 6.2))

# gradient field arrows (faint, scaled down)
ax.quiver(X, Y, U, V, color="#9aa7b8", angles="xy", scale_units="xy",
          scale=9.0, width=0.004, alpha=0.7, zorder=1)

# level circles of f = x^2 + y^2
th = np.linspace(0, 2 * np.pi, 200)
for L in levels:
    r = np.sqrt(L)
    ax.plot(r * np.cos(th), r * np.sin(th), color="#d0d7de", lw=0.9,
            ls=(0, (4, 4)), zorder=0)

# the two open paths
ax.plot(p1[0], p1[1], color="#1f6feb", lw=2.6, zorder=4,
        label=r"path 1 (straight): $\int \nabla f\cdot d\mathbf{r}=f(B)-f(A)$")
ax.plot(p2[0], p2[1], color="#0b8457", lw=2.6, zorder=4,
        label=r"path 2 (detour): same value $f(B)-f(A)$")
# the closed loop
ax.plot(loop[0], loop[1], color="#d1242f", lw=2.4, ls=(0, (6, 3)), zorder=3,
        label=r"closed loop: $\oint \nabla f\cdot d\mathbf{r}=0$")

# arrowheads to show direction of travel
for path, color in [(p1, "#1f6feb"), (p2, "#0b8457")]:
    k = int(0.62 * path.shape[1])
    ax.add_patch(FancyArrowPatch(path[:, k - 1], path[:, k + 1],
                                 arrowstyle="-|>", mutation_scale=20,
                                 color=color, zorder=5))
k = int(0.25 * loop.shape[1])
ax.add_patch(FancyArrowPatch(loop[:, k - 1], loop[:, k + 1],
                             arrowstyle="-|>", mutation_scale=18,
                             color="#d1242f", zorder=5))

# endpoints
ax.scatter(*A, s=55, color="#24292f", zorder=6)
ax.scatter(*B, s=55, color="#24292f", zorder=6)
ax.text(A[0] - 0.12, A[1] - 0.34, r"$A$", fontsize=15, weight="bold", ha="center")
ax.text(B[0] + 0.10, B[1] + 0.10, r"$B$", fontsize=15, weight="bold")

ax.set_title(
    r"Gradient field $\nabla f=(2x,2y)$ of $f=x^2+y^2$: "
    "line integral is path-independent", fontsize=12.5)
ax.text(-2.5, -2.92,
        rf"$f(B)-f(A)={exact:.2f}$   "
        rf"(path 1 $\approx{I1:.2f}$, path 2 $\approx{I2:.2f}$, "
        rf"loop $\approx{abs(Iloop):.2f}$)",
        ha="left", fontsize=11.5, color="#24292f")

ax.set_xlim(-2.6, 2.6)
ax.set_ylim(-3.0, 2.6)
ax.set_aspect("equal")
ax.axhline(0, color="#e1e4e8", lw=0.8, zorder=0)
ax.axvline(0, color="#e1e4e8", lw=0.8, zorder=0)
ax.set_xticks([-2, -1, 0, 1, 2])
ax.set_yticks([-2, -1, 0, 1, 2])
ax.tick_params(labelsize=9)
ax.legend(loc="upper left", fontsize=8.6, framealpha=0.92)

fig.tight_layout()
fig.savefig(OUT, format="svg", bbox_inches="tight")

print(f"wrote {OUT}")
print(f"  f(B)-f(A) = {exact:.4f}")
print(f"  path1 = {I1:.4f}   path2 = {I2:.4f}   loop = {Iloop:.4f}")
