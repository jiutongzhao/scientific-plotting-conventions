"""
publisher_page_layouts.py
=========================
Renders ONE to-scale page-layout figure per publisher (so each is large and
legible), plus a standalone three-typeface specimen. Each per-publisher figure
shows that journal's page at true column widths, with:

  * paper size & margins (left-margin dimension, left-aligned);
  * a full-width MULTI-PANEL figure (a-d) with panel labels in the journal's
    house style, and a part-/single-column figure — each at a distinct aspect
    ratio (w:h printed on the panel tag);
  * a caption under each figure in the journal's house format;
  * greeked body text (only the first paragraph is real);
  * a heading line listing the publisher's single/full widths, aspect ratios
    and panel-label style.

Type is rendered to scale, so title > heading > body > caption > axis-label
sizes are faithful. A geometric self-check flags any overlap.

Outputs (per publisher):  layout_<slug>.png / .pdf
Output (specimen):        typeface_specimen.png / .pdf
"""
import textwrap
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib.font_manager import FontProperties, findfont

# data colour cycle: SciencePlots "high-vis" style (github.com/garrettj403/SciencePlots)
HIGHVIS = ["#0d49fb", "#e6091c", "#26eb47", "#8936df", "#fec32d", "#25d7fd"]
mpl.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Liberation Sans", "Helvetica", "DejaVu Sans"],
    "font.size": 3.0,
    "axes.labelsize": 2.7, "xtick.labelsize": 2.3, "ytick.labelsize": 2.3,
    "legend.fontsize": 2.6,
    "axes.linewidth": 0.45, "lines.linewidth": 0.8, "lines.markersize": 2.2,
    "axes.prop_cycle": mpl.cycler(color=HIGHVIS),
})

INK, SUB, ACCENT = "#1f2a37", "#6b7280", "#2563b8"
W_BLUE, W_ORNG = "#0d49fb", "#e6091c"   # high-vis blue / red
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

LG = dict(frameon=True, framealpha=0.78, facecolor="white", edgecolor="none",
          borderpad=0.2, handletextpad=0.3, handlelength=1.0)


# ---------- sample plots ------------------------------------------------------
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
    ax.stackplot(x, a, b, labels=["U", "V"], colors=HIGHVIS[2:4], alpha=.85)
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
    "Nature":         ("lower", "none", True,  "tl"),
    "Elsevier":       ("lower", "()",   False, "tl"),
    "Springer":       ("lower", "()",   True,  "tl"),
    "IEEE":           ("lower", "()",   False, "below"),
    "Wiley":          ("upper", "()",   False, "tl"),
    "Science (AAAS)": ("upper", "none", True,  "tl"),
}


def panel_text(i, case, paren):
    ch = chr((65 if case == "upper" else 97) + i)
    return f"({ch})" if paren == "()" else ch


def panel_desc(name):
    case, paren, bold, pos = PANELSTYLE[name]
    ch = "A" if case == "upper" else "a"
    s = f"({ch})" if paren == "()" else ch
    if bold:
        s = "bold " + s
    if pos == "below":
        s += " (below panels)"
    return s


MT, MB = 24, 22
PL, PB, PR, PT_ = 18, 9, 2, 3

CHECKS, BODYBOX, STRUCT, INSETS, CAPS = [], [], [], [], []
CUR, REAL = [0], [False]
ax = fig = None                     # reassigned per figure


def fill_body(x0, ytop, ybot, colw_mm, fs=3.4, lh=3.9, size_tag=None):
    L = textwrap.wrap(BODY, max(14, int(colw_mm * 0.55)))
    y = ytop
    while y > ybot:
        real = not REAL[0]
        plen = int(rng.integers(5, 9))
        for k in range(plen):
            if y <= ybot:
                return
            last = k == plen - 1
            if real and k < 2:
                t = ax.text(x0, y, L[k % len(L)], fontsize=fs, va="top", ha="left",
                            color=BODY_C, zorder=2)
                BODYBOX.append((CUR[0], t, x0, x0 + colw_mm))
                REAL[0] = True
            elif real and k == 2 and size_tag:
                tg = ax.text(x0, y, size_tag, fontsize=3.0, va="top", ha="left",
                             color=ACCENT, style="italic", zorder=2)
                STRUCT.append((CUR[0], tg))
            else:
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


