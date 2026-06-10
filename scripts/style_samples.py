"""
style_samples.py
================
Render the SAME plot through each bundled style sheet, so the README can show
what paper.mplstyle and slides.mplstyle actually look like:

  * style_sample_paper.png/.pdf  — paper.mplstyle  (3.4645 x 3.4645 in, 6 pt)
  * style_sample_slides.png/.pdf — slides.mplstyle (6.8 x 4.2 in, 18 pt)

Both PNGs are saved at the SAME dpi (300) so that, embedded side by side, their
pixel sizes preserve the true physical-size ratio between the two figures —
the size difference IS the message (design at final size for the medium).
"""
from pathlib import Path

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)

DPI = 300   # equal for both exports (overrides each style's own savefig.dpi)


def demo(ax):
    """One plot, drawn identically under either style — every visible
    difference between the two outputs comes from the style sheet."""
    x = np.linspace(0, 4 * np.pi, 400)
    env = np.exp(-x / 9)
    ax.plot(x, env * np.sin(x), label="signal")
    ax.plot(x, env * np.cos(x), label="quadrature")
    ax.plot(x[::25], env[::25], marker="o", label="envelope")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude (a.u.)")
    ax.set_ylim(-1.1, 1.45)            # headroom for the frameless legend
    ax.legend(loc="upper right", ncols=1)


def render(style_file, slug):
    with plt.style.context(str(ROOT / style_file)):
        fig, ax = plt.subplots()       # the style's own figsize — no override
        demo(ax)
        fig.savefig(OUT / f"style_sample_{slug}.pdf")
        fig.savefig(OUT / f"style_sample_{slug}.png", dpi=DPI)
        size = tuple(round(v, 3) for v in fig.get_size_inches())
        plt.close(fig)
    print(f"wrote style_sample_{slug}.png/.pdf  ({style_file}, {size} in @ {DPI} dpi)")


if __name__ == "__main__":
    render("paper.mplstyle", "paper")
    render("slides.mplstyle", "slides")
