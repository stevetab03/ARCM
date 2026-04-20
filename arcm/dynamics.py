"""
ARCM Regime-Conditional Factor Dynamics
Created by Liyuan Zhang
========================================
Calibrates Ornstein-Uhlenbeck parameters for the Nelson-Siegel slope
factor beta2 within each detected policy regime via closed-form MLE.

This is the original analytical contribution of ARCM. The MLE estimators
are derived from first principles in the technical monograph (Section 4).
No external calibration library is used.

Input:
  - outputs/powerbi/regime_timeline.csv   (from regime.py)

Output:
  - outputs/powerbi/regime_dynamics.csv   OU parameters per regime
  - outputs/powerbi/ou_paths.csv          fitted vs actual beta2 per regime
  - outputs/models/ou_params.pkl          serialised parameter estimates

The closed-form estimators (Theorem 1, monograph) are:

    kappa  = -1/Delta * log( (S*Sxy - Sx*Sy) / (S*Sxx - Sx^2) )
    theta  = (Sy*Sxx - Sx*Sxy) / ( S*(Sxx - Sxy) - (Sx^2 - Sx*Sy) )
    eta^2  = 2*kappa / (1 - exp(-2*kappa*Delta)) * [residual variance]

where S, Sx, Sy, Sxx, Sxy are sufficient statistics over the regime
observations and Delta is the time step in years.

Usage:
  python dynamics.py
  python dynamics.py --timeline_path outputs/powerbi/regime_timeline.csv
"""

import logging
import argparse
import warnings
import pickle
import numpy as np
import pandas as pd
import scipy.stats as stats

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
