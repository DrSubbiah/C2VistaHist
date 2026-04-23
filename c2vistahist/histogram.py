"""
C2VistaHist — enriched_histogram()
Cepheus AI Labs | Dr Subbiah | https://cepheusonline.com/
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import stats
from scipy.stats import skew, kurtosis


def enriched_histogram(
    filepath      = None,
    column        = None,
    variable_name = "Study Variable",
    bin_rule      = "fd",
    y_axis_mode   = "frequency",
    show_normal   = True,
    percentiles   = [25, 75],
):
    """
    Plot an enriched univariate histogram with statistical overlays.

    Parameters
    ----------
    filepath : str
        Path to the CSV file. Required.
    column : str
        Column name in the CSV to analyse. Required.
    variable_name : str
        Display label for the X-axis and plot title.
        Default: "Study Variable"
    bin_rule : str or int
        Bin selection rule. One of "sturges", "scott", "fd" (Freedman-Diaconis),
        or a positive integer for manual bin count.
        Default: "fd"
    y_axis_mode : str
        Y-axis scale. "frequency" shows counts, "density" shows probability density.
        Default: "frequency"
    show_normal : bool
        If True, overlays a fitted normal curve using sample mean and SD.
        Default: True
    percentiles : list of int/float
        Additional percentile reference lines to draw. Up to 5 values in range (0, 100).
        P50 (median) is always plotted as a dedicated line — do not include 50 here.
        Default: [25, 75]

    Returns
    -------
    plotly.graph_objects.Figure
        The enriched histogram figure. Also opens in browser via fig.show().

    Examples
    --------
    Minimal call — all defaults applied:
        enriched_histogram(filepath="data.csv", column="bweight")

    Full custom call:
        enriched_histogram(
            filepath      = "data.csv",
            column        = "bweight",
            variable_name = "Birth Weight",
            bin_rule      = "fd",
            y_axis_mode   = "frequency",
            show_normal   = True,
            percentiles   = [5, 25, 75, 95]
        )
    """

    # ─────────────────────────────────────────────────────────
    #  INPUT VALIDATION
    # ─────────────────────────────────────────────────────────
    if filepath is None:
        raise ValueError("filepath is required. Provide path to your CSV file.")
    if column is None:
        raise ValueError("column is required. Provide the column name to analyse.")

    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: '{filepath}'. Check the path.")
    except Exception as e:
        raise ValueError(f"Could not read CSV file: {e}")

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' not found in file. "
            f"Available columns: {list(df.columns)}"
        )

    data = df[column].dropna().values

    if not np.issubdtype(data.dtype, np.number):
        raise ValueError(f"Column '{column}' must be numeric.")

    if len(data) < 10:
        raise ValueError(
            f"Only {len(data)} valid observations found in '{column}'. "
            f"Minimum 10 required for a meaningful histogram."
        )

    valid_bin_rules = ["sturges", "scott", "fd"]
    if not (isinstance(bin_rule, int) and bin_rule > 0) and bin_rule not in valid_bin_rules:
        raise ValueError(
            f"bin_rule='{bin_rule}' is not valid. "
            f"Use 'sturges', 'scott', 'fd', or a positive integer."
        )

    # Silently remove P50 if user included it — median is always plotted separately
    percentiles = [p for p in percentiles if p != 50]
    if len(percentiles) > 5:
        percentiles = percentiles[:5]
        print("Note: Maximum 5 percentiles allowed. Only the first 5 will be used.")

    # ─────────────────────────────────────────────────────────
    #  STATISTICS
    # ─────────────────────────────────────────────────────────
    n        = len(data)
    mn       = np.mean(data)
    med      = np.median(data)
    sd       = np.std(data, ddof=0)
    skew_val = skew(data)
    kurt_val = kurtosis(data, fisher=True)
    dmin     = np.min(data)
    dmax     = np.max(data)

    # Mode — histogram peak bin centre
    counts_mode, edges_mode = np.histogram(data, bins="fd")
    peak_bin = np.argmax(counts_mode)
    mode_val = (edges_mode[peak_bin] + edges_mode[peak_bin + 1]) / 2

    # Percentile values
    pct_values = {p: float(np.percentile(data, p)) for p in percentiles}

    # ─────────────────────────────────────────────────────────
    #  HISTOGRAM BINS
    # ─────────────────────────────────────────────────────────
    if isinstance(bin_rule, int):
        bin_edges = np.linspace(dmin, dmax, bin_rule + 1)
    else:
        _, bin_edges = np.histogram(data, bins=bin_rule)

    bin_width = bin_edges[1] - bin_edges[0]
    counts, _ = np.histogram(data, bins=bin_edges)
    density   = counts / (n * bin_width)

    y_vals  = density if y_axis_mode == "density" else counts
    y_label = "Density" if y_axis_mode == "density" else "Frequency"
    y_max   = max(y_vals) * 1.35

    # ─────────────────────────────────────────────────────────
    #  NORMAL CURVE
    # ─────────────────────────────────────────────────────────
    x_norm  = np.linspace(dmin - sd, dmax + sd, 400)
    y_norm_ = stats.norm.pdf(x_norm, mn, sd)
    y_norm  = y_norm_ if y_axis_mode == "density" else y_norm_ * n * bin_width

    # ─────────────────────────────────────────────────────────
    #  COLOUR & STYLE PALETTE
    # ─────────────────────────────────────────────────────────
    HIST_COLOR   = "rgba(100, 149, 237, 0.55)"
    HIST_BORDER  = "rgba(60, 90, 160, 0.85)"
    MEAN_COLOR   = "#1A56DB"
    MEDIAN_COLOR = "#1E8C45"
    MODE_COLOR   = "#C0392B"
    NORMAL_COLOR = "#7B2FBE"
    PCT_COLORS   = ["#E67E22", "#D35400", "#F39C12", "#CA6F1E", "#A04000"]
    LINE_WIDTH   = 1.4

    # ─────────────────────────────────────────────────────────
    #  BUILD FIGURE
    # ─────────────────────────────────────────────────────────
    fig = go.Figure()

    # Histogram bars
    bin_centres = (bin_edges[:-1] + bin_edges[1:]) / 2
    fig.add_trace(go.Bar(
        x             = bin_centres,
        y             = y_vals,
        width         = bin_width * 0.92,
        name          = "Histogram",
        marker        = dict(color=HIST_COLOR, line=dict(color=HIST_BORDER, width=0.8)),
        hovertemplate = f"Bin centre: %{{x:.2f}}<br>{y_label}: %{{y:.4f}}<extra></extra>",
    ))

    # Normal curve
    if show_normal:
        fig.add_trace(go.Scatter(
            x             = x_norm,
            y             = y_norm,
            mode          = "lines",
            name          = "Normal fit",
            line          = dict(color=NORMAL_COLOR, width=LINE_WIDTH + 0.4, dash="dashdot"),
            hovertemplate = "x: %{x:.2f}<br>Normal: %{y:.4f}<extra></extra>",
        ))

    # Vertical line helper — name label rotated 90°, staggered heights
    def vline(x_val, color, dash, label, label_y_frac=0.80):
        fig.add_shape(
            type  = "line",
            x0=x_val, x1=x_val,
            y0=0,     y1=y_max,
            line  = dict(color=color, width=LINE_WIDTH, dash=dash),
            layer = "above",
        )
        fig.add_annotation(
            x         = x_val,
            y         = y_max * label_y_frac,
            text      = f"<b>{label}</b>",
            showarrow = False,
            textangle = -90,
            font      = dict(size=9, color=color),
            xanchor   = "left",
            yanchor   = "middle",
            bgcolor   = "rgba(255,255,255,0.55)",
            borderpad = 2,
        )

    # Mean / Median / Mode — staggered
    vline(mn,       MEAN_COLOR,   "solid", "Mean",   label_y_frac=0.82)
    vline(med,      MEDIAN_COLOR, "dash",  "Median", label_y_frac=0.65)
    vline(mode_val, MODE_COLOR,   "dot",   "Mode",   label_y_frac=0.48)

    # Percentile lines — shorter, lower label band
    for i, (p, pv) in enumerate(pct_values.items()):
        col = PCT_COLORS[i % len(PCT_COLORS)]
        fig.add_shape(
            type  = "line",
            x0=pv, x1=pv,
            y0=0,  y1=y_max * 0.55,
            line  = dict(color=col, width=LINE_WIDTH - 0.2, dash="longdash"),
            layer = "above",
        )
        fig.add_annotation(
            x         = pv,
            y         = y_max * 0.28,
            text      = f"<b>P{p}</b>",
            showarrow = False,
            textangle = -90,
            font      = dict(size=8.5, color=col),
            xanchor   = "left",
            yanchor   = "middle",
            bgcolor   = "rgba(255,255,255,0.55)",
            borderpad = 2,
        )

    # ─────────────────────────────────────────────────────────
    #  STATS FOOTNOTE BOX
    # ─────────────────────────────────────────────────────────
    stats_lines = [
        f"<b>n</b> = {n}   |   "
        f"<b>Min</b> = {dmin:.3f}   <b>Max</b> = {dmax:.3f}   |   "
        f"<b>Mean</b> = {mn:.3f}   <b>Median</b> = {med:.3f}   <b>Mode</b> ≈ {mode_val:.3f}",

        f"<b>SD</b> = {sd:.3f}   |   "
        f"<b>Skewness</b> = {skew_val:.3f}   "
        f"<b>Kurtosis (excess)</b> = {kurt_val:.3f}",
    ]
    if pct_values:
        pct_str = "   ".join([f"<b>P{p}</b> = {v:.3f}" for p, v in pct_values.items()])
        stats_lines.append(f"<b>Percentiles →</b>   {pct_str}")

    fig.add_annotation(
        text        = "<br>".join(stats_lines),
        xref="paper", yref="paper",
        x=0.0, y=-0.26,
        showarrow   = False,
        align       = "left",
        xanchor     = "left",
        font        = dict(size=12, family="Courier New, monospace", color="#2C3E50"),
        bgcolor     = "rgba(236,240,245,0.92)",
        bordercolor = "#A0A8B8",
        borderwidth = 1.2,
        borderpad   = 12,
        width       = 1400,
    )

    # ─────────────────────────────────────────────────────────
    #  LAYOUT
    # ─────────────────────────────────────────────────────────
    fig.update_layout(
        title = dict(
            text     = f"<b>Enriched Histogram  —  {variable_name}</b>",
            font     = dict(size=18, family="Georgia, serif", color="#1A252F"),
            x        = 0.5,
            xanchor  = "center",
        ),
        xaxis = dict(
            title      = dict(text=variable_name, font=dict(size=13)),
            showgrid   = True,
            gridcolor  = "rgba(200,205,215,0.5)",
            zeroline   = False,
        ),
        yaxis = dict(
            title      = dict(text=y_label, font=dict(size=13)),
            showgrid   = True,
            gridcolor  = "rgba(200,205,215,0.5)",
            range      = [0, y_max],
            zeroline   = False,
        ),
        showlegend    = False,
        plot_bgcolor  = "#F8F9FC",
        paper_bgcolor = "#FFFFFF",
        margin        = dict(t=80, b=180, l=70, r=50),
        width         = 1100,
        height        = 620,
        bargap        = 0,
        font          = dict(family="Georgia, serif"),
        hoverlabel    = dict(bgcolor="white", font_size=11),
    )

    fig.show()
    return fig
