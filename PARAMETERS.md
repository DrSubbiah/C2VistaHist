# C2VistaHist — Parameter Reference

**Cepheus AI Labs | Dr Subbiah | https://cepheusonline.com/**

---

## `enriched_histogram()` — Full Parameter Table

| Parameter | Type | Default | Required | Description |
|---|---|---|---|---|
| `filepath` | str | — | ✅ Yes | Path to the CSV file |
| `column` | str | — | ✅ Yes | Column name in the CSV to analyse |
| `variable_name` | str | `"Study Variable"` | No | Display label on X-axis and plot title |
| `bin_rule` | str or int | `"fd"` | No | Bin selection rule — see options below |
| `y_axis_mode` | str | `"frequency"` | No | Y-axis scale — `"frequency"` or `"density"` |
| `show_normal` | bool | `True` | No | Overlay fitted normal curve |
| `percentiles` | list | `[25, 75]` | No | Additional percentile lines — max 5 values |

---

## Parameter Details

### `filepath`
Path to your data file. Must be a CSV.
```python
filepath = "C:/data/birthweight.csv"
filepath = "/home/user/data/survey.csv"
```

---

### `column`
The exact column name in your CSV containing the numeric variable to plot.
```python
column = "bweight"
column = "age"
column = "income_usd"
```

---

### `variable_name`
Label shown on the X-axis and in the plot title. Does not affect computation.
```python
variable_name = "Birth Weight (grams)"
variable_name = "Age at Diagnosis"
```
Default: `"Study Variable"`

---

### `bin_rule`
Controls how histogram bins are computed.

| Value | Method |
|---|---|
| `"fd"` | Freedman-Diaconis — robust to outliers, recommended for most data |
| `"sturges"` | Sturges' rule — suitable for small, roughly normal datasets |
| `"scott"` | Scott's rule — assumes normality, good for smooth distributions |
| integer e.g. `20` | Manual — you specify the exact number of bins |

```python
bin_rule = "fd"      # default — recommended
bin_rule = "sturges"
bin_rule = "scott"
bin_rule = 20        # exactly 20 bins
bin_rule = 50        # exactly 50 bins
```
Default: `"fd"`

---

### `y_axis_mode`
Controls what the Y-axis represents.

| Value | Y-axis shows |
|---|---|
| `"frequency"` | Raw counts per bin |
| `"density"` | Probability density (area under histogram = 1) |

Use `"density"` when overlaying and comparing the normal curve shape directly.
Use `"frequency"` for count-based eyeball judgement.

```python
y_axis_mode = "frequency"   # default
y_axis_mode = "density"
```
Default: `"frequency"`

---

### `show_normal`
If `True`, overlays a fitted normal distribution curve using the sample mean and SD.
Useful for visually assessing departure from normality.

```python
show_normal = True    # default — normal curve shown
show_normal = False   # histogram only
```
Default: `True`

---

### `percentiles`
List of additional percentile reference lines to draw on the histogram.

- Maximum 5 values
- Values must be between 0 and 100 (exclusive)
- **Do not include 50** — median is always plotted as a dedicated green dashed line
- If 50 is included it is silently removed

```python
percentiles = [25, 75]           # default — interquartile markers
percentiles = [5, 25, 75, 95]   # common epidemiological choice
percentiles = [10, 90]           # outer deciles
percentiles = []                  # no additional percentile lines
```
Default: `[25, 75]`

---

## What is Always Plotted (not user-controlled)

These components are always present regardless of parameters:

| Component | Description |
|---|---|
| Histogram bars | Cornflower blue, bin-width gap controlled |
| Mean line | Deep blue solid vertical line |
| Median line | Forest green dashed vertical line |
| Mode line | Crimson dotted vertical line (histogram peak bin centre) |
| Stats footnote box | n, Min, Max, Mean, Median, Mode, SD, Skewness, Kurtosis |

---

## Returns
`plotly.graph_objects.Figure` — the enriched histogram figure.
The plot opens automatically in the browser via `fig.show()`.
The figure object is also returned for further use:

```python
fig = enriched_histogram(filepath="data.csv", column="bweight")
fig.write_html("my_histogram.html")
fig.write_image("my_histogram.png", width=1200, height=750, scale=2)
```
Note: `write_image()` requires the `kaleido` package (`pip install kaleido`).