def draw_page(idx, X0, Yb, name, paper, PW, PH, single, double, ncol, dfn, sfn, ok, heading):
    CUR[0] = idx
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
    (adw, adh), (asw, ash) = ASPECT[name]
    dwid = (tx1 - tx0) - PL - PR
    h2 = dwid * adh / adw + PB + PT_
    swid = single - PL - PR
    h1 = swid * ash / asw + PB + PT_
    d_tag = (f"full width · {double:g} mm · {adw}:{adh}" if one
             else f"2-column · {double:g} mm · {adw}:{adh}")
    s_tag = (f"part width · {single:g} mm · {asw}:{ash}" if one
             else f"1-col · {single:g} mm · {asw}:{ash}")

    y_title = ty1
    S(idx, gx(tx0), gy(y_title), "Sample Article Title", fontsize=6.0,
      fontweight="bold", color=INK, va="top", zorder=4)
    y_tag2 = y_title - 7.5
    S(idx, gx(tx0), gy(y_tag2), d_tag, fontsize=4.4, color=T_BLUE,
      fontweight="bold", va="top", zorder=4)

    fig2_top = y_tag2 - 5.0
    fig2_bot = fig2_top - h2
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
    sa = ax.inset_axes([gx(fx1 + PL), gy(fig1_bot + PB), swid, h1 - PB - PT_], transform=ax.transData)
    sa.set_zorder(3); sfn(sa)
    CHECKS.append((name + " 1-col", sa, X0 + fx1, X0 + fx1 + single)); INSETS.append((idx, sa))
    y_cap2 = fig1_bot - 3.0
    CAPS.append((idx, gx(fx1), gy(y_cap2), single, cap_segs(name, 2, CAPTXT1),
                 one or name.startswith("IEEE")))
    fill_body(gx(tx0), gy(y_cap2 - 5.5), gy(MB), bodyw)
    for j in range(1, ncol):
        fill_body(gx(cols[j]), gy(y_head), gy(MB), single)

    ym = ty1 + 10
    ax.annotate("", (gx(0), gy(ym)), (gx(ML), gy(ym)), zorder=5,
                arrowprops=dict(arrowstyle="<|-|>", color=ACCENT, lw=0.8,
                                mutation_scale=7, shrinkA=0, shrinkB=0))
    S(idx, gx(0), gy(ym) + 3.0, f"{ML:.0f} mm", ha="left", va="bottom",
      fontsize=5.2, color=ACCENT)

    S(idx, gx(PW / 2), gy(0) - 11, f"{paper} · {PW:g} × {PH:g} mm", ha="center",
      va="top", fontsize=6.8, color=INK, fontweight="bold")
    _info = "single-column text" if one else f"{ncol}-column · gutter {gut:.0f} mm"
    S(idx, gx(PW / 2), gy(0) - 20, _info, ha="center", va="top", fontsize=6.0, color=SUB)


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


def audit(label):
    """Geometric self-check for the current figure, in data (mm) coordinates."""
    fig.canvas.draw()
    R = fig.canvas.get_renderer()
    inv = ax.transData.inverted()

    def dbox(art, tight=False):
        bb = art.get_tightbbox(R) if tight else art.get_window_extent(R)
        (x0, y0) = inv.transform((bb.x0, bb.y0)); (x1, y1) = inv.transform((bb.x1, bb.y1))
        return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))

    def ov(a, b, pad=0.5):
        return a[0] < b[2] - pad and b[0] < a[2] - pad and a[1] < b[3] - pad and b[1] < a[3] - pad

    probs = []
    for tag, ins, L, Rr in CHECKS:                       # axis labels stay in column
        bb = dbox(ins, tight=True)
        if bb[0] < L - 0.6 or bb[2] > Rr + 0.6:
            probs.append(f"{tag}: label out of column")
    for _i, t, l, r in BODYBOX:                           # body text fits its column
        if dbox(t)[2] > r + 0.8:
            probs.append(f"body overflow: {t.get_text()[:14]}")
    if len([1 for _i, *_ in BODYBOX]) < 2:
        probs.append("real paragraph missing")
    Sx = [(s, dbox(s)) for _i, s in STRUCT]               # pairwise overlap audit
    Ix = [(a, dbox(a, tight=True)) for _i, a in INSETS]
    Bx = [(t, dbox(t)) for _i, t, l, r in BODYBOX]
    for a in range(len(Sx)):
        for b in range(a + 1, len(Sx)):
            if ov(Sx[a][1], Sx[b][1]):
                probs.append(f"struct/struct: {Sx[a][0].get_text()[:10]} / {Sx[b][0].get_text()[:10]}")
    for s, sb in Sx:
        for _a, ab in Ix:
            if ov(sb, ab):
                probs.append(f"struct/figure: {s.get_text()[:12]}")
    for t, tb in Bx:
        for _a, ab in Ix:
            if ov(tb, ab, 0.4):
                probs.append(f"body/figure: {t.get_text()[:10]}")
        for s, sb in Sx:
            if ov(tb, sb, 0.4):
                probs.append(f"body/struct: {t.get_text()[:8]} / {s.get_text()[:8]}")
    print(f"  {label:16s} {'OK ✓' if not probs else str(len(probs)) + ' ISSUE(S): ' + '; '.join(probs[:6])}")
    return probs


