"""
size_samples.py
===============
Render the seven common panel grids — 1x1, 1x2, 1x3, 2x2, 2x3, 2x4, 3x3 —
each through the sizes/ patch that serves it, stacked on paper.mplstyle:

  height = width x 0.618 (golden) x rows/cols

so grids with the same rows:cols ratio share one patch file, and four files
cover all seven grids:

  * paper-double          (7.087 x 4.38) — 1x1, 2x2, 3x3
  * paper-double-2x3      (7.087 x 2.92) — 2x3
  * paper-double-1x2      (7.087 x 2.19) — 1x2, 2x4
  * paper-double-1x3      (7.087 x 1.46) — 1x3

Outputs size_sample_<rows>x<cols>.png/.pdf per grid, plus the two slide-size
samples (slides-half, slides-full) on slides.mplstyle. All PNGs export at the
same dpi (300): embedded together, their pixel sizes preserve the true
physical-size ratios.
"""
from fractions import Fraction

import numpy as np
import matplotlib.pyplot as plt

from style_samples import ROOT, OUT, DPI, demo

GRIDS = [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (2, 4), (3, 3)]
SQUARE_GRIDS = [(2, 2), (2, 3)]   # two representative square-panel demos

# rows:cols ratio -> the one patch that serves every grid with that ratio
PATCH_BY_RATIO = {
    Fraction(1, 1): "paper-double",
    Fraction(2, 3): "paper-double-2x3",
    Fraction(1, 2): "paper-double-1x2",
    Fraction(1, 3): "paper-double-1x3",
}
# same classes for SQUARE panels (panel_aspect = 1 instead of golden);
# use together with ax.set_box_aspect(1)
SQUARE_PATCH_BY_RATIO = {
    ratio: patch.replace("paper-double", "paper-double-square")
    for ratio, patch in PATCH_BY_RATIO.items()
}


def panel(ax, k):
    """One small panel: a phase-shifted damped sine + a bold panel letter."""
    x = np.linspace(0, 4 * np.pi, 300)
    ax.plot(x, np.exp(-x / 9) * np.sin(x + k * np.pi / 3), color=f"C{k % 6}")
    ax.text(0.05, 0.92, chr(ord("a") + k), transform=ax.transAxes,
            fontsize=8, fontweight="bold", va="top",
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
    ax.set_ylim(-1.15, 1.15)


def render_grid(rows, cols, square=False):
    table = SQUARE_PATCH_BY_RATIO if square else PATCH_BY_RATIO
    patch = table[Fraction(rows, cols)]
    slug = f"square_{rows}x{cols}" if square else f"{rows}x{cols}"
    styles = [str(ROOT / "paper.mplstyle"), str(ROOT / "sizes" / f"{patch}.mplstyle")]
    with plt.style.context(styles):
        fig, axs = plt.subplots(rows, cols, squeeze=False, sharex=True, sharey=True)
        for k, ax in enumerate(axs.flat):
            panel(ax, k)
            if square:
                ax.set_box_aspect(1)   # the patch budgets the height for this
        for ax in axs[-1, :]:
            ax.set_xlabel("Time (s)")
        for ax in axs[:, 0]:
            ax.set_ylabel("Amplitude (a.u.)")
        fig.savefig(OUT / f"size_sample_{slug}.pdf")
        fig.savefig(OUT / f"size_sample_{slug}.png", dpi=DPI)
        size = tuple(round(v, 3) for v in fig.get_size_inches())
        plt.close(fig)
    print(f"wrote size_sample_{slug}.png/.pdf  ({patch}, {size} in @ {DPI} dpi)")


def render_slides(patch):
    styles = [str(ROOT / "slides.mplstyle"), str(ROOT / "sizes" / f"{patch}.mplstyle")]
    with plt.style.context(styles):
        fig, ax = plt.subplots()
        demo(ax)
        fig.savefig(OUT / f"size_sample_{patch}.pdf")
        fig.savefig(OUT / f"size_sample_{patch}.png", dpi=DPI)
        size = tuple(round(v, 3) for v in fig.get_size_inches())
        plt.close(fig)
    print(f"wrote size_sample_{patch}.png/.pdf  (slides + {patch}, {size} in @ {DPI} dpi)")


if __name__ == "__main__":
    for rows, cols in GRIDS:
        render_grid(rows, cols)
    for rows, cols in SQUARE_GRIDS:
        render_grid(rows, cols, square=True)
    for patch in ("slides-half", "slides-full"):
        render_slides(patch)
