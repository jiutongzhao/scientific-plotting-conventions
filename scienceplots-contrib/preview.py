"""
preview.py
==========
Render the proposed SciencePlots additions stacked on the REAL SciencePlots
base styles (from the local clone, by file path), so the previews show
exactly what a SciencePlots user would get:

  plt.style.use(['science', 'no-latex', <patch>])

Outputs land in preview/. Also verifies the two non-visual claims:
  * size patches: saved PNG pixel size == figsize x dpi (bbox 'standard'
    overrides science's 'tight');
  * editable-text: PDF embeds TrueType (Type 42) fonts, not Type 3.
"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE / "preview"
OUT.mkdir(exist_ok=True)

SP = Path.home() / "Code/SciencePlots/src/scienceplots/styles"
BASE = [str(SP / "science.mplstyle"), str(SP / "misc/no-latex.mplstyle")]


def patch(name):
    p = HERE / f"{name}.mplstyle"
    if not p.exists():
        p = HERE / "sizes" / f"{name}.mplstyle"
    return str(p)


def panel(ax, k):
    x = np.linspace(0, 4 * np.pi, 300)
    ax.plot(x, np.exp(-x / 9) * np.sin(x + k * np.pi / 3), color=f"C{k % 6}")
    ax.text(0.05, 0.92, chr(ord("a") + k), transform=ax.transAxes,
            fontsize=8, fontweight="bold", va="top",
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
    ax.set_ylim(-1.15, 1.15)


def demo(ax):
    x = np.linspace(0, 4 * np.pi, 400)
    env = np.exp(-x / 9)
    ax.plot(x, env * np.sin(x), label="signal")
    ax.plot(x, env * np.cos(x), label="quadrature")
    ax.plot(x, env, marker="o", markevery=40, label="envelope")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude (a.u.)")
    ax.set_ylim(-1.1, 1.45)
    ax.legend(loc="upper right")


def check_px(png, dpi):
    img = Image.open(png)
    return f"{img.size[0]}x{img.size[1]} px @ {dpi} dpi = " \
           f"{img.size[0] / dpi:.3f} x {img.size[1] / dpi:.3f} in"


def render_grid(rows, cols, name, square=False, extra=None):
    patches = [patch(name)] + ([patch(e) for e in extra] if extra else [])
    slug = "_".join([name] + (extra or []))
    with plt.style.context(BASE + patches):
        fig, axs = plt.subplots(rows, cols, squeeze=False, sharex=True, sharey=True)
        for k, ax in enumerate(axs.flat):
            panel(ax, k)
            if square:
                ax.set_box_aspect(1)
        for ax in axs[-1, :]:
            ax.set_xlabel("Time (s)")
        for ax in axs[:, 0]:
            ax.set_ylabel("Amplitude (a.u.)")
        png = OUT / f"grid_{slug}.png"
        fig.savefig(png, dpi=300)
        size = tuple(round(v, 3) for v in fig.get_size_inches())
        plt.close(fig)
    print(f"{png.name:32s} figsize {size} -> {check_px(png, 300)}")


def render_slides(extra=None):
    styles = BASE + [patch("slides")] + ([patch(extra)] if extra else [])
    slug = extra or "slides-default"
    with plt.style.context(styles):
        fig, ax = plt.subplots()
        if extra == "slides-third":
            # third-width = one idea per figure: a single curve, no legend
            x = np.linspace(0, 4 * np.pi, 400)
            ax.plot(x, np.exp(-x / 9) * np.sin(x))
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Amplitude (a.u.)")
        else:
            demo(ax)
        png = OUT / f"slides_{slug}.png"
        fig.savefig(png)          # slides style sets savefig.dpi: 300
        size = tuple(round(v, 3) for v in fig.get_size_inches())
        plt.close(fig)
    print(f"{png.name:32s} figsize {size} -> {check_px(png, 300)}")


def render_legend(with_patch):
    styles = BASE + ([patch("short-legend")] if with_patch else [])
    slug = "with-patch" if with_patch else "plain"
    with plt.style.context(styles):
        fig, ax = plt.subplots(figsize=(3.5, 2.625))
        demo(ax)
        png = OUT / f"legend_{slug}.png"
        fig.savefig(png, dpi=300)
        plt.close(fig)
    print(f"{png.name:32s} legend.labelcolor = "
          f"{'linecolor' if with_patch else 'black (default)'}")


def check_fonttype():
    for with_patch in (False, True):
        styles = BASE + ([patch("editable-text")] if with_patch else [])
        with plt.style.context(styles):
            fig, ax = plt.subplots(figsize=(3.5, 2.625))
            demo(ax)
            pdf = OUT / f"fonttype_{'42' if with_patch else 'default'}.pdf"
            fig.savefig(pdf)
            plt.close(fig)
        raw = pdf.read_bytes()
        # Type 42 lands in PDF as a composite TrueType font: /Type0 + /CIDFontType2
        kinds = [k for k in ("Type3", "TrueType", "CIDFontType2", "Type1")
                 if f"/{k}".encode() in raw]
        print(f"{pdf.name:32s} embedded font subtype(s): {', '.join(kinds)}")


if __name__ == "__main__":
    render_grid(2, 3, "2x3")
    render_grid(2, 3, "2x3", extra=["fontsize"])   # same size, journal-scale text
    render_grid(1, 2, "1x2")
    render_grid(2, 3, "2x3-square", square=True)
    for width in ("slides-full", "slides-half", "slides-third"):
        render_slides(width)
    render_legend(False)
    render_legend(True)
    check_fonttype()
