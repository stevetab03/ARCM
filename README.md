# ARC: Adaptive Rate Curve

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Methods: NS · HMM · LSTM](https://img.shields.io/badge/Methods-NS_%7C_HMM_%7C_LSTM-blueviolet)](https://github.com/stevetab03/ARC)
[![Domain: US Fixed Income](https://img.shields.io/badge/Domain-US_Fixed_Income-success)](https://github.com/stevetab03/ARC)
[![Dashboard: Power BI](https://img.shields.io/badge/Dashboard-Power_BI-F2C811?logo=powerbi&logoColor=black)](https://github.com/stevetab03/powerbi-dax-patterns)

**Author:** Liyuan Zhang  
**Status:** Active Development

---

## Motivation

In April 2026, I entered a long position in 1-year US Treasury bill (CUSIP 912797UE5) at $96.439575 —
an implied yield of approximately 3.69%. The purchase was straightforward. What was
not straightforward was the analytical question it raised:

> *Standard yield curve models assume factor dynamics are stationary across Fed policy
> regimes. They are not. The 2022–2023 hiking cycle and the 2026 geopolitical
> escalation produced structural breaks in how the curve level, slope, and curvature
> co-move — breaks that a single fitted model cannot capture. What does a
> regime-aware framework say about where the 1-year rate is going, and was this
> a good entry point?*

ARC is the answer to that question. It is not an academic exercise. It is an
analytical framework built around a real position, designed to be updated as
the position approaches maturity.

---

## The Problem with Standard Approaches

The dominant fixed income analytical stack — Nelson-Siegel factor extraction
followed by OLS or VAR forecasting — has a well-known but rarely quantified
failure mode: it estimates a single set of factor dynamics across the full
historical sample, implicitly assuming that the yield curve behaves the same
way whether the Fed is hiking, cutting, or on hold.

It does not. Three structural breaks are visible in the 2000–2026 data:

- The zero-lower-bound era (2009–2015), where the slope factor lost its
  mean-reversion property entirely
- The 2022–2023 hiking cycle, the fastest in 40 years, where slope dynamics
  were non-stationary at the monthly scale
- The 2026 geopolitical regime, where the short end decoupled from the long
  end in a pattern not seen in the post-GFC data

A model that ignores these breaks produces forecasts that are precise but
miscalibrated — high confidence in the wrong distribution.

---

## The ARC Framework

ARC addresses this in three sequential layers.

### Layer 1 — Yield Curve Decomposition

The Treasury curve is decomposed daily into three interpretable factors using
the Nelson-Siegel parameterization:

$$y(\tau) = \beta_1 + \beta_2 \left(\frac{1 - e^{-\tau/\lambda}}{\tau/\lambda}\right) + \beta_3 \left(\frac{1 - e^{-\tau/\lambda}}{\tau/\lambda} - e^{-\tau/\lambda}\right)$$

where $\beta_1$ is the **level** (long-run rate), $\beta_2$ is the **slope**
(short-end premium, the primary signal for rate direction), and $\beta_3$ is
the **curvature** (policy uncertainty hump). The decay parameter $\lambda$
controls the maturity at which $\beta_3$ achieves its maximum loading.

The slope factor $\beta_2(t)$ is the central object of study. It is the
market's implicit forecast of rate direction — negative values signal inversion,
positive values signal steepening, and its dynamics under different Fed regimes
are the core empirical question.

### Layer 2 — Regime Detection and Factor Dynamics

The slope factor time series is not stationary in the classical sense.
Its distributional properties — mean, variance, autocorrelation structure —
shift discretely as monetary policy regime changes. ARC identifies these
latent regime transitions using an unsupervised probabilistic approach that
requires no manual labeling of Fed cycle dates.

Within each detected regime, the slope factor dynamics are characterized
analytically. The calibration methodology draws on established results
from continuous-time stochastic processes — specifically the relationship
between the observed discrete time series and the underlying continuous
dynamics — adapted here to the multi-regime setting.

The regime-conditional characterization is the structural innovation of ARC.
The full mathematical treatment is reserved for the forthcoming technical note.

### Layer 3 — Regime-Aware Sequential Forecasting

A recurrent neural network architecture is trained on the full NS factor
time series to produce distributional forecasts of the 1-year yield at the
target horizon — the maturity date of the held position.

The model is trained with an asymmetric objective that reflects the actual
economic exposure of a long duration position: a forecast error in the
direction of rising rates is penalized more severely than an equivalent error
in the direction of falling rates. This is not a modeling convention. It is
a direct consequence of the convexity structure of fixed income positions.

The output is not a point forecast. It is a calibrated forecast interval
centered on the conditional distribution for the current detected regime,
updated daily as new curve data is ingested.

---

## What ARC Produces

Three analytical outputs, each actionable:

**Current Regime State**
Which of the identified policy regimes is the market currently in, with what
probability, and how long has this regime persisted? This is the first thing
to know before interpreting any rate forecast.

**Slope Factor Dynamics**
Given the current regime, what are the calibrated mean-reversion parameters
for $\beta_2(t)$? Where is the slope expected to revert, and on what timescale?
This directly characterizes the rate environment over the holding period.

**1-Year Rate Forecast at Maturity**
A distributional forecast for the 1-year rate at the target date, conditioned
on the current regime. Presented as a central estimate with asymmetric confidence
bands reflecting the actual risk structure of the position.

---

## Data

All inputs are publicly available. No proprietary data sources are required.

| Source | Series | Frequency |
|--------|--------|-----------|
| [FRED](https://fred.stlouisfed.org) | Full Treasury par yield curve (3m–30yr) | Daily |
| [FRED](https://fred.stlouisfed.org) | Federal Funds Rate, policy announcements | Daily |
| [TreasuryDirect](https://www.treasurydirect.gov) | T-bill auction prices and yields | Weekly |

The pipeline runs fully automated via `fredapi`. No manual downloads required.

---

## Repository Structure

```
ARC/
├── README.md
├── arc/
│   ├── pipeline.py          FRED ingestion and curve construction
│   ├── nelson_siegel.py     NS factor extraction and daily update
│   ├── regime.py            Latent regime detection
│   ├── dynamics.py          Regime-conditional factor characterization
│   ├── forecast.py          Sequential distributional forecasting
│   └── position.py          Position-level P&L and risk attribution
├── notebooks/
│   ├── 01_curve_exploration.ipynb
│   ├── 02_regime_detection.ipynb
│   └── 03_forecast_and_position.ipynb
└── outputs/
    └── powerbi/
        ├── curve_factors.csv
        ├── regime_timeline.csv
        └── forecast_distribution.csv
```

---

## Dashboard

The Power BI dashboard consuming ARC's pipeline outputs is maintained in
[stevetab03/powerbi-dax-patterns](https://github.com/stevetab03/powerbi-dax-patterns).
Three pages — curve monitor, regime timeline, position forecast — built on the
same DAX architecture documented in that repository.

---

## Connection to ORBIT

[ORBIT](https://github.com/stevetab03/ORBIT) established a rigorous framework
for basis convergence in commodity futures, demonstrating that variance collapse
is provable from first principles when the convergence mechanism is contractually
enforced. ARC operates in the same intellectual register but in a different
market: the convergence being studied is not futures-to-spot but
rate-forecasts-to-realized-rates across policy regime boundaries.

The shared insight: *the dynamics that matter most are the ones that are
structurally different across regimes, not the ones that are stable.*

---

## Status

| Component | Status |
|-----------|--------|
| FRED pipeline and NS fitting | In development |
| Regime detection | In development |
| Factor dynamics calibration | In development |
| Sequential forecasting | Planned |
| Power BI dashboard | Planned |
| Technical note | Forthcoming |

---

## Contact

**LinkedIn:** https://www.linkedin.com/in/hlzhang/  
**GitHub:** https://github.com/stevetab03
