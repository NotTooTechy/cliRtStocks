#!/usr/bin/env python
import matplotlib
matplotlib.use('Agg')

import pandas_datareader as pdr
import pandas as pd
import datetime 
import sys
import os
# Import Matplotlib's `pyplot` module as `plt`
import matplotlib.pyplot as plt

# tst ^GSPTSE
ticker = sys.argv[1]
instr = pdr.get_data_yahoo(ticker, 
                          start=datetime.datetime(2018, 1, 1), 
                          end=datetime.datetime(2018, 8, 1))
print instr.tail()
# Calculate the moving average

adj_close_px = instr['Adj Close']
moving_avg = adj_close_px.rolling(window=20).mean()
# Inspect the result
print(moving_avg[-10:])

# Short moving window rolling mean

# Plot the adjusted closing price, the short and long windows of rolling means
# Show plot
if adj_close_px[-1] >moving_avg[-1]:
	print '\t'*9, 'Consider'.upper()
