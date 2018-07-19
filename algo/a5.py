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
import numpy as np


ticker = sys.argv[1]
instr = pdr.get_data_yahoo(ticker, 
                          start=datetime.datetime(2017, 1, 1), 
                          end=datetime.datetime(2018, 8, 1))j
fname = 'data/%s.csv'%ticker
if not os.path.exists(fname):
  instr.to_csv(fname)
df = pd.read_csv(fname, header=0, index_col='Date', parse_dates=True)
print instr.tail()

# Initialize the short and long windows
short_window = 20
long_window = 60

# Initialize the `signals` DataFrame with the `signal` column
signals = pd.DataFrame(index=instr.index)
signals['signal'] = 0.0

# Create short simple moving average over the short window
signals['short_mavg'] = instr['Close'].rolling(window=short_window, min_periods=1, center=False).mean()

# Create long simple moving average over the long window
signals['long_mavg'] = instr['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

# Create signals
signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] 
                                            > signals['long_mavg'][short_window:], 1.0, 0.0)   

# Generate trading orders
signals['positions'] = signals['signal'].diff()

# Print `signals`
print(signals)
# Set the initial capital
initial_capital= float(10000.0)

# Create a DataFrame `positions`
positions = pd.DataFrame(index=signals.index).fillna(0.0)

# Buy a 100 shares
positions[ticker] = 100*signals['signal']   
  
# Initialize the portfolio with value owned   
portfolio = positions.multiply(instr['Adj Close'], axis=0)

# Store the difference in shares owned 
pos_diff = positions.diff()

# Add `holdings` to portfolio
portfolio['holdings'] = (positions.multiply(instr['Adj Close'], axis=0)).sum(axis=1)

# Add `cash` to portfolio
portfolio['cash'] = initial_capital - (pos_diff.multiply(instr['Adj Close'], axis=0)).sum(axis=1).cumsum()   

# Add `total` to portfolio
portfolio['total'] = portfolio['cash'] + portfolio['holdings']

# Add `returns` to portfolio
portfolio['returns'] = portfolio['total'].pct_change()

# Print the first lines of `portfolio`
print(portfolio.head())


