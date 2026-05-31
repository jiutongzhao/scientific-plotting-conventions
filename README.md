# Scientific Plotting & Presentation Conventions

A practical, **matplotlib-focused** reference for making figures that are
**publication-ready**, **legible**, and **editable** — with a ready-to-use style sheet and
to-scale schematics of how the major publishers expect figures to look.

> **The one rule that explains all the others:** *build the figure at the exact physical size
> it will be printed or projected.* Never draw a big figure and shrink it in Word/LaTeX/
> PowerPoint — scaling silently shrinks fonts and line weights below the legibility limits and
> makes panels inconsistent. Set the size in **inches/mm**, the font in **points**, and what
> you see is what the reader gets.

![To-scale page layouts across six publishers: paper size and margins, full- and part-width figures at each journal's true column width and a distinct aspect ratio, multi-panel labels and figure captions in each house style, greeked body text, and a three-typeface specimen](publisher_page_layouts.png)

## Repository contents

| File | What it is |
|---|---|
| **this `README.md`** | The full guide — everything below. |
| **[`scientific.mplstyle`](scientific.mplstyle)** | A drop-in matplotlib style sheet encoding the defaults: Arial · 7 pt · Type-42 editable vector export · despined axes · Wong colour-blind-safe palette. |
| **[`publisher_page_layouts.py`](publisher_page_layouts.py)** | Generates the cross-publisher schematic above (Nature · Elsevier · Springer · IEEE · Wiley · Science), drawn to scale with real sample plots. → `.png` / `.pdf` |
| **[`journal_layout_schematic.py`](journal_layout_schematic.py)** | Generates a single-page "figure anatomy" schematic. → `.png` / `.pdf` |

## Quick start

```python
import matplotlib.pyplot as plt
plt.style.use("scientific.mplstyle")   # publication-ready defaults, one line

fig, ax = plt.subplots(figsize=(3.5, 2.16))   # single-column, ~golden ratio (inches)
ax.plot(x, y, label="data")
ax.set_xlabel("Time (s)")              # quantity + unit
ax.set_ylabel("Signal (a.u.)")
ax.legend()
fig.savefig("figure.pdf")              # vector + embedded editable fonts -> submit this
```

Reproduce the schematics (needs `numpy` + `matplotlib`; Arial improves the look but a bundled
sans-serif is used as a fallback):

```bash
python publisher_page_layouts.py      # -> publisher_page_layouts.{pdf,png}
python journal_layout_schematic.py    # -> journal_layout_schematic.{pdf,png}
```

The full reference follows.

---

## Table of contents

1. [Quick-reference cheat sheet](#1-quick-reference-cheat-sheet)
2. [Figure size](#2-figure-size)
3. [Resolution (DPI) & file format](#3-resolution-dpi--file-format)
4. [Fonts & font size](#4-fonts--font-size)
5. [Editable / vector content](#5-editable--vector-content)
6. [Lines, markers, ticks, spines](#6-lines-markers-ticks-spines)
7. [Color](#7-color)
8. [Layout & multi-panel figures](#8-layout--multi-panel-figures)
9. [Presentations & slides](#9-presentations--slides)
10. [Putting it together in matplotlib](#10-putting-it-together-in-matplotlib)
11. [Publisher figure specifications](#11-publisher-figure-specifications-quick-reference)
12. [References & further reading](#12-references--further-reading)

---

## 1. Quick-reference cheat sheet

| Aspect | Print figure (journal) | Slide / poster |
|---|---|---|
| **Width** | 1 column ≈ 89 mm (3.5 in); 2 columns ≈ 180 mm (7.1 in) | Fill the content area; design at 16:9 (13.33 × 7.5 in) |
| **Height** | ≤ full page (~240 mm); usually keep panels short | — |
| **Font** | 7 pt typical, **never below ~5 pt** | 18–28 pt body, 28–40 pt titles |
| **Typeface** | Sans-serif (Arial / Helvetica) | Same sans-serif everywhere |
| **Line width** | 0.5–1.0 pt (absolute min ~0.25 pt) | 1.5–3 pt (thicker for projection) |
| **Raster resolution** | 300 dpi (photos), 600 dpi (line/combination) | 150–300 dpi export is plenty |
| **Format** | **Vector**: PDF/EPS for plots; TIFF for images | PNG (or vector pasted into the deck) |
| **Text** | Must stay **editable** (real text, embedded fonts) | Editable helps, less critical |
| **Color** | Colorblind-safe palette; check it survives grayscale | Same; ensure contrast on a projector |

Representative print specs (**always confirm against the target venue's author guidelines**, the numbers drift):

| Journal | 1-column | 2-column (full) | Max height | Min font | Raster res |
|---|---|---|---|---|---|
| Nature | 89 mm (3.50 in) | 183 mm (7.20 in) | 247 mm | 5–7 pt | 300 dpi photo / 600 dpi line |
| Science | 55 mm (2.17 in) | 120 / 183 mm | ~183 mm | ~6–7 pt | ≥ 300 dpi |
| Cell | 85 mm | 174 mm | 240 mm | 5–7 pt | 300 dpi |
| IEEE | 88.9 mm (3.5 in) | 181.6 mm (7.16 in) | — | 8 pt | 300–600 dpi |
| PLOS | 67 mm (2.63 in) min | 190 mm (7.5 in) max | 222 mm | 8–12 pt | 300–600 dpi |

> **More publishers?** A full cross-publisher comparison — Wiley, Elsevier, Springer, ACS,
> RSC, APS, Taylor & Francis and others, with widths, resolution, fonts and formats — is in
> [§11](#11-publisher-figure-specifications-quick-reference).

---

## 2. Figure size

**Think in physical units, not pixels.** A figure has a true size in inches/mm; pixels only
appear when you rasterize (`width_px = width_in × dpi`).

- **Match the column grid.** Most journals are two-column. Make figures either single-column
  (~89 mm) or full-width (~180 mm) so they drop in without scaling. A "1.5-column" width
  (~120–136 mm) is allowed by some journals for wide panels.
- **Keep height modest.** A figure may not exceed the printable page height (~240 mm including
  the caption). Tall figures get shrunk by the typesetter — which re-shrinks your fonts.
- **Pick a deliberate aspect ratio.** The golden ratio (height ≈ 0.618 × width) or a clean 4:3
  reads well; square (1:1) suits matrices/heatmaps; wide/short suits time series.

### In matplotlib

`figsize` is **in inches**. Set it once and design at 1:1:

```python
fig, ax = plt.subplots(figsize=(3.5, 2.16))   # single-column Nature, ~golden ratio
```

A tiny helper keeps you in physical units and consistent ratios:

```python
def fig_size(width_mm, aspect=0.618, fraction=1.0):
    """Return (width, height) in INCHES for a target column width in mm."""
    width_in = (width_mm / 25.4) * fraction
    return (width_in, width_in * aspect)

fig, ax = plt.subplots(figsize=fig_size(89))    # single column
fig, ax = plt.subplots(figsize=fig_size(183))   # double column
```

> **Gotcha — `bbox_inches="tight"` changes the final size.** It crops to the artists, so the
> saved width is no longer exactly your `figsize`. For *strict* column fitting, prefer
> `constrained_layout` (below) and save **without** `tight`, or add a fixed
> `pad_inches`. For everyday use, `tight` is fine and convenient.

---

## 3. Resolution (DPI) & file format

**Resolution only matters for raster (pixel) content.** The single most effective quality
decision is to **export plots as vector**, which has effectively infinite resolution.

- **Vector** (PDF, EPS, SVG): lines/text/shapes stored as math. Scales to any size, stays
  crisp, stays editable, smallest files for line art. **Use for all plots, schematics, and
  anything text-heavy.**
- **Raster** (PNG, TIFF, JPEG): a pixel grid. Required only for photographs, microscopy,
  heat maps with millions of cells, or volumetric renders.

DPI guidance for raster content (at **final printed size**):

| Content | Minimum DPI |
|---|---|
| Color / grayscale photographs | 300 |
| Line art (text, axes, thin lines) | 600–1200 |
| Combination (photo + labels) | 600 |
| Screen / slides only | 150 (≈ 96 acceptable) |

### File-format chooser

| Format | Kind | Best for | Notes |
|---|---|---|---|
| **PDF** | Vector | Final plots, LaTeX (`\includegraphics`) | Embed fonts as Type 42; supports transparency |
| **SVG** | Vector | Web; hand-editing in Illustrator/Inkscape | Set `svg.fonttype:none` to keep text as text |
| **EPS** | Vector | Legacy journal submission | No transparency/alpha — flatten first |
| **TIFF** | Raster | Photographic/image-panel submission | LZW compression, 300–600 dpi |
| **PNG** | Raster | Slides, web, previews | Lossless; always set `dpi` |
| **JPEG** | Raster | ❌ avoid for plots | Lossy → ringing artifacts around edges/text |

### In matplotlib

```python
# Vector — the default deliverable for plots
fig.savefig("figure.pdf")                      # picks up savefig.* rcParams below
fig.savefig("figure.svg")

# Raster — only when you must; set dpi explicitly at final size
fig.savefig("figure.png", dpi=600)
fig.savefig("figure.tiff", dpi=600, pil_kwargs={"compression": "tiff_lzw"})

# Selective rasterization: keep text/axes vector, rasterize only a heavy layer
ax.pcolormesh(X, Y, Z, rasterized=True)        # huge mesh becomes pixels...
fig.savefig("figure.pdf", dpi=600)             # ...at this dpi, labels stay vector
```

---

## 4. Fonts & font size

Legibility is non-negotiable: a reader (or reviewer) must read every label at print size.

- **Use a sans-serif face**, consistently: **Arial** or **Helvetica** are the de-facto journal
  standard (DejaVu Sans is matplotlib's bundled look-alike if Arial isn't installed).
- **Keep the type small but legible.** Aim for ~7 pt; treat **~5 pt as the absolute floor**.
  Figure text should be similar to, or slightly smaller than, the article body text.
- **Be consistent across panels.** All panels of a multi-part figure share one font and one
  size scheme. This is the #1 reason to design at final size — scaling panels differently
  breaks consistency.
- **Match math to text.** Make symbols/equations use the same family, and always **label axes
  with quantity + unit**, e.g. `Time (s)`, `Voltage (mV)`.

Suggested point sizes:

| Element | Print (pt) | Slide (pt) |
|---|---|---|
| Axis tick labels | 6–8 | 18–24 |
| Axis titles | 7–9 | 22–28 |
| Legend / annotations | 6–8 | 18–22 |
| Panel letters (a, b, c) | 8, **bold** | — |
| Slide title | — | 28–40 |

### In matplotlib

```python
import matplotlib as mpl
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],  # first available wins
    "font.size":        7,    # base size; other elements scale from this
    "axes.titlesize":   8,
    "axes.labelsize":   7,
    "xtick.labelsize":  6,
    "ytick.labelsize":  6,
    "legend.fontsize":  6,
    "mathtext.fontset": "dejavusans",  # keep math consistent with sans text
})
```

> If you see `findfont: Font family 'Arial' not found`, Arial isn't installed (common on Linux/
> WSL). Either install it (e.g. `msttcorefonts`), drop in a `.ttf` and run
> `matplotlib.font_manager.fontManager.addfont(...)`, or rely on the **DejaVu Sans** fallback.
> For full LaTeX-identical typesetting set `text.usetex: True` (needs a LaTeX install; slower).

---

## 5. Editable / vector content

Journals' production teams (and your co-authors) need to **edit the text and elements** of a
figure — fix a typo, recolor a line, restyle a label — without your source script. Two things
make a figure editable:

1. **Export vector** (PDF/SVG/EPS), so every line and glyph is an object, not a pixel.
2. **Keep text as text with embedded, editable fonts** — not outlined into paths, not
   rasterized.

### The Type 3 vs Type 42 trap (important)

By default matplotlib embeds **Type 3** fonts in PDF/PS. Type 3 fonts are **not editable** in
Illustrator and are **rejected by many journals** (Nature, IEEE, …). Switch to **Type 42**
(TrueType) and your text becomes selectable and editable downstream:

```python
mpl.rcParams["pdf.fonttype"] = 42   # TrueType, editable (NOT Type 3)
mpl.rcParams["ps.fonttype"]  = 42
mpl.rcParams["svg.fonttype"] = "none"   # write <text> tags, not vector outlines
```

Do's and don'ts for editability:

- ✅ Save **PDF/SVG/EPS**, not PNG/JPEG, for any plot.
- ✅ Set the three `fonttype` params above (the SVG one keeps text as real text).
- ✅ Use selective `rasterized=True` only on the heavy data layer; keep axes/labels vector.
- ❌ Don't "Create outlines"/"flatten text" in a vector editor — it kills editability.
- ❌ Don't paste a screenshot of a plot into the manuscript.
- ❌ Don't rasterize the whole figure to PNG and call it "final."

**Verify it worked:** open the PDF and try to *select the axis text* — if you can highlight it,
it's real text. (Power users: `pdffonts figure.pdf` should list `Type 1`/`TrueType`/
`Type 42`, **never** `Type 3`.)

---

## 6. Lines, markers, ticks, spines

Small details that separate amateur from publication-grade:

- **Line weight:** 0.5–1.0 pt for data; ~0.6 pt for axes. Below ~0.25 pt lines vanish in
  print. Bump everything up for slides/posters.
- **Markers:** ~4 pt; give them an edge (`markeredgewidth ≈ 0.6`) so overlapping points stay
  distinct. Vary **shape** as well as color so the figure survives grayscale.
- **Ticks:** point **outward** so they don't collide with data; show minor ticks for fine
  scales. Keep tick labels sparse and rounded.
- **Spines:** remove the top and right spines ("despine") to cut visual clutter and maximize
  the data-ink ratio.
- **Avoid chartjunk:** no 3-D bars, no heavy gridlines, no drop shadows, no background fills.
  If you use a grid, make it light (`alpha ≈ 0.3–0.4`, thin).

```python
mpl.rcParams.update({
    "axes.linewidth": 0.6,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "lines.linewidth": 1.0,
    "lines.markersize": 4,
    "lines.markeredgewidth": 0.6,
    "xtick.direction": "out", "ytick.direction": "out",
    "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.major.size": 3,    "ytick.major.size": 3,
    "xtick.minor.visible": True, "ytick.minor.visible": True,
})
# or per-axes: ax.spines[["top", "right"]].set_visible(False)
```

---

## 7. Color

- **Use a colorblind-safe palette.** ~8% of men have a color-vision deficiency. The
  **Wong / Okabe–Ito** 8-color palette is the standard safe choice:

  | Name | Hex |
  |---|---|
  | Black | `#000000` |
  | Orange | `#E69F00` |
  | Sky blue | `#56B4E9` |
  | Bluish green | `#009E73` |
  | Yellow | `#F0E442` |
  | Blue | `#0072B2` |
  | Vermillion | `#D55E00` |
  | Reddish purple | `#CC79A7` |

- **Redundant encoding:** never rely on color alone — pair it with line style, marker shape,
  or direct labels, so the figure still works in **grayscale** and for colorblind readers.
- **Colormaps:** use **perceptually uniform** maps — `viridis`, `cividis`, `magma`, `plasma`
  for sequential data; `coolwarm`/`RdBu` for diverging (zero-centered) data. **Avoid `jet`/
  rainbow** — it invents false structure and is not colorblind-safe. `cividis` is the most
  colorblind-friendly of the built-ins.
- **Print vs screen:** journals print in **CMYK**; saturated RGB blues/greens can shift. Keep
  colors moderately saturated and check a CMYK proof if the venue requires it.

```python
import matplotlib as mpl
wong = ["#0072B2", "#E69F00", "#009E73", "#D55E00",
        "#56B4E9", "#CC79A7", "#F0E442", "#000000"]
mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=wong)
mpl.rcParams["image.cmap"] = "viridis"   # default for imshow/pcolormesh
```

---

## 8. Layout & multi-panel figures

- **Label panels** `a, b, c …` (lowercase, bold), placed consistently at the top-left of each
  panel. Refer to them in the caption. *Publishers differ on case, brackets and position
  (`a` vs `A` vs `(a)`, top-left vs below) — see [§11.5](#115-panel-labels-by-publisher-in-matplotlib).*
- **Align and share axes.** Panels comparing the same quantity should share axis ranges and
  scales; align panel edges to a grid.
- **Control whitespace automatically.** Use `constrained_layout` (or `tight_layout`) so labels
  never overlap and margins stay tight and uniform.
- **Compose, don't cram.** A panel that needs its own caption is probably a separate figure.

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=fig_size(183, aspect=0.42),
                         layout="constrained")     # auto, non-overlapping spacing
for ax, letter in zip(axes.flat, "ab"):
    ax.text(-0.12, 1.04, letter, transform=ax.transAxes,
            fontsize=8, fontweight="bold", va="bottom", ha="right")
```

> `layout="constrained"` (matplotlib ≥ 3.6) is generally better than `tight_layout()` for
> multi-panel figures because it also reserves room for shared legends/colorbars.

---

## 9. Presentations & slides

Slides invert several print rules — viewers are **far away** and see each slide for **seconds**.

- **Size:** design the deck at **16:9** (13.33 × 7.5 in) — or 4:3 (10 × 7.5 in) for older
  projectors. Make figures fill the content area; don't shrink a print figure onto a slide.
- **Font:** **big** — ~18–24 pt body, 28–40 pt titles. The back-row test: if you can't read it
  standing across the room from your laptop, it's too small.
- **Line/marker weight:** thicker than print (1.5–3 pt) so lines survive projection and
  compression.
- **Contrast:** dark-on-light or light-on-dark with strong contrast; avoid thin yellow/pastels
  on white — projectors wash them out.
- **One idea per slide;** strip axis clutter further than you would for print.
- **Export:** vector pasted into the deck stays crisp; otherwise PNG at 150–300 dpi.

```python
import matplotlib as mpl
mpl.rcParams.update({
    "figure.figsize": (8, 4.5),    # inches, 16:9-ish figure area
    "font.size":       18,
    "axes.labelsize":  20,
    "axes.titlesize":  22,
    "xtick.labelsize": 16, "ytick.labelsize": 16,
    "legend.fontsize": 16,
    "lines.linewidth": 2.5,
    "lines.markersize": 8,
    "savefig.dpi":     200,
})
# Quick toggle: plt.style.use("seaborn-v0_8-talk") bumps sizes for talks.
```

---

## 10. Putting it together in matplotlib

Three ways to apply settings, from quick to reproducible:

1. **Inline** `mpl.rcParams.update({...})` at the top of a script (snippets above).
2. **A reusable style sheet** (`.mplstyle`) — recommended; portable and version-controllable.
3. **A context manager** for a one-off figure: `with plt.style.context("paper.mplstyle"): ...`.

### A complete, ready-to-use style sheet

Save the block below as **`scientific.mplstyle`** next to your script (a companion file
[`scientific.mplstyle`](scientific.mplstyle) is included in this repo), then load it:

```python
import matplotlib.pyplot as plt
plt.style.use("scientific.mplstyle")      # local file
# Or install once for all projects by copying it to:
#   matplotlib.get_configdir() + "/stylelib/scientific.mplstyle"
# then: plt.style.use("scientific")
```

```ini
# scientific.mplstyle — single-column, publication-ready defaults
# ---- Figure & export ----
figure.figsize:        3.5, 2.16          # inches: single column, ~golden ratio
figure.dpi:            150                 # on-screen
figure.constrained_layout.use: True
savefig.dpi:           600                 # raster export at final size
savefig.bbox:          tight
savefig.pad_inches:    0.02
savefig.transparent:   False

# ---- Editable, vector-safe text ----
pdf.fonttype:          42                  # TrueType (editable), NOT Type 3
ps.fonttype:           42
svg.fonttype:          none                # keep text as text in SVG

# ---- Fonts ----
font.family:           sans-serif
font.sans-serif:       Arial, Helvetica, DejaVu Sans
font.size:             7
axes.titlesize:        8
axes.labelsize:        7
xtick.labelsize:       6
ytick.labelsize:       6
legend.fontsize:       6
mathtext.fontset:      dejavusans

# ---- Axes & spines ----
axes.linewidth:        0.6
axes.spines.top:       False
axes.spines.right:     False
axes.labelpad:         2.0
axes.titlepad:         4.0
axes.prop_cycle:       cycler('color', ['0072B2','E69F00','009E73','D55E00','56B4E9','CC79A7','F0E442','000000'])

# ---- Lines & markers ----
lines.linewidth:       1.0
lines.markersize:      4
lines.markeredgewidth: 0.6

# ---- Ticks ----
xtick.direction:       out
ytick.direction:       out
xtick.major.size:      3
ytick.major.size:      3
xtick.major.width:     0.6
ytick.major.width:     0.6
xtick.minor.visible:   True
ytick.minor.visible:   True

# ---- Legend & grid ----
legend.frameon:        False
legend.handlelength:   1.5
legend.labelspacing:   0.3
axes.grid:             False
grid.linewidth:        0.4
grid.alpha:            0.4

# ---- Images ----
image.cmap:            viridis
```

### Worked example

```python
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("scientific.mplstyle")

x = np.linspace(0, 2 * np.pi, 400)
fig, ax = plt.subplots()                       # size/fonts come from the style
ax.plot(x, np.sin(x),  label="sin")
ax.plot(x, np.cos(x), ls="--", label="cos")    # line style = redundant encoding
ax.set_xlabel("Phase (rad)")                   # quantity + unit
ax.set_ylabel("Amplitude (a.u.)")
ax.legend()

fig.savefig("demo.pdf")                # vector + editable text → for the manuscript
fig.savefig("demo.png", dpi=600)       # raster → for slides / quick preview
```

### `savefig` recipe (what each argument buys you)

```python
fig.savefig(
    "figure.pdf",          # vector container; format inferred from extension
    dpi=600,               # only affects any rasterized layers
    bbox_inches="tight",   # crop to artists (note: changes final size slightly)
    pad_inches=0.02,       # small uniform margin
    transparent=True,      # no white box when placed on a colored slide
)
```

---

## 11. Publisher figure specifications (quick reference)

Publishers ask for slightly different widths, resolutions, fonts and formats.
This section collects the major ones so you can size a figure once and trust it
will drop in.

> **How to read this.** Rows marked **✔** were verified in 2026 against the
> publisher's official artwork page (**Nature, Elsevier, IEEE**). Unmarked rows
> are representative published values that vary by individual journal and change
> over time — **always open your target journal's author / artwork guidelines
> before final export.**

*(The schematic at the top of this README is the same figure, drawn to scale; it is generated by [`publisher_page_layouts.py`](publisher_page_layouts.py) using the column widths (§11.4), panel-label styles (§11.5) and editable vector export (§5) covered in this document.)*

### 11.1 Figure widths & maximum height

| Publisher | Single col | Mid (1.5 col) | Double / full width | Max height |
|---|---|---|---|---|
| **Nature** ✔ | 88 mm | — | 180 mm | caption-dependent, ≈130–225 mm |
| **Elsevier** ✔ | 90 mm | 140 mm | 190 mm | — (min usable 30 mm) |
| **IEEE** ✔ | 88.9 mm (3.5″) | — | 182 mm (7.16″) | — |
| Springer (general) | 84 mm | 129 mm | 174 mm | ≈234 mm |
| Wiley | ≈80 mm | — | ≈176 mm | journal-dependent |
| Science (AAAS) | 55 mm | 120 mm | 183 mm | ≈240 mm |
| ACS | 85 mm (3.33″) | — | 178 mm (7″) | 241 mm (9.5″) |
| APS (Phys. Rev.) | 86 mm | — | 178 mm | — |
| RSC | 83 mm | — | 171 mm | — |
| Optica (OSA) | 83 mm | — | 165 mm | — |
| PLOS | 67 mm (min) | — | 190 mm (max) | 222 mm (8.75″) |

**Takeaway:** single columns cluster at **83–90 mm**, full width at **170–190 mm**.
Draw single-column figures at ~88–90 mm and full-width at ~180–190 mm and they fit
nearly everywhere (Science's narrow 55 mm single column is the main outlier).

### 11.2 Resolution, formats & colour

DPI applies to **raster** content at final size; vector art is resolution-free.

| Publisher | Line art | Photo / halftone | Combination | Vector | Raster | Colour |
|---|---|---|---|---|---|---|
| **Nature** ✔ | 600 | 300 | 600 | AI · EPS · PDF | TIFF | RGB (research) / CMYK (other) |
| **Elsevier** ✔ | 1000 | 300 | 500 | EPS · PDF | TIFF · JPEG | RGB |
| **IEEE** ✔ | 600 (B/W) | 300 (color/gray) | — | PS · EPS · PDF | PNG · TIFF | not mandated |
| Springer | 1200 | 300 | 600 | EPS · PDF | TIFF | RGB |
| Wiley | 600–1200 | 300 | 600 | EPS · PDF | TIFF | RGB → CMYK |
| Science (AAAS) | vector pref. | 300+ | 600 | AI · EPS · PDF | TIFF | RGB |
| ACS | 1200 | 300 | 600 | EPS · PDF | TIFF | RGB |
| RSC | 600+ | 300 | 600 | EPS · PDF | TIFF | RGB |
| Taylor & Francis | 1200 | 300 | 600 | EPS · PDF | TIFF · JPEG | RGB / CMYK |
| APS (Phys. Rev.) | 600 | 300 | — | EPS · PS · PDF | TIFF | RGB |
| PLOS | — | 300–600 | — | EPS | TIFF | RGB |

**Consensus:** photos **300 dpi**, line art **600–1200 dpi**, combination
**500–600 dpi**; **EPS/PDF** vector accepted everywhere; submit **RGB** unless a
journal asks for CMYK (IEEE doesn't mandate a colour mode — RGB is the safe default).

### 11.3 Fonts & font size

| Publisher | Typeface | Size (at final size) | Notes |
|---|---|---|---|
| **Nature** ✔ | Helvetica / Arial | 5–7 pt | sans-serif only |
| **Elsevier** ✔ | Arial, Times, Courier, Symbol | ≈6–8 pt | embed fonts |
| **IEEE** ✔ | Helvetica, Arial, Times, Cambria, Symbol | 9–10 pt | outline text **or** embed fonts |
| Springer | Helvetica / Arial | ≈8 pt (lettering 2–3 mm) | consistent across panels |
| Wiley | sans-serif (Arial / Helvetica) | ≥ ~7 pt | varies by journal |
| Science (AAAS) | Helvetica / Arial | 5–7 pt | panel labels bold |
| ACS | Helvetica / Arial | 4.5–12 pt | |
| RSC | sans-serif | 7–8 pt | |
| PLOS | Arial | 8–12 pt | |

**Consensus:** **sans-serif (Arial / Helvetica)**, roughly **5–8 pt** in print
(IEEE runs a little larger at 9–10 pt). Keep text as **editable, embedded fonts —
never Type 3** (see [§5](#5-editable--vector-content)).

### 11.4 One export that satisfies (almost) everyone

You rarely need a different file per publisher. These defaults clear every row above:

- **Width** — single column **88–90 mm**, full width **180–190 mm**.
- **Font** — sans-serif, **≥ 7 pt** (meets Nature's floor, stays legible like IEEE).
- **Vector PDF** with **Type 42 / TrueType** embedded fonts (editable — see §5).
- **Raster only where needed** — **≥ 600 dpi** line art, **≥ 300 dpi** photos.
- **RGB** colour; convert to CMYK only if a print journal demands it.

The bundled [`scientific.mplstyle`](scientific.mplstyle) already encodes these.
Size per publisher with one small helper:

```python
WIDTHS_MM = {            # (single, full-width) in mm — see §11.1
    "nature": (88, 180), "elsevier": (90, 190), "ieee": (88.9, 182),
    "springer": (84, 174), "wiley": (80, 176), "science": (55, 183),
    "acs": (85, 178), "aps": (86, 178), "rsc": (83, 171),
    "optica": (83, 165), "plos": (67, 190),
}

def fig_size(publisher="nature", full=False, aspect=0.72):
    """(width, height) in inches for a publisher's column width."""
    w_in = WIDTHS_MM[publisher][1 if full else 0] / 25.4
    return (w_in, w_in * aspect)

import matplotlib.pyplot as plt
plt.style.use("scientific.mplstyle")
fig, ax = plt.subplots(figsize=fig_size("elsevier", full=True))   # 190 mm wide
```

### 11.5 Panel labels by publisher (in matplotlib)

Multi-panel figures get a letter per panel, but the **house style differs** along four axes:
**case** (`a` vs `A`), **weight** (bold vs regular), **brackets** (`a`, `(a)`, `a)`) and
**position** (inside the top-left corner vs centred *below* the panel). Representative styles —
these are exactly the ones drawn in the schematic above:

| Publisher | Looks like | Case | Bold | Brackets | Position |
|---|---|---|---|---|---|
| **Nature** | **a** | lower | ✔ | none | top-left |
| **Elsevier** | (a) | lower | — | round | top-left |
| **Springer** | **(a)** | lower | ✔ | round | top-left |
| **IEEE** | (a) | lower | — | round | **below** the panel |
| **Wiley** | (A) | upper | — | round | top-left |
| **Science (AAAS)** | **A** | upper | ✔ | none | top-left |

> Conventions vary **between journals of the same publisher** and drift over time — treat this
> as a starting point and confirm against your target journal's guidelines.

A small helper stamps a correctly-styled label onto any axes (`i` is 0-based: `0 → a/A`):

```python
import matplotlib.pyplot as plt

PANEL_STYLE = {   # (case, brackets, bold, position) — representative house styles
    "nature":   ("lower", "none",  True,  "tl"),     #  a    bold, no brackets
    "elsevier": ("lower", "round", False, "tl"),     # (a)
    "springer": ("lower", "round", True,  "tl"),     # (a)  bold
    "ieee":     ("lower", "round", False, "below"),  # (a)  centred under the panel
    "wiley":    ("upper", "round", False, "tl"),     # (A)
    "science":  ("upper", "none",  True,  "tl"),     #  A    bold, no brackets
}

def panel_label(ax, i, journal="nature", size=8):
    """Add a sub-panel label in `journal`'s house style. i is 0-based (0 -> a/A)."""
    case, brackets, bold, pos = PANEL_STYLE[journal]
    ch  = chr((65 if case == "upper" else 97) + i)              # A.. or a..
    txt = {"round": f"({ch})", "square": f"[{ch}]", "none": ch}[brackets]
    kw  = dict(fontsize=size, fontweight=("bold" if bold else "normal"))
    if pos == "below":                       # IEEE: centred just under the axes
        ax.text(0.5, -0.16, txt, transform=ax.transAxes, ha="center", va="top", **kw)
    else:                                    # top-left, just inside the corner
        ax.text(0.02, 0.98, txt, transform=ax.transAxes, ha="left", va="top", **kw)
```

> **Placement tip.** A corner label (`0.02, 0.98`) can sit on top of data; placing it just
> *outside* the axes — `ax.text(-0.08, 1.04, txt, transform=ax.transAxes, …)` — avoids overlap
> but needs a little margin (`layout="constrained"`). Pick one and keep it identical on every panel.

> **Captions are the journal's job — not the artwork's.** Submit the figure *caption*
> ("Fig. 1. …") as **manuscript text**, so the typesetter renders `Fig.`/`Figure`, the number
> and any bold lead-in in house style. Only the **panel letters** belong inside the figure file.

### 11.6 Putting one publisher together, end to end

Width (§11.4) + the house font & vector export (`scientific.mplstyle`, §10) + panel labels —
one short block makes a compliant figure for a chosen journal:

```python
import matplotlib.pyplot as plt
plt.style.use("scientific.mplstyle")     # Arial · 7 pt · Type-42 vector export · Wong colours

journal = "ieee"                          # swap to "nature", "elsevier", …
fig, axes = plt.subplots(1, 2, layout="constrained",
                         figsize=fig_size(journal, full=True, aspect=0.42))   # 182 mm wide
for i, ax in enumerate(axes.flat):
    ax.plot(...)                          # your data
    ax.set_xlabel("Time (s)")             # quantity + unit
    ax.set_ylabel("Signal (a.u.)")
    panel_label(ax, i, journal)           # IEEE → (a), (b) centred below each panel

fig.savefig("figure.pdf")                 # vector + embedded editable fonts → submit this
```

Swapping `journal` re-sizes the canvas (`fig_size`/`WIDTHS_MM`, §11.4) and restyles the panel
letters (`panel_label`); the font, line weights, colours and vector/Type-42 export come from the
shared style sheet (§10), so the rest of the requirements (§§3–7) are satisfied automatically.

### 11.7 Official artwork guidelines

- **Nature / Springer Nature** — <https://www.nature.com/documents/NRJs-guide-to-preparing-final-artwork.pdf>
- **Elsevier** — <https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions>
- **Wiley** — Author Services → *Electronic artwork guidelines* (`authorservices.wiley.com`)
- **IEEE** — <https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/>
- **Science / AAAS** — `science.org` → *Instructions for preparing an initial manuscript*
- **ACS** — <https://pubs.acs.org/page/4authors/submission/graphics_prep.html>
- **RSC** — `rsc.org` → *Prepare your article* (artwork & images)
- **Taylor & Francis** — `authorservices.taylorandfrancis.com` → *Submitting your artwork*
- **APS (Physical Review)** — `journals.aps.org/authors` → *Figures*
- **PLOS** — `journals.plos.org` → *Figures* guidelines
- **Optica (OSA)** — `opg.optica.org` → *Author guidelines*

---

## 12. References & further reading

- **Wong, B.** "Points of view: Color blindness." *Nature Methods* **8**, 441 (2011) — the
  source of the 8-color colorblind-safe palette.
- **Rougier, Droettboom & Bourne.** "Ten Simple Rules for Better Figures." *PLOS Comput. Biol.*
  **10**, e1003833 (2014).
- **Nature** — "Final figure preparation" / artwork guidelines (sizes, fonts, formats).
- **Matplotlib docs** — *Customizing with style sheets and rcParams*, *Text rendering and
  fonts*, and the *Constrained-layout guide*.
- **SciencePlots** (`pip install SciencePlots`) — community matplotlib styles matching common
  journals, if you'd rather start from a maintained preset.

> Specific numbers (column widths, DPI floors, accepted formats) change and differ by venue —
> **always open the target journal's "author/figure guidelines" before final export.**

---

## License

[MIT](LICENSE) © Jiutong Zhao
