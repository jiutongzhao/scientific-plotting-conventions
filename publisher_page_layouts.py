"""
publisher_page_layouts.py
=========================
A 2x3 to-scale schematic of how figures and text sit on the page across
publishers: A4 journals on the top row, US-Letter on the bottom row.

Each page shows, at the publisher's true column width:
  * paper size, margins / text area (left-margin dimension, left-aligned);
  * a REAL full-width and part-width figure (sample data, legend, axis labels)
    whose drawing area is inset so the axis labels stay INSIDE the column;
    every publisher uses a DIFFERENT figure aspect ratio (w : h shown in the tag);
  * a figure CAPTION under each panel, in that publisher's house format;
  * body TEXT, greeked: only the FIRST paragraph is real (with a "9 pt" tag),
    the rest are rules.

Type is rendered roughly to scale, so the relative sizes (title 16 > body 9 >
caption 8 > axis label 7 pt) are faithful. The top-right panel sets the SAME
words and formula in three typefaces (Arial / Times New Roman / Computer Modern),
aligned on a grid, across Large/Regular/Small + italic/bold/math rows.

A geometric self-check at the end flags any label/text/figure overlap.
Output: .pdf (vector, embedded fonts) and .png (400 dpi).
"""
import textwrap
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib.font_manager import FontProperties, findfont

WONG = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#56B4E9", "#CC79A7"]
# inset fonts are sized to scale (7 pt axis label < 9 pt body, etc.)
mpl.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Liberation Sans", "Helvetica", "DejaVu Sans"],
    "font.size": 3.0,
    "axes.labelsize": 2.7, "xtick.labelsize": 2.3, "ytick.labelsize": 2.3,
    "legend.fontsize": 2.6,
    "axes.linewidth": 0.45, "lines.linewidth": 0.8, "lines.markersize": 2.2,
    "axes.prop_cycle": mpl.cycler(color=WONG),
})

INK, SUB, ACCENT = "#1f2a37", "#6b7280", "#2563b8"
W_BLUE, W_ORNG = "#0072B2", "#E69F00"
T_BLUE, T_ORNG = "#0a4f7a", "#8a6000"
PAPER_EC, TEXT_EC = "#c9cfd6", "#cdd5dd"
BODY_C, GREEK_C, CAP_C = "#565c64", "#c3c9d0", "#3b424b"
rng = np.random.default_rng(4)

FP_TIMES = FontProperties(fname=findfont("Times New Roman"))
FP_TIMES_I = FontProperties(family="Times New Roman", style="italic")
FP_TIMES_B = FontProperties(family="Times New Roman", weight="bold")
FP_ARIAL = FontProperties(fname=findfont("Arial"))
FP_ARIAL_I = FontProperties(family="Arial", style="italic")
FP_ARIAL_B = FontProperties(family="Arial", weight="bold")
FP_CM = FontProperties(fname=findfont("cmr10"))
FP_CMB = FontProperties(fname=findfont("cmb10"))


# ---------- sample plots (short y-labels so labels fit inside the column) ----
# translucent white legend box + extra head-room so legends never hide the data
LG = dict(frameon=True, framealpha=0.78, facecolor="white", edgecolor="none",
          borderpad=0.2, handletextpad=0.3, handlelength=1.0)


