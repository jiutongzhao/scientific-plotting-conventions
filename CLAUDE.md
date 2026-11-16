# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **reference guide** to what journals require of a figure (size, resolution, fonts, formats,
color, panel labels) and the matplotlib commands that meet those requirements. **`README.md` is
the deliverable.** The `.mplstyle` files are an optional convenience, not the product, so frame
them that way in prose. Don't write "best-practice" prose for things journals don't mandate
(lines, markers, ticks, spines); show those in a figure instead.

There is no package, build, linter or test suite. "Building" means regenerating the figures in
`figures/` that the README embeds.

## Commands

Needs `numpy` + `matplotlib` (3.10 here). Arial is installed; the scripts fall back to
Liberation Sans or DejaVu without it. Each script runs standalone and writes `.png` + `.pdf` into
`figures/`:

```bash
python scripts/publisher_page_layouts.py   # layout_<publisher>.* x6, prints an overlap audit
python scripts/slide_layout.py             # slide_layout.*
python scripts/journal_layout_schematic.py # journal_layout_schematic.* (README hero image)
python scripts/rcparams_text_map.py        # rcparams_text_map.*
python scripts/style_samples.py            # style_sample_{paper,slides}.*
python scripts/size_samples.py             # size_sample_*.* (grids, square grids, slide sizes)
python scienceplots-contrib/preview.py     # -> scienceplots-contrib/preview/ (needs Pillow + ~/Code/SciencePlots clone)
pdffonts figures/<name>.pdf                # must list TrueType / CID TrueType, never Type 3
```

`publisher_page_layouts.py` must end with `ALL CLEAN ✓`. Its audit has missed misplaced text
before, so also open and read the rendered PNG after any layout change.

## Architecture

### Style files compose; later entries win

`plt.style.use([base, patch, ...])`. The two **base** styles at the root share one visual
identity: DejaVu-first fonts (so output is the same on every machine), the SciencePlots high-vis
color cycle with cycling linestyles, boxed inward ticks with minors, and a frameless legend whose
labels take their line's color. They differ only in scale:

- `paper.mplstyle`: 3.46 in single column, 6 pt type, 1 pt lines
- `slides.mplstyle`: 6.8 × 4.2 in, 18 pt type, 2.5 pt lines. `figure.dpi: 96` and
  `savefig.dpi: 300` make exported PNGs paste into PowerPoint at true size.

**Patches** each change one concern and stack after a base:

- `sizes/`: only `figure.figsize`. Column widths (`single` 88 mm, `onehalf` 120 mm, `double`
  180 mm), single-column aspect variants (`single-short`/`-medium`/`-tall`), grid heights and
  `slides-half`/`-full`.
- `fontsizes/`: a full font-size hierarchy from one base size (title = 1.2×, ticks/legend = 0.83×).
- `editable-text.mplstyle`, `short-legend.mplstyle`: standalone versions of settings that
  `paper.mplstyle` already bundles (or, for short-legend, goes one step past).

Every patch's header comment carries its own `plt.style.use([...])` usage line. Update it when
you rename a file.

**Grid-height rule:** `height = width × panel_aspect × rows / cols`. So patches are named by
rows:cols ratio, and one file serves every grid with that ratio: `double` covers 1×1, 2×2 and
3×3; `1x2` covers 1×2 and 2×4. Golden panels (0.618) are the default. The `square` and
`*-square` variants assume `ax.set_box_aspect(1)` on every panel; without it constrained layout
shrinks the panels. `scripts/size_samples.py` maps `Fraction(rows, cols)` to a patch name
(`PATCH_BY_RATIO`), so renaming or adding a size patch means updating that map, the README tables
and links, and the patch's own comment.

**Invariant: `savefig.bbox: standard` with `figure.constrained_layout.use: True`.** The saved
file is then exactly `figsize`. Never switch to `tight`: it silently crops every save. Never call
`tight_layout()`: it fights the layout solver.

### Two kinds of scripts

Every script writes to `Path(__file__).resolve().parent.parent / "figures"`.

- **Samples** (`style_samples.py`, `size_samples.py`) render through the repo's own `.mplstyle`
  files. Re-run them after editing any style or patch so the README images stay true.
  `size_samples.py` imports `ROOT`, `OUT`, `DPI` and `demo` from `style_samples.py`. All sample
  PNGs export at the same dpi (300), so their pixel sizes keep the true physical-size ratios. The
  README `<img width=...>` values encode those ratios: paper 333 vs slides 653, grids 680, slide
  sizes at ½ scale. Change a figsize and you must update those widths too.
- **Schematics** (`publisher_page_layouts.py`, `slide_layout.py`, `journal_layout_schematic.py`,
  `rcparams_text_map.py`) do **not** use the style files. Each sets its own rcParams (Arial-first,
  Type 42) and draws to scale. The page schematics plot in millimetre data coordinates with
  `ax.set_aspect("equal")`.

`publisher_page_layouts.py` is data-driven:

- The `pubs` tuples hold paper size, column widths, column count, sample-plot functions, and a
  flag for whether the widths are *verified*.
- `ASPECT` holds each publisher's distinct figure aspect ratios; `PANELSTYLE` holds its panel-label
  case, bold, parentheses and position.
- Captions follow each publisher's house style (Nature `Fig. 1 | …`, IEEE centred `Fig. 1.`).
- Text must be registered (via `S()` into `STRUCT`, or into `BODYBOX`/`INSETS`/`CHECKS`) for
  `audit()` to check it for overlaps. Register any text you add.

Publisher figure specs are **verified for Nature, Elsevier and IEEE** against their official
artwork guides. The others are representative values and are flagged as such. Don't promote a
number to "verified" without checking the publisher's own page.

### `scienceplots-contrib/`

Staging area for an upstream PR to [SciencePlots](https://github.com/garrettj403/SciencePlots).
Its files mirror the root styles but are rewritten in SciencePlots conventions:

- `key : value` syntax, flat names that don't collide with existing styles.
- Every size patch also carries `savefig.bbox: standard` and constrained layout, because the base
  `science` style sets `tight`.

It deliberately differs from the root: a single 7 pt `fontsize.mplstyle`, and a `slides-third`
patch. Its `README.md` holds the planned PR split. When a root style changes, decide whether the
contrib copy should follow.

## README conventions

- Order: title → tagline → hero image → the guide (**Part 1** Set up → **Part 2** Tune the
  content → **Part 3** Export) → References → Cheat sheet → Appendix (print layouts and full
  publisher specs) → About this repository / Reproduce → License. Repo plumbing, the cheat sheet
  and file lists stay at the **back**; the front leads straight into the guide.
- Publisher layouts and spec tables live in collapsed `<details>` blocks; GitHub has no native
  tabs. The spec tables are transposed, with publishers as columns.
- Cross-references are links to heading anchors (`[...](#figure-size)`), not `§N`. Renaming a
  heading breaks them, so grep for `](#` after editing headings.
- American spelling in README prose ("color"). Some `.mplstyle` comments still use "colour".
- Figures: SciencePlots high-vis colors (`#0d49fb #e6091c #26eb47 #8936df #fec32d #25d7fd`).
  Export editable vector PDF (Type 42) plus PNG at ≥300 dpi. Legends must never cover data: use
  headroom or a translucent box. Text in a schematic must be sized to scale against the body text.
