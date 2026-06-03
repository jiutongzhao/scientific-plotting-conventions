"""
slide_layout.py
===============
A to-scale schematic of a presentation slide, drawn in the same visual language
as the per-publisher page layouts (publisher_page_layouts.py) — but for a talk
instead of a journal page. It shows a 16:9 slide with:

  * the slide at its true 13.33 x 7.5 in size, with a dashed content/safe area;
  * a big slide title and a few short bullets (the slide rules: one idea, big type);
  * a large sample figure that FILLS the content area, with thick lines and big
    labels (the print-vs-slide contrast);
  * coloured tags calling out the slide-scale type sizes (title 28-40 pt, body /
    axis text 18-24 pt, data lines 1.5-3 pt);
  * width and height dimension lines annotating the 13.33 x 7.5 in canvas.

Output: slide_layout.png / .pdf
"""
from pathlib import Path

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(exist_ok=True)

# data colour cycle: SciencePlots "high-vis" (github.com/garrettj403/SciencePlots)
HIGHVIS = ["#0d49fb", "#e6091c", "#26eb47", "#8936df", "#fec32d", "#25d7fd"]
mpl.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Liberation Sans", "Helvetica", "DejaVu Sans"],
})

INK, SUB, ACCENT = "#1f2a37", "#6b7280", "#2563b8"
T_BLUE, T_ORNG = "#0a4f7a", "#8a6000"
PAPER_EC, AREA_EC = "#c9cfd6", "#cdd5dd"

SW, SH = 13.33, 7.5            # 16:9 slide, inches


def slide_plot(ax):
    """A slide-scale sample figure: thick lines, big markers, large labels."""
    x = np.linspace(0, 10, 120)
    ax.plot(x, np.sin(x) + 0.14 * x, lw=2.7, marker="o", markevery=18, ms=7,
            color=HIGHVIS[0], label="model")
    ax.plot(x, 0.6 * np.cos(x) + 0.10 * x, lw=2.7, ls=(0, (4, 2)), marker="s",
            markevery=18, ms=6, color=HIGHVIS[1], label="data")
    ax.set_xlabel("Time (s)", fontsize=11, color=INK)
    ax.set_ylabel("Signal (a.u.)", fontsize=11, color=INK)
    ax.tick_params(labelsize=9, length=4, width=1.0, color="#9aa1a9", labelcolor=INK)
    ax.legend(fontsize=10, frameon=False, loc="upper left", handlelength=1.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#9aa1a9"); ax.spines[s].set_linewidth(1.0)
    ax.locator_params(nbins=5)


def render():
    x0c, x1c, y0c, y1c = -1.9, 15.5, -2.3, 10.4
    FAC = 0.47
    fig, ax = plt.subplots(figsize=((x1c - x0c) * FAC, (y1c - y0c) * FAC))
    ax.set_xlim(x0c, x1c); ax.set_ylim(y0c, y1c)
    ax.set_aspect("equal"); ax.axis("off")

    # ---- slide: drop shadow, white face, faint template bar -----------------
    ax.add_patch(Rectangle((0.16, -0.16), SW, SH, facecolor="#0b1320",
                           alpha=0.06, ec="none", zorder=0))
    ax.add_patch(Rectangle((0, 0), SW, SH, facecolor="white", ec=PAPER_EC,
                           lw=1.2, zorder=1))
    ax.add_patch(Rectangle((0, SH - 0.16), SW, 0.16, facecolor=ACCENT,
                           alpha=0.18, ec="none", zorder=2))

    # dashed content / safe area
    mx = 0.55
    ax.add_patch(Rectangle((mx, 0.6), SW - 2 * mx, SH - 1.05, facecolor="none",
                           ec=AREA_EC, lw=0.9, ls=(0, (4, 3)), zorder=2))

    # ---- title + tags --------------------------------------------------------
    ax.text(mx + 0.05, SH - 0.55, "One clear message", fontsize=16,
            fontweight="bold", color=INK, va="top", zorder=4)
    ax.add_line(Line2D([mx + 0.05, mx + 4.3], [SH - 1.28, SH - 1.28],
                       color=ACCENT, lw=1.8, solid_capstyle="round", zorder=3))
    ax.text(mx + 0.05, SH - 1.55, "slide title · 28–40 pt", fontsize=6.6,
            color=T_BLUE, fontweight="bold", va="top", zorder=4)

    # ---- bullets -------------------------------------------------------------
    bullets = ["Big type, thick lines", "One idea per slide",
               "High contrast, little clutter"]
    by = SH - 2.75
    for k, b in enumerate(bullets):
        ax.plot([mx + 0.13], [by - 0.02], marker="o", ms=6.5,
                color=HIGHVIS[k % len(HIGHVIS)], zorder=4)
        ax.text(mx + 0.5, by, b, fontsize=9, color=INK, va="center", ha="left", zorder=4)
        by -= 0.95
    ax.text(mx + 0.05, 1.05, "body & axis text · 18–24 pt", fontsize=6.6,
            color=SUB, fontweight="bold", va="top", zorder=4)

    # ---- the figure fills the content area ----------------------------------
    fx0, fy0, fw, fh = 5.55, 0.85, 7.25, 4.55
    sub = ax.inset_axes([fx0, fy0, fw, fh], transform=ax.transData)
    sub.set_zorder(3); slide_plot(sub)
    ax.text(fx0, fy0 + fh + 0.5, "figure fills the content area · data lines 1.5–3 pt",
            fontsize=6.6, color=T_ORNG, fontweight="bold", va="bottom", zorder=4)

    # ---- dimension lines (the canvas size) ----------------------------------
    ap = dict(arrowstyle="<|-|>", color=ACCENT, lw=1.0, mutation_scale=10,
              shrinkA=0, shrinkB=0)
    ax.annotate("", (0, -0.95), (SW, -0.95), arrowprops=ap, zorder=5)
    for xx in (0, SW):
        ax.plot([xx, xx], [0, -0.95], color=ACCENT, lw=0.7, zorder=5)
    ax.text(SW / 2, -1.15, "13.33 in  ·  16:9", ha="center", va="top",
            fontsize=8, color=ACCENT, fontweight="bold")

    ax.annotate("", (-0.95, 0), (-0.95, SH), arrowprops=ap, zorder=5)
    for yy in (0, SH):
        ax.plot([0, -0.95], [yy, yy], color=ACCENT, lw=0.7, zorder=5)
    ax.text(-1.25, SH / 2, "7.5 in", ha="center", va="center", rotation=90,
            fontsize=8, color=ACCENT, fontweight="bold")

    # ---- header + caption ----------------------------------------------------
    ax.text(0, SH + 2.55, "Presentation slide", fontsize=13, fontweight="bold",
            color=INK, va="top", ha="left")
    ax.text(0, SH + 1.55, "16:9 · 13.33 × 7.5 in   (4:3 alternative: 10 × 7.5 in)",
            fontsize=5.6, color=SUB, va="top", ha="left")
    ax.text(0, SH + 1.0, "design at final size · big type · thick lines · high contrast",
            fontsize=5.6, color=SUB, va="top", ha="left")

    ax.text(SW / 2, -1.85,
            "Don't shrink a print figure onto a slide — rebuild it at slide scale: "
            "one idea, fonts ~18–40 pt, lines 1.5–3 pt, strong contrast.",
            ha="center", va="top", fontsize=6.2, color=SUB)

    fig.savefig(OUT / "slide_layout.pdf", bbox_inches="tight", pad_inches=0.05)
    fig.savefig(OUT / "slide_layout.png", dpi=300, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print("wrote slide_layout.png and .pdf")


if __name__ == "__main__":
    render()
