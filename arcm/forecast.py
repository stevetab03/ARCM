"""
ARCM Sequential Distributional Forecasting
Created by Liyuan Zhang
============================================
LSTM-based distributional forecast of the 1-year Treasury yield
trained with an asymmetric quantile loss derived from the convexity
structure of the held ZCB position.

The asymmetric loss objective and optimal quantile level tau_q* = 0.74
are derived in full in the ARCM technical monograph (Section 5).

Multi-horizon training:
  The LSTM predicts yield at 21, 63, 126, and 252 trading days ahead
  simultaneously. This produces ~40x more training signal from the same
  dataset relative to a single-horizon objective, resolving the data
  scarcity problem while preserving the LSTM sequential learning capacity.
  The 252-day forecast remains the primary output for position analytics.

Input:
  - outputs/powerbi/regime_timeline.csv
  - outputs/powerbi/curve_factors.csv

Output:
  - outputs/powerbi/forecast_distribution.csv
  - outputs/powerbi/forecast_current.csv
  - outputs/powerbi/training_history.csv
  - outputs/models/lstm_model.pt
  - outputs/models/lstm_scaler.pkl

Usage:
  python forecast.py
  python forecast.py --epochs 200
  python forecast.py --no_retrain
  python forecast.py --start_date 2010-01-01
"""

import logging
import argparse
import warnings
import pickle
import numpy as np
import pandas as pd
import torch
import torch.nn as nn

from pathlib import Path
from torch.utils.data import Dataset, DataLoader

warnings.filterwarnings("ignore")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

#######################################
#                                     #
#    Contact me for my source code    #
#                                     #
#######################################

if __name__ == "__main__":
    main()
