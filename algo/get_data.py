#!/usr/bin/env python
import matplotlib
matplotlib.use('Agg')

import pandas_datareader as pdr
import pandas as pd
import datetime
import sys
import os
import json
# Import Matplotlib's `pyplot` module as `plt`
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy as cp
import sys

ticker = sys.argv[1]

fname = "data/ticker.csv"

df = pd.read_csv(fname)
print df