def render_publisher(i):
    global ax, fig
    name, paper, PW, PH, single, double, ncol, dfn, sfn, ok, heading = pubs[i]
    for L in (CHECKS, BODYBOX, STRUCT, INSETS, CAPS):
        L.clear()
    CUR[0] = i; REAL[0] = False
    (adw, adh), (asw, ash) = ASPECT[name]
    x0c, x1c, y0c, y1c = -6, PW + 8, -27, PH + 33
    FAC = 0.0215
    fig, ax = plt.subplots(figsize=((x1c - x0c) * FAC, (y1c - y0c) * FAC))
    ax.set_xlim(x0c, x1c); ax.set_ylim(y0c, y1c)
    ax.set_aspect("equal"); ax.axis("off")

    draw_page(i, 0, 0, name, paper, PW, PH, single, double, ncol, dfn, sfn, ok, heading)
    S(i, 0, PH + 31, name, fontsize=12, fontweight="bold", color=INK, va="top", ha="left")
    S(i, 0, PH + 16.5, f"single {single:g} mm · full {double:g} mm · figures {adw}:{adh} & {asw}:{ash}",
      fontsize=5.0, color=SUB, va="top", ha="left")
    S(i, 0, PH + 9.5, f"panel labels: {panel_desc(name)} · width {'verified' if ok else 'representative'}",
      fontsize=5.0, color=SUB, va="top", ha="left")

    fig.canvas.draw()
    render_captions(fig.canvas.get_renderer())
    probs = audit(name)
    slug = name.split()[0].lower()
    fig.savefig(f"layout_{slug}.pdf", bbox_inches="tight", pad_inches=0.05)
    fig.savefig(f"layout_{slug}.png", dpi=300, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    return probs


def render_specimen():
    global ax, fig
    cw, ch = 200, 72
    fig, ax = plt.subplots(figsize=(cw * 0.032, ch * 0.032))
    ax.set_xlim(0, cw); ax.set_ylim(0, ch); ax.set_aspect("equal"); ax.axis("off")
    ax.text(0, ch, "Three typefaces — same text & formula", fontsize=6.5,
            fontweight="bold", color=INK, va="top", ha="left")
    speccols = [("Arial", FP_ARIAL, FP_ARIAL_I, FP_ARIAL_B, "stixsans"),
                ("Times New Roman", FP_TIMES, FP_TIMES_I, FP_TIMES_B, "stix"),
                ("Computer Modern", FP_CM, None, FP_CMB, "cm")]
    rows = [("Large · 12 pt", 7.4, "reg"), ("Regular · 9 pt", 5.6, "reg"),
            ("Small · 7 pt", 4.3, "reg"), ("italic", 5.6, "ital"),
            ("bold", 5.6, "bold"), ("math", 6.3, "math")]
    TXT, FORMULA = "Sample 0123", r"$E=mc^2$"
    yhdr = ch - 13
    for cj, (nm, reg, ital, bold, mset) in enumerate(speccols):
        cx = 34 + cj * 56
        ax.text(cx, yhdr, nm, fontproperties=bold, fontsize=6.0, color=ACCENT, va="center", ha="left")
        for ri, (lab, fs, kind) in enumerate(rows):
            ry = yhdr - 11 - ri * 8.0
            if cj == 0:
                ax.text(0, ry, lab, fontsize=4.5, color=SUB, va="center", ha="left", style="italic")
            if kind == "reg":
                ax.text(cx, ry, TXT, fontproperties=reg, fontsize=fs, color=INK, va="center", ha="left")
            elif kind == "bold":
                ax.text(cx, ry, TXT, fontproperties=bold, fontsize=fs, color=INK, va="center", ha="left")
            elif kind == "ital":
                if ital is not None:
                    ax.text(cx, ry, TXT, fontproperties=ital, fontsize=fs, color=INK, va="center", ha="left")
                else:
                    ax.text(cx, ry, r"$Sample\ 0123$", math_fontfamily="cm", fontsize=fs,
                            color=INK, va="center", ha="left")
            else:
                ax.text(cx, ry, FORMULA, math_fontfamily=mset, fontsize=fs, color=INK, va="center", ha="left")
    fig.savefig("typeface_specimen.pdf", bbox_inches="tight", pad_inches=0.05)
    fig.savefig("typeface_specimen.png", dpi=300, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


if __name__ == "__main__":
    print("Per-publisher layout self-checks:")
    all_ok = True
    for i in range(len(pubs)):
        if render_publisher(i):
            all_ok = False
    render_specimen()
    print("typeface_specimen     OK ✓")
    print("ALL CLEAN ✓" if all_ok else "SOME ISSUES — see above ✗")
    print("wrote layout_<publisher>.{png,pdf} (×6) and typeface_specimen.{png,pdf}")
