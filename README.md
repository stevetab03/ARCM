# ARCM: Adaptive Rate Curve Model

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Methods: NS · HMM · OU · LSTM](https://img.shields.io/badge/Methods-NS_%7C_HMM_%7C_OU_%7C_LSTM-blueviolet)](https://github.com/stevetab03/ARCM)
[![Domain: US Fixed Income](https://img.shields.io/badge/Domain-US_Fixed_Income-success)](https://github.com/stevetab03/ARCM)
[![Dashboard: Power BI](https://img.shields.io/badge/Dashboard-Power_BI-F2C811?logo=powerbi&logoColor=black)](https://github.com/stevetab03/powerbi-dax-patterns)

**Author:** Liyuan Zhang  
**Status:** Active Research & Development / Portfolio Showcase  

_To protect my IP, all Jupyter notebooks have been converted to HTML format using the nbconvert --no-input command. This process ensures that only the research outputs and visualizations are shared within the repository, while the underlying source code remains restricted._ 

---

## Motivation

In April 2026, the author entered a long position in a 1-year US Treasury
bill (CUSIP 912797UE5) at \$96.439575 — an implied yield of approximately
3.69%. The purchase was straightforward. The analytical question it raised
was not:

> *Standard yield curve models assume factor dynamics are stationary across
> Fed policy regimes. They are not. The 2022–2023 hiking cycle and the 2026
> geopolitical escalation produced structural breaks in how the curve level,
> slope, and curvature co-move — breaks that a single fitted model cannot
> capture. What does a regime-aware framework say about where the 1-year rate
> is going, and was this a good entry point?*

ARCM is the answer to that question. It is not an academic exercise. It is
an analytical framework built around a real position, updated on demand as
the position approaches maturity.

---

## The Problem with Standard Approaches

The dominant fixed income analytical stack — Nelson-Siegel factor extraction
followed by OLS or VAR forecasting — has a well-known but rarely quantified
failure mode: it estimates a single set of factor dynamics across the full
historical sample, implicitly assuming the yield curve behaves the same way
whether the Fed is hiking, cutting, or on hold.

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

## The ARCM Framework

ARCM addresses this in three sequential layers, each with a distinct
technical contribution.

### Layer 1 — Yield Curve Decomposition

The Treasury curve is decomposed daily into three interpretable factors
using the Nelson-Siegel parameterization:

$$y(\tau) = \beta_1 + \beta_2 \left(\frac{1 - e^{-\tau/\lambda}}{\tau/\lambda}\right) + \beta_3 \left(\frac{1 - e^{-\tau/\lambda}}{\tau/\lambda} - e^{-\tau/\lambda}\right)$$

where $\beta_1$ is the **level**, $\beta_2$ is the **slope** (the primary
signal for rate direction), and $\beta_3$ is the **curvature**. The slope
factor $\beta_2(t)$ is the central object of study — negative values signal
inversion, positive values signal steepening.

### Layer 2 — Regime Detection and Factor Dynamics

The slope factor time series is not stationary in the classical sense.
ARCM identifies latent policy regime transitions using a Gaussian Hidden
Markov Model implemented in pure numpy — no external HMM library required.
Three regimes are learned without manual labelling:

| Regime | β₂ mean | Avg episode | Interpretation |
|--------|---------|-------------|----------------|
| Easing | −8.92% | 145 days | Inverted curve, cutting cycle |
| Neutral | +1.19% | 294 days | Flat curve, plateau |
| Tightening | +8.44% | 180 days | Steep curve, hiking cycle |

Within each detected regime, the slope factor dynamics are characterised
analytically using a closed-form MLE calibration of an Ornstein-Uhlenbeck
process — the original contribution of ARCM documented in the technical
monograph.

### Layer 3 — Regime-Aware Sequential Forecasting

A multi-horizon LSTM produces distributional forecasts of the 1-year yield
at four horizons simultaneously: 21, 63, 126, and 252 trading days. Training
on multiple horizons jointly generates approximately 40× more training signal
from the same dataset, resolving the data scarcity problem inherent to
year-ahead forecasting on a post-ZLB training set.

The model is trained with an asymmetric quantile loss whose optimal quantile
level τ_q\* = 0.74 is derived directly from the convexity structure of the
held ZCB position — underpredicting rates is penalised 2.85× more heavily
than overpredicting, encoding the actual economic exposure of the position.

---

## Original Contributions

The following are not available in this form in the published literature:

**Regime-conditional OU MLE.** Closed-form maximum likelihood estimators
for Ornstein-Uhlenbeck parameters specific to each latent regime, derived
from the exact Gaussian transition density. Standard errors expressed as
functions of regime occupancy. Full derivation: monograph Section 4.

**Asymmetric quantile objective for ZCB positions.** Derivation of the
optimal quantile level τ_q\* = τ²P / (2 + τ²P) from the convexity
structure of a long zero-coupon bond, with the gradient explicitly computed
for LSTM backpropagation. Full derivation: monograph Section 5.

**Position analytics for CUSIP 912797UE5.** Regime-conditional DV01,
modified duration, expected yield at maturity, and rate-rise probability
expressed as closed-form functions of the calibrated OU parameters and
current Nelson-Siegel factors for the specific held instrument.

---

## Current Results (as of April 19, 2026)

**Detected regime:** Tightening (confidence 1.0)
**Current β₂:** +10.77% — above tightening equilibrium of +8.44%
**OU half-life in tightening:** 5 days

**OU regime-conditional forecast:**
Expected yield at maturity: 3.872% | P(rates rise): 91.4% | P(rates fall): 8.6%

**LSTM multi-horizon forecast:**

| Horizon | Q10 | Q50 | Q74 (ZCB-optimal) |
|---------|-----|-----|-------------------|
| 21d | 2.80% | 3.11% | 3.25% |
| 63d | 2.25% | 2.95% | 3.28% |
| 126d | 2.76% | 3.10% | 3.40% |
| 252d | 2.49% | 3.05% | 3.34% |

Purchase yield: 3.622%. The central forecast implies modest rate decline
over the holding period, consistent with β₂ above tightening equilibrium
mean-reverting toward its regime attractor.

*LSTM calibration improves as post-2026 data accumulates.*

---

## Data

All inputs are publicly available. No API keys required.

| Source | Series | Frequency |
|--------|--------|-----------|
| [FRED](https://fred.stlouisfed.org) | Treasury par yields 3m–30yr | Daily |
| [FRED](https://fred.stlouisfed.org) | Federal Funds Rate | Monthly |

---

## Usage

All modules are on-demand. Run the full stack or any individual module:

```bash
python pipeline.py                    # fetch FRED data, fit NS factors
python regime.py                      # HMM regime detection
python dynamics.py                    # regime-conditional OU calibration
python forecast.py --epochs 200       # multi-horizon LSTM forecast
python position.py                    # P&L, DV01, scenario analysis
```

Each module reads from and writes to `outputs/powerbi/`. No scheduler
or automation required — run when you want fresh results.

---

## Repository Structure

```
ARCM/
├── README.md
├── arcm/
│   ├── pipeline.py        FRED ingestion, NS factor extraction
│   ├── regime.py          Gaussian HMM regime detection (pure numpy)
│   ├── dynamics.py        Regime-conditional OU calibration via MLE
│   ├── forecast.py        Multi-horizon LSTM + asymmetric quantile loss
│   └── position.py        Position P&L, DV01, scenario analysis
├── notebooks/
│   ├── 01_curve_exploration.ipynb
│   ├── 02_regime_detection.ipynb
│   └── 03_forecast_and_position.ipynb
└── outputs/
    ├── models/
    │   ├── hmm_model.pkl
    │   ├── ou_params.pkl
    │   ├── lstm_model.pt
    │   └── lstm_scaler.pkl
    └── powerbi/
        ├── curve_panel.csv
        ├── curve_factors.csv
        ├── fed_funds.csv
        ├── position_summary.csv
        ├── regime_timeline.csv
        ├── regime_stats.csv
        ├── regime_dynamics.csv
        ├── ou_paths.csv
        ├── position_analytics.csv
        ├── forecast_distribution.csv
        ├── forecast_current.csv
        ├── training_history.csv
        ├── position_report.csv
        └── scenario_analysis.csv
```

---

## Dashboard

The Power BI dashboard consuming ARCM outputs is maintained in
[stevetab03/powerbi-dax-patterns](https://github.com/stevetab03/powerbi-dax-patterns).
Built on the same DAX architecture documented in that repository.

---

## Technical Monograph

Full derivations of the original contributions are in `arcm_monograph.pdf`.
**Available upon request.**

---

## Connection to ORBIT

[ORBIT](https://github.com/stevetab03/ORBIT) established a rigorous framework
for basis convergence in commodity futures, demonstrating that variance
collapse is provable from first principles when the convergence mechanism
is contractually enforced. ARCM operates in the same intellectual register
in a different market: the convergence studied is not futures-to-spot but
rate-forecasts-to-realised-rates across policy regime boundaries.

The shared insight: *the dynamics that matter most are structurally different
across regimes, not the ones that are stable.*

---

## Status

| Component | Status |
|-----------|--------|
| FRED pipeline and NS fitting | Complete |
| Gaussian HMM regime detection | Complete |
| Regime-conditional OU calibration | Complete |
| Multi-horizon LSTM forecast | Complete |
| Position analytics and scenarios | Complete |
| Power BI dashboard | In development |
| Technical monograph | Complete — available on request |

---

## Contact

**Monograph:** Available upon request for full derivations, proofs, and theorem statements.    
**LinkedIn:** https://www.linkedin.com/in/hlzhang/  
**GitHub:** https://github.com/stevetab03
