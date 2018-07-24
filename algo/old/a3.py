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


ticker = sys.argv[1]
instr = pdr.get_data_yahoo(ticker, 
                          start=datetime.datetime(2018, 1, 1), 
                          end=datetime.datetime(2018, 8, 1))
fname = 'data/%s.csv'%ticker
if not os.path.exists(fname):
  instr.to_csv(fname)
df = pd.read_csv(fname, header=0, index_col='Date', parse_dates=True)
print instr.tail()
# Calculate the moving average

adj_close_px = instr['Adj Close']
moving_avg = adj_close_px.rolling(window=20).mean()
# Inspect the result
print(moving_avg[-10:])

# Short moving window rolling mean
instr['42'] = adj_close_px.rolling(window=40).mean()

# Long moving window rolling mean
instr['252'] = adj_close_px.rolling(window=252).mean()

# Plot the adjusted closing price, the short and long windows of rolling means
instr[['Adj Close', '42', '252']].plot()

# Show plot
plt.show()
