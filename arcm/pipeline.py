"""
ARCM Data Pipeline
Created by Liyuan Zhang
=======================
Adaptive Rate Curve Model — Yield Curve Factor Extraction for Power BI

Sources (all free, no API key required):
  - Full Treasury par yield curve  : FRED public CSV  (10 maturities)
  - Federal Funds Rate             : FRED public CSV  (series FEDFUNDS)

Outputs (Power BI CSVs):
  - curve_panel.csv          daily: raw yields, NS factors, curve shape metrics
  - curve_factors.csv        NS factors only — primary modelling input
  - fed_funds.csv            Federal Funds Rate with regime annotations
  - position_summary.csv     Position-level metrics for CUSIP 912797UE5

On-demand usage:
  python pipeline.py
  python pipeline.py --start 2000-01-01
  python pipeline.py --start 2000-01-01 --end 2026-04-18
  python pipeline.py --cusip 912797UE5 --purchase_price 96.439575 \
                     --purchase_date 2026-04-17
"""

import logging
import argparse
import warnings
import numpy as np
import pandas as pd
import requests

from io import StringIO
from pathlib import Path
from datetime import datetime

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
