"""
ARCM Regime Detection
Created by Liyuan Zhang
=======================
Latent Fed policy regime identification via Gaussian Hidden Markov Model.
Implemented in pure numpy — no hmmlearn dependency.

Input:
  - outputs/powerbi/curve_factors.csv   (from pipeline.py)

Output:
  - outputs/powerbi/regime_timeline.csv  daily regime assignments and probabilities
  - outputs/powerbi/regime_stats.csv     per-regime summary statistics

Algorithm:
  - Parameter estimation : Baum-Welch (EM)
  - State decoding       : Viterbi
  - Smoothed posteriors  : Forward-Backward

Usage:
  python regime.py
  python regime.py --n_regimes 3
  python regime.py --no_retrain
"""

import logging
import argparse
import warnings
import pickle
import numpy as np
import pandas as pd

from pathlib import Path

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
