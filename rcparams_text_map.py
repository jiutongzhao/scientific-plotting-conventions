"""
rcparams_text_map.py
====================
A teaching diagram: which matplotlib rcParam sets the SIZE of each text element
in a figure. Every text element in the sample plot is coloured by the rcParam
that controls it (x- and y-axis labels share a colour because both are governed
by `axes.labelsize`), and a colour-matched key on the right lists the parameter
names. Data lines are kept grey so the only colour carries the text mapping.

Output: rcparams_text_map.png / .pdf
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# one distinct colour per controlling rcParam.  Hues are the SciencePlots
# "high-vis" cycle (github.com/garrettj403/SciencePlots), darkened where needed
# so small text stays legible on white; two extras (crimson, grey) round it out.
C = {
    "figure.titlesize":      "#0d49fb",   # high-vis blue
    "axes.titlesize":        "#e6091c",   # high-vis red
    "axes.labelsize":        "#8936df",   # high-vis purple  (x AND y axis labels)
    "xtick.labelsize":       "#1a9e30",   # high-vis green (darkened)
    "ytick.labelsize":       "#0e9ec4",   # high-vis cyan (darkened)
    "legend.fontsize":       "#b8860b",   # high-vis yellow (darkened to gold)
    "legend.title_fontsize": "#c2185b",   # crimson (extra)
    "font.size":             "#555555",   # grey  (extra; generic text / fallback base)
}

# exaggerated, clearly-different sizes so the hierarchy is obvious ------------
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Liberation Sans", "Helvetica", "DejaVu Sans"],
    "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
    "figure.titlesize": 19, "axes.titlesize": 15, "axes.labelsize": 13,
    "xtick.labelsize": 10.5, "ytick.labelsize": 10.5,
    "legend.fontsize": 12, "legend.title_fontsize": 12, "font.size": 11,
    "axes.linewidth": 1.0, "lines.linewidth": 2.0,
})

fig = plt.figure(figsize=(11.6, 5.7))
gs = fig.add_gridspec(1, 2, width_ratios=[1.08, 1.0], wspace=0.10,
                      left=0.06, right=0.985, top=0.86, bottom=0.12)
ax = fig.add_subplot(gs[0, 0])
key = fig.add_subplot(gs[0, 1]); key.axis("off")

# ---- sample plot: grey data, every text element coloured by its rcParam ----
x = np.linspace(0, 10, 200)
ax.plot(x, np.sin(x), color="#3a3a3a", label="signal A")
ax.plot(x, 0.7 * np.cos(x), color="#9a9a9a", ls="--", label="signal B")

ax.set_title("Axes title  ·  ax.set_title()", color=C["axes.titlesize"], fontweight="bold")
ax.set_xlabel("x-axis label (unit)", color=C["axes.labelsize"])
ax.set_ylabel("y-axis label (unit)", color=C["axes.labelsize"])
ax.tick_params(axis="both", color="#888888")
ax.tick_params(axis="x", labelcolor=C["xtick.labelsize"])
ax.tick_params(axis="y", labelcolor=C["ytick.labelsize"])
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#888888")

leg = ax.legend(title="Legend title", loc="upper right")
for t in leg.get_texts():
    t.set_color(C["legend.fontsize"])
leg.get_title().set_color(C["legend.title_fontsize"])

ax.text(0.035, 0.07, "Text annotation  ·  ax.text()", transform=ax.transAxes,
        color=C["font.size"], style="italic")

fig.suptitle("Figure title  ·  fig.suptitle()", x=0.305, y=0.965,
             color=C["figure.titlesize"], fontweight="bold")

# ---- key: parameter names in matching colours -----------------------------
key.set_xlim(0, 1); key.set_ylim(0, 1)
key.text(0.0, 1.0, "Which rcParam sets each text size", fontsize=14,
         fontweight="bold", color="#1f2a37", va="top")

rows = [
    ("figure.titlesize",       "figure title — fig.suptitle()"),
    ("axes.titlesize",         "axes title — ax.set_title()"),
    ("axes.labelsize",         "x- and y-axis labels (both)"),
    ("xtick.labelsize",        "x tick labels"),
    ("ytick.labelsize",        "y tick labels"),
    ("legend.fontsize",        "legend entries"),
    ("legend.title_fontsize",  "legend title"),
    ("font.size",              "other text; base others fall back to"),
]
y = 0.885
for param, desc in rows:
    col = C[param]
    val = mpl.rcParams[param]
    key.plot([0.0, 0.035], [y - 0.012, y - 0.012], color=col, lw=4,
             solid_capstyle="round", clip_on=False)
    key.text(0.055, y, param, color=col, fontweight="bold", fontsize=12.5,
             family="monospace", va="top")
    key.text(0.055, y - 0.045, f"{val:g} pt  →  {desc}", color=col, fontsize=10, va="top")
    y -= 0.112

key.text(0.0, -0.02,
         "Typeface of every element: font.family / font.sans-serif.\n"
         "Weights: axes.titleweight · axes.labelweight · figure.titleweight.\n"
         "Also: figure.labelsize → fig.supxlabel()/supylabel().",
         fontsize=8.6, color="#6b7280", va="top")

fig.savefig("rcparams_text_map.pdf", bbox_inches="tight", pad_inches=0.05)
fig.savefig("rcparams_text_map.png", dpi=300, bbox_inches="tight", pad_inches=0.05)
print("wrote rcparams_text_map.png and .pdf")
