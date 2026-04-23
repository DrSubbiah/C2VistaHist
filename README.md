# C2VistaHist

**Enriched Univariate Histogram — Cepheus AI Labs**

*Dr Subbiah | https://cepheusonline.com/*

---

## What It Does

A plain histogram shows shape. **C2VistaHist reveals the full story.**

`enriched_histogram()` produces a single, self-contained, publication-ready interactive histogram that simultaneously displays:

- Histogram bars
- Mean, Median, and Mode as distinct vertical reference lines (color + line type differentiated)
- User-defined percentile lines (up to 5)
- Fitted normal distribution curve overlay (optional)
- Integrated statistics footnote panel: n, Min, Max, Mean, Median, Mode, SD, Skewness, Kurtosis

All components are designed for both **human eyeball judgement** and future **AI-assisted interpretation pipelines**.

Built on [Plotly](https://plotly.com/python/) — fully interactive, hoverable, exportable.

---

## Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/CepheusAILabs/C2VistaHist.git
```

Or clone and install locally:

```bash
git clone https://github.com/CepheusAILabs/C2VistaHist.git
cd C2VistaHist
pip install -r requirements.txt
```

Then in your script:

```python
from c2vistahist import enriched_histogram
```

---

## Quick Start

**Minimal call — all defaults applied:**
```python
from c2vistahist import enriched_histogram

enriched_histogram(
    filepath = "your_data.csv",
    column   = "your_column"
)
```

**Full custom call:**
```python
enriched_histogram(
    filepath      = "your_data.csv",
    column        = "bweight",
    variable_name = "Birth Weight (grams)",
    bin_rule      = "fd",
    y_axis_mode   = "frequency",
    show_normal   = True,
    percentiles   = [5, 25, 75, 95]
)
```

---

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `filepath` | — | Path to CSV file. **Required.** |
| `column` | — | Column name to analyse. **Required.** |
| `variable_name` | `"Study Variable"` | X-axis label and plot title |
| `bin_rule` | `"fd"` | `"sturges"` / `"scott"` / `"fd"` / integer |
| `y_axis_mode` | `"frequency"` | `"frequency"` or `"density"` |
| `show_normal` | `True` | Overlay fitted normal curve |
| `percentiles` | `[25, 75]` | Up to 5 percentile lines. Do not include 50. |

See [PARAMETERS.md](PARAMETERS.md) for full details on every parameter.

---

## Saving Output

The figure opens in the browser automatically.
To save:

```python
fig = enriched_histogram(filepath="data.csv", column="bweight")

# Save as interactive HTML
fig.write_html("histogram.html")

# Save as static image (requires kaleido)
# pip install kaleido
fig.write_image("histogram.png", width=1200, height=750, scale=2)
```

---

## Dependencies

```
numpy
scipy
plotly
pandas
```

---

## Roadmap

| Module | Status |
|---|---|
| `enriched_histogram` | ✅ v0.1.0 |
| `enriched_kde` | Coming — C2VistaKDE |
| `enriched_scatter` | Coming — C2VistaScatter |

---

## License

MIT License — see [LICENSE](LICENSE)

---

*Cepheus AI Labs | https://cepheusonline.com/*