def _tidy(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#9aa1a9")
    ax.tick_params(length=1.2, width=0.4, pad=0.7)
    ax.locator_params(axis="x", nbins=4)
    ax.locator_params(axis="y", nbins=3)
    ax.xaxis.labelpad = 1.2
    ax.yaxis.labelpad = 1.2


def p_ts(ax):
    x = np.linspace(0, 12, 120)
    for k, lab in enumerate(["α", "β", "γ"]):
        ax.plot(x, np.sin(x + k) / (1 + .2 * k) + .12 * k, label=lab)
    ax.set(xlabel="Time (s)", ylabel="Value", ylim=(-1.25, 2.15))
    ax.legend(loc="upper center", ncol=3, columnspacing=0.7, **LG)
    _tidy(ax)


def p_scatter(ax):
    for k in range(2):
        x = rng.normal(k * 1.3, 1, 26); y = x * .6 + rng.normal(0, .7, 26)
        ax.scatter(x, y, s=4, alpha=.8, label=f"g{k+1}", edgecolor="none")
    ax.set(xlabel="x (a.u.)", ylabel="y")
    ax.margins(x=0.05, y=0.22)
    ax.legend(loc="lower right", **LG)
    _tidy(ax)


def p_bar(ax):
    xc = np.arange(4)
    ax.bar(xc - .18, rng.uniform(.4, 1, 4), .36, label="ctrl")
    ax.bar(xc + .18, rng.uniform(.4, 1, 4), .36, label="treat")
    ax.set(xlabel="Condition", ylabel="Count", ylim=(0, 1.75))
    ax.set_xticks(xc); ax.set_xticklabels(["A", "B", "C", "D"])
    ax.legend(loc="upper center", ncol=2, columnspacing=0.8, **LG)
    _tidy(ax)


def p_sine(ax):
    x = np.linspace(0, 2 * np.pi, 160)
    ax.plot(x, np.sin(x), label="sin")
    ax.plot(x, np.cos(x), ls=(0, (3, 2)), label="cos")
    ax.set(xlabel="Phase (rad)", ylabel="Amp.", ylim=(-1.5, 2.05))
    ax.legend(loc="upper center", ncol=2, columnspacing=0.8, **LG)
    _tidy(ax)


def p_band(ax):
    x = np.linspace(0, 10, 90); m = np.sin(x) * np.exp(-x / 12)
    sd = .12 + .04 * np.cos(x)
    ax.fill_between(x, m - sd, m + sd, alpha=.25, color=W_BLUE, lw=0, label="±s.d.")
    ax.plot(x, m, color=W_BLUE, label="mean")
    ax.set(xlabel="Time (s)", ylabel="Signal")
    ax.margins(y=0.2)
    ax.legend(loc="lower right", ncol=2, columnspacing=0.8, **LG)
    _tidy(ax)


def p_area(ax):
    x = np.linspace(0, 10, 60)
    a = .5 + .4 * np.sin(x / 2) ** 2; b = .4 + .3 * np.cos(x / 3) ** 2
    ax.stackplot(x, a, b, labels=["U", "V"], colors=WONG[2:4], alpha=.85)
    ax.set(xlabel="Time (s)", ylabel="Frac.", ylim=(0, 2.5))
    ax.legend(loc="upper center", ncol=2, columnspacing=0.7, **LG)
    _tidy(ax)


def mini(ax, kind):
    """A compact, label-free sub-panel plot for multi-panel figures."""
    k = kind % 4
    if k == 0:
        x = np.linspace(0, 6, 50)
        ax.plot(x, np.sin(x)); ax.plot(x, np.cos(x), ls=(0, (3, 2)))
        ax.set_ylim(-1.4, 1.4)
    elif k == 1:
        for j in range(2):
            xx = rng.normal(j * .9, .7, 14)
            ax.scatter(xx, xx * .5 + rng.normal(0, .5, 14), s=2.2, edgecolor="none")
    elif k == 2:
        ax.bar(np.arange(4), rng.uniform(.4, 1, 4), .62)
    else:
        x = np.linspace(0, 6, 40); m = np.sin(x) * np.exp(-x / 8)
        ax.fill_between(x, m - .12, m + .12, alpha=.3, color=W_BLUE, lw=0)
        ax.plot(x, m, color=W_BLUE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#9aa1a9"); ax.spines[s].set_linewidth(0.4)
    ax.set_xticks([]); ax.set_yticks([])


BODY = ("We introduce a compact, well-formatted figure and evaluate it across "
        "several conditions. The trend shown in the panel agrees with theory and "
        "improves on the baseline. Shaded regions and error bars give one standard "
        "deviation across repeats.")

CAPTXT2 = "Shaded band shows mean ± s.d."
CAPTXT1 = "Sample data; n = 8 per group."


def cap_segs(name, n, body):
    B, P = "bold", "normal"
    if name == "Nature":
        return [(f"Fig. {n} | ", B), ("Sample panel. ", B), (body, P)]
    if name == "ACS":
        return [(f"Figure {n}. ", B), (body, P)]
    if name == "Springer":
        return [(f"Fig. {n} ", B), (body, P)]
    if name.startswith("IEEE"):
        return [(f"Fig. {n}. ", P), (body, P)]
    return [(f"Fig. {n}. ", B), (body, P)]


# name, paper, w, h, single, double, ncol, double_fn, single_fn, verified, heading
pubs = [
    ("Nature",         "A4",     210, 297, 88,   180, 2, p_ts,    p_bar,     True,  "Introduction"),
    ("Elsevier",       "A4",     210, 297, 90,   190, 2, p_scatter, p_sine,  True,  "Results"),
    ("Springer",       "A4",     210, 297, 84,   174, 2, p_band,  p_scatter, False, "Methods"),
    ("IEEE",           "Letter", 216, 279, 88.9, 182, 2, p_area,  p_bar,     True,  "Results"),
    ("Wiley",          "Letter", 216, 279, 84,   176, 1, p_ts,    p_sine,    False, "Discussion"),
    ("Science (AAAS)", "Letter", 216, 279, 55,   183, 3, p_band,  p_scatter, False, "Analysis"),
]

# per-publisher figure aspect ratios (w:h) — (full-width fig, part-/single-col fig)
# every value is distinct so the panels visibly differ in shape
ASPECT = {
    "Nature":         ((4, 1), (4, 3)),
    "Elsevier":       ((7, 2), (3, 2)),
    "Springer":       ((3, 1), (5, 4)),
    "IEEE":           ((5, 1), (16, 9)),
    "Wiley":          ((9, 2), (1, 1)),
    "Science (AAAS)": ((11, 3), (2, 1)),
}

# per-publisher panel-label house style: (case, parenthesis, bold, position)
PANELSTYLE = {
    "Nature":         ("lower", "none", True,  "tl"),     # bold  a
    "Elsevier":       ("lower", "()",   False, "tl"),     #       (a)
    "Springer":       ("lower", "()",   True,  "tl"),     # bold  (a)
    "IEEE":           ("lower", "()",   False, "below"),  #       (a)  under panel
    "Wiley":          ("upper", "()",   False, "tl"),     #       (A)
    "Science (AAAS)": ("upper", "none", True,  "tl"),     # bold  A
}


def panel_text(i, case, paren):
    ch = chr((65 if case == "upper" else 97) + i)
    if paren == "()":
        return f"({ch})"
    if paren == ")":
        return f"{ch})"
    return ch

MT, MB = 24, 22
PL, PB, PR, PT_ = 18, 9, 2, 3             # inset paddings: keep axis labels in column
PWMAX, PHMAX = 216, 297
GAPX, GAPY = 40, 72
YB = [PHMAX - 18 + GAPY, 0]

fig, ax = plt.subplots(figsize=(14.5, 14.8))
ax.set_aspect("equal"); ax.axis("off")
CHECKS = []                      # (tag, inset, col_left, col_right) -> labels in column
BODYBOX = []                     # (page, real-text, col_left, col_right)
STRUCT = []                      # (page, text)  structural labels for overlap audit
INSETS = []                      # (page, axes)  figures for overlap audit
HDRS = []                        # publisher-name headers
CAPS = []                        # deferred caption requests (need a renderer to lay out)
CUR = [0]                        # current page index
REAL = [False]                   # has the one real paragraph been shown on this page?


def fill_body(x0, ytop, ybot, colw_mm, fs=3.4, lh=3.9, size_tag=None):
    """Greeked body: ONLY the first paragraph on the page is real text; every
    later paragraph is light rules. `size_tag` is printed after the real lines."""
    L = textwrap.wrap(BODY, max(14, int(colw_mm * 0.55)))
    y = ytop
    while y > ybot:
        real = not REAL[0]
        plen = int(rng.integers(5, 9))
        for k in range(plen):
            if y <= ybot:
                return
            last = k == plen - 1
            if real and k < 2:                                   # 2 real opening lines
                t = ax.text(x0, y, L[k % len(L)], fontsize=fs, va="top", ha="left",
                            color=BODY_C, zorder=2)
                BODYBOX.append((CUR[0], t, x0, x0 + colw_mm))
                REAL[0] = True
            elif real and k == 2 and size_tag:                   # in-place size tag
                tg = ax.text(x0, y, size_tag, fontsize=3.0, va="top", ha="left",
                             color=ACCENT, style="italic", zorder=2)
                STRUCT.append((CUR[0], tg))
            else:                                                # rule (greeked line)
                frac = rng.uniform(0.36, 0.6) if last else rng.uniform(0.9, 1.0)
                yr = y - lh * 0.45
                ax.add_line(Line2D([x0, x0 + colw_mm * frac], [yr, yr], lw=1.3,
                                   color=GREEK_C, solid_capstyle="round", zorder=2))
            y -= lh
        y -= 2.4


def S(idx, *a, **k):
    t = ax.text(*a, **k)
    STRUCT.append((idx, t))
    return t


def draw_page(idx, col, row, name, paper, PW, PH, single, double, ncol, dfn, sfn, ok, heading):
    CUR[0] = idx; REAL[0] = False
    X0, Yb = col * (PWMAX + GAPX), YB[row]
    gx = lambda x: X0 + x
    gy = lambda y: Yb + y
    ML = (PW - double) / 2
    gut = (double - ncol * single) / (ncol - 1) if ncol > 1 else 0.0

    ax.add_patch(Rectangle((gx(2.4), gy(-2.4)), PW, PH, facecolor="#0b1320",
                           alpha=0.06, ec="none", zorder=0))
    ax.add_patch(Rectangle((gx(0), gy(0)), PW, PH, facecolor="white",
                           ec=PAPER_EC, lw=1.0, zorder=1))

    tx0, tx1, ty0, ty1 = ML, PW - ML, MB, PH - MT
    ax.add_patch(Rectangle((gx(tx0), gy(ty0)), tx1 - tx0, ty1 - ty0,
                 facecolor="none", ec=TEXT_EC, lw=0.8, ls=(0, (4, 3)), zorder=2))
    cols = [tx0 + j * (single + gut) for j in range(ncol)]
    one = ncol == 1
    bodyw = (tx1 - tx0) if one else single
    fx1 = tx0 + ((tx1 - tx0) - single) / 2 if one else cols[0]
    (adw, adh), (asw, ash) = ASPECT[name]                       # figure aspect ratios
    dwid = (tx1 - tx0) - PL - PR                                # full-width drawing box
    h2 = dwid * adh / adw + PB + PT_                            # -> slot height
    swid = single - PL - PR                                     # part-width drawing box
    h1 = swid * ash / asw + PB + PT_
    d_tag = (f"full width · {double:g} mm · {adw}:{adh}" if one
             else f"2-column · {double:g} mm · {adw}:{adh}")
    s_tag = (f"part width · {single:g} mm · {asw}:{ash}" if one
             else f"1-col · {single:g} mm · {asw}:{ash}")

    # ---- vertical stack, top-down with explicit gaps and caption slots ---------
    y_title = ty1
    S(idx, gx(tx0), gy(y_title), "Sample Article Title", fontsize=6.0,
      fontweight="bold", color=INK, va="top", zorder=4)
    y_tag2 = y_title - 7.5
    S(idx, gx(tx0), gy(y_tag2), d_tag, fontsize=4.4, color=T_BLUE,
      fontweight="bold", va="top", zorder=4)

    fig2_top = y_tag2 - 5.0
    fig2_bot = fig2_top - h2
    # full-width figure = a row of sub-panels with journal-styled panel labels (a-d)
    npan, pgap = 4, 3.0
    prow_h = h2 - PB - PT_
    pw = (dwid - (npan - 1) * pgap) / npan
    case, paren, bold, pos = PANELSTYLE[name]
    fw = "bold" if bold else "normal"
    for pi in range(npan):
        px = tx0 + PL + pi * (pw + pgap)
        sub = ax.inset_axes([gx(px), gy(fig2_bot + PB), pw, prow_h], transform=ax.transData)
        sub.set_zorder(3); mini(sub, pi)
        INSETS.append((idx, sub)); CHECKS.append((f"{name} p{pi}", sub, X0 + tx0, X0 + tx1))
        lab = panel_text(pi, case, paren)
        if pos == "below":
            sub.text(0.5, -0.12, lab, transform=sub.transAxes, ha="center", va="top",
                     fontsize=4.2, fontweight=fw, color=INK, clip_on=False)
        else:
            sub.text(0.06, 0.93, lab, transform=sub.transAxes, ha="left", va="top",
                     fontsize=4.2, fontweight=fw, color=INK, clip_on=False)
    y_cap1 = fig2_bot - 3.0
    CAPS.append((idx, gx(tx0), gy(y_cap1), tx1 - tx0, cap_segs(name, 1, CAPTXT2), False))

    y_head = fig2_bot - 10
    S(idx, gx(tx0), gy(y_head), heading, fontsize=4.7, fontweight="bold",
      color=INK, va="top", zorder=4)
    y_b1 = y_head - 6.5
    y_tag1 = y_b1 - 24
    fill_body(gx(tx0), gy(y_b1), gy(y_tag1 + 6), bodyw, size_tag="↑ body text — 9 pt")

    S(idx, gx(fx1), gy(y_tag1), s_tag, fontsize=4.4, color=T_ORNG,
      fontweight="bold", va="top", zorder=4)
    fig1_top = y_tag1 - 5.0
    fig1_bot = fig1_top - h1
    sa = ax.inset_axes([gx(fx1 + PL), gy(fig1_bot + PB),
                        swid, h1 - PB - PT_], transform=ax.transData)
    sa.set_zorder(3); sfn(sa)
    CHECKS.append((name + " 1-col", sa, X0 + fx1, X0 + fx1 + single)); INSETS.append((idx, sa))
    y_cap2 = fig1_bot - 3.0
    CAPS.append((idx, gx(fx1), gy(y_cap2), single, cap_segs(name, 2, CAPTXT1),
                 one or name.startswith("IEEE")))
    fill_body(gx(tx0), gy(y_cap2 - 5.5), gy(MB), bodyw)
    for j in range(1, ncol):
        fill_body(gx(cols[j]), gy(y_head), gy(MB), single)

    # left-margin dimension arrow, LEFT-ALIGNED label inside the page
    ym = ty1 + 10
    ax.annotate("", (gx(0), gy(ym)), (gx(ML), gy(ym)), zorder=5,
                arrowprops=dict(arrowstyle="<|-|>", color=ACCENT, lw=0.8,
                                mutation_scale=7, shrinkA=0, shrinkB=0))
    S(idx, gx(0), gy(ym) + 3.0, f"{ML:.0f} mm", ha="left", va="bottom",
      fontsize=5.2, color=ACCENT)

    # publisher name — uniform colour, close to the page
    HDRS.append(ax.text(gx(PW / 2), gy(PH) + 6, name, ha="center", va="bottom",
                fontsize=10.0, fontweight="bold", color=INK))
    S(idx, gx(PW / 2), gy(0) - 11, f"{paper} · {PW:g} × {PH:g} mm", ha="center",
      va="top", fontsize=6.8, color=INK, fontweight="bold")
    _info = "single-column text" if one else f"{ncol}-column · gutter {gut:.0f} mm"
    S(idx, gx(PW / 2), gy(0) - 20, _info, ha="center", va="top", fontsize=6.0, color=SUB)


for i, p in enumerate(pubs):
    draw_page(i, i % 3, i // 3, *p)

totalW = 3 * PWMAX + 2 * GAPX
top = YB[0] + PHMAX
ax.set_xlim(-16, totalW + 16)
ax.set_ylim(-60, top + 108)

# ---- header: title + subtitles + representative type sizes (left) ------------
LEFTT = [
    ax.text(-16, top + 96, "Paper size, margins, figures & typefaces — to scale across publishers",
            fontsize=14, fontweight="bold", color=INK, va="top"),
    ax.text(-16, top + 80, "Top row A4, bottom row US Letter. Real full- and part-width figures "
            "(a different aspect ratio per publisher), axis labels kept inside the column.",
            fontsize=8.5, color=SUB, va="top"),
    ax.text(-16, top + 71, "Body text is greeked — only the first paragraph is real; each figure "
            "caption follows that journal's house style.", fontsize=8.5, color=SUB, va="top"),
    ax.text(-16, top + 60, "Type shown to scale —  article title 16 pt  ·  body 9 pt  ·  "
            "caption 8 pt  ·  axis label 7 pt", fontsize=7.4, color=ACCENT, va="top",
            fontweight="bold"),
]

# ---- typeface specimen (top-right): aligned grid, same text & formula --------
_tsx = totalW - 200
KEY = [ax.text(_tsx, top + 99, "Three typefaces — same text & formula",
               fontsize=6.5, fontweight="bold", color=INK, va="top", ha="left")]
_speccols = [("Arial",           FP_ARIAL, FP_ARIAL_I, FP_ARIAL_B, "stixsans"),
             ("Times New Roman", FP_TIMES, FP_TIMES_I, FP_TIMES_B, "stix"),
             ("Computer Modern", FP_CM,    None,        FP_CMB,    "cm")]
_rows = [("Large · 12 pt", 7.4, "reg"), ("Regular · 9 pt", 5.6, "reg"),
         ("Small · 7 pt", 4.3, "reg"), ("italic", 5.6, "ital"),
         ("bold", 5.6, "bold"), ("math", 6.3, "math")]
TXT, FORMULA = "Sample 0123", r"$E=mc^2$"
_yhdr = top + 86                                       # header-row centre
for _cj, (_nm, _reg, _ital, _bold, _mset) in enumerate(_speccols):
    _cx = _tsx + 36 + _cj * 56
    KEY.append(ax.text(_cx, _yhdr, _nm, fontproperties=_bold, fontsize=6.0,
                       color=INK, va="center", ha="left"))
    for _ri, (_lab, _fs, _kind) in enumerate(_rows):
        _ry = _yhdr - 12 - _ri * 8.0                  # row centre (vertical align)
        if _cj == 0:
            KEY.append(ax.text(_tsx, _ry, _lab, fontsize=4.5, color=SUB,
                               va="center", ha="left", style="italic"))
        if _kind in ("reg",):
            KEY.append(ax.text(_cx, _ry, TXT, fontproperties=_reg, fontsize=_fs,
                               color=INK, va="center", ha="left"))
        elif _kind == "bold":
            KEY.append(ax.text(_cx, _ry, TXT, fontproperties=_bold, fontsize=_fs,
                               color=INK, va="center", ha="left"))
        elif _kind == "ital":
            if _ital is not None:
                KEY.append(ax.text(_cx, _ry, TXT, fontproperties=_ital, fontsize=_fs,
                                   color=INK, va="center", ha="left"))
            else:
                KEY.append(ax.text(_cx, _ry, r"$Sample\ 0123$", math_fontfamily="cm",
                                   fontsize=_fs, color=INK, va="center", ha="left"))
        else:
            KEY.append(ax.text(_cx, _ry, FORMULA, math_fontfamily=_mset, fontsize=_fs,
                               color=INK, va="center", ha="left"))

# ---- bottom legend + footnote -----------------------------------------------
ly = -38
leg = [(W_ORNG, "-", "part-/single-column figure"),
       (W_BLUE, "-", "full-width figure"),
       (TEXT_EC, "dash", "text area (margins)"),
       (GREEK_C, "rule", "greeked body text")]
for lx, (color, kind, label) in zip([70, 250, 410, 560], leg):
    ax.plot([lx, lx + 11], [ly, ly], color=color,
            lw=(3 if kind == "-" else (1.3 if kind == "rule" else 1.0)),
            ls=("-" if kind != "dash" else (0, (4, 3))), solid_capstyle="round")
    ax.text(lx + 15, ly, label, va="center", ha="left", fontsize=9, color=INK)

ax.text(-16, -51, "Type sizes are shown roughly to scale (title 16 pt down to axis label 7 pt); "
        "column widths verified for Nature / Elsevier / IEEE, others representative. Figures use a "
        "different aspect ratio per publisher (w : h on each panel) and panel labels (a, (a), (A), "
        "A …) in each journal's house style. Always confirm with the target journal.",
        fontsize=6.6, color=SUB, va="top")


# ---- lay out the deferred captions now that a renderer exists ----------------
def render_captions(R):
    inv = ax.transData.inverted()

    def dataw(px):
        return inv.transform((px, 0))[0] - inv.transform((0, 0))[0]

    for page, x0, y, maxw, segs, center in CAPS:
        widths = []
        for txt, w in segs:
            tmp = ax.text(0, -1e4, txt, fontsize=3.2, fontweight=w)
            widths.append(dataw(tmp.get_window_extent(R).width)); tmp.remove()
        sx = x0 + max(0.0, (maxw - sum(widths)) / 2) if center else x0
        for (txt, w), dw in zip(segs, widths):
            t = ax.text(sx, y, txt, fontsize=3.2, fontweight=w, va="top", ha="left",
                        color=CAP_C, zorder=4)
            STRUCT.append((page, t)); sx += dw


fig.canvas.draw()
render_captions(fig.canvas.get_renderer())
fig.canvas.draw()
R = fig.canvas.get_renderer()
_inv = ax.transData.inverted()


def _dx(px):
    return _inv.transform((px, 0))[0]


def _ov(a, b, pad=1.0):
    p = pad / (R.points_to_pixels(1) / 0.728)
    return a.x0 < b.x1 - p and b.x0 < a.x1 - p and a.y0 < b.y1 - p and b.y0 < a.y1 - p


_bad = []
for _tag, _ins, _L, _Rr in CHECKS:
    _bb = _ins.get_tightbbox(R)
    if _dx(_bb.x0) < _L - 0.6 or _dx(_bb.x1) > _Rr + 0.6:
        _bad.append((_tag, f"[{_dx(_bb.x0):.1f},{_dx(_bb.x1):.1f}] vs [{_L:.1f},{_Rr:.1f}]"))
print("LABELS OUTSIDE COLUMN:", "none ✓" if not _bad else _bad)

_bodybad = [(t.get_text()[:14], round(_dx(t.get_window_extent(R).x1), 1), round(r, 1))
            for _i, t, l, r in BODYBOX if _dx(t.get_window_extent(R).x1) > r + 0.8]
print("BODY TEXT OVERFLOWING COLUMN:", "none ✓" if not _bodybad else _bodybad[:8])

import collections as _co
_cnt = _co.Counter()
for _i, t, l, r in BODYBOX:
    _cnt[_i] += 1
print("real body lines per page:", [_cnt[k] for k in range(6)])
print("  -> every page has its real paragraph:",
      "ok ✓" if len(_cnt) == 6 and min(_cnt.values()) >= 2 else "MISSING ✗")

_kb = min(k.get_window_extent(R).y0 for k in KEY)
_ht = max(h.get_window_extent(R).y1 for h in HDRS)
print("SPECIMEN clears publisher headers:",
      "ok ✓" if _kb > _ht else f"OVERLAP ✗ key={_kb:.0f} hdr={_ht:.0f}")
_lr = max(t.get_window_extent(R).x1 for t in LEFTT)
print("TITLE clears specimen:", "ok ✓" if _dx(_lr) < _tsx else f"OVERLAP ✗ {_dx(_lr):.0f}>{_tsx}")

_sp, _ip, _bp = _co.defaultdict(list), _co.defaultdict(list), _co.defaultdict(list)
for _i, a in STRUCT:
    _sp[_i].append(a)
for _i, a in INSETS:
    _ip[_i].append(a)
for _i, t, l, r in BODYBOX:
    _bp[_i].append(t)
_prob = []
for _i in range(6):
    Sx = [(s, s.get_window_extent(R)) for s in _sp[_i]]
    Ix = [(a, a.get_tightbbox(R)) for a in _ip[_i]]
    Bx = [(t, t.get_window_extent(R)) for t in _bp[_i]]
    for a in range(len(Sx)):
        for b in range(a + 1, len(Sx)):
            if _ov(Sx[a][1], Sx[b][1]):
                _prob.append((_i, "struct/struct", Sx[a][0].get_text()[:12], Sx[b][0].get_text()[:12]))
    for s, sb in Sx:
        for _a, ab in Ix:
            if _ov(sb, ab):
                _prob.append((_i, "struct/figure", s.get_text()[:14]))
    for t, tb in Bx:
        for _a, ab in Ix:
            if _ov(tb, ab, 0.4):
                _prob.append((_i, "body/figure", t.get_text()[:12]))
        for s, sb in Sx:
            if _ov(tb, sb, 0.4):
                _prob.append((_i, "body/struct", t.get_text()[:10], s.get_text()[:10]))
print("PAIRWISE OVERLAPS:", "none ✓" if not _prob else f"{len(_prob)} found")
for _p in _prob[:24]:
    print("   ", _p)

fig.savefig("publisher_page_layouts.pdf", bbox_inches="tight", pad_inches=0.15)
fig.savefig("publisher_page_layouts.png", dpi=400, bbox_inches="tight", pad_inches=0.15)
print("wrote publisher_page_layouts.pdf and .png")
