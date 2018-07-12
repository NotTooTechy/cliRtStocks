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
from copy import deepcopy as cp

short_window = 20
long_window = 40

fprint = False 
if 'debug' in sys.argv:
	fprint = True 
if any("short" in s for s in sys.argv):
	index = [i for i, s in enumerate(sys.argv) if 'short' in s][0]
	sshort = sys.argv[index].split('=')[1]
	sshort = int(sshort)
	short_window = sshort
	long_window = sshort
if any("long" in s for s in sys.argv):
	index = [i for i, s in enumerate(sys.argv) if 'long' in s][0]
	llong = sys.argv[index].split('=')[1]
	long_window = int(llong)
ticker = sys.argv[1]
instr = pdr.get_data_yahoo(ticker, 
                          start=datetime.datetime(2018, 1, 1), 
                          end=datetime.datetime(2019, 5, 1))
fname = 'data/%s.csv'%ticker
if not os.path.exists(fname):
  instr.to_csv(fname)
df = pd.read_csv(fname, header=0, index_col='Date', parse_dates=True)
if fprint:
	print instr.tail()

# Initialize the short and long windows

# Initialize the `signals` DataFrame with the `signal` column
signals = pd.DataFrame(index=instr.index)
signals['signal'] = 0.0


signals['close'] = instr['Close'].rolling(window=1, min_periods=1, center=False).mean()
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
if fprint:
	print '*'*100
	#print(signals)
	print '*'*100
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
#print(portfolio.head())
'''
print 'signals'
print signals['short_mavg']
print type(signals['short_mavg'])
print dir(signals['short_mavg'])
for loop in signals['short_mavg']:
	print loop
'''
#print
size = len(signals['close'])
capital = 22000.0
icapital = cp(capital)
buy_flag = True
sell_flag = False
step_sell = 0
step_sell_th = 6 
if fprint:
	print
	print 'Date\tClose\tShort_avg\tLong_avg'
for i in range(size):
	date = signals.index[i]
	close = round(signals['close'][i], 2)
	short_mavg= round(signals['short_mavg'][i], 3)
	long_mavg= round(signals['long_mavg'][i], 3)
	if fprint:
		print date.date(), close, short_mavg, long_mavg,
	if close > short_mavg and close > long_mavg and i > 30 and buy_flag and capital > 500:
		if fprint:
			print '\tBUY at', close, ' \t\tEnter capital', capital, 
		buy_flag = False
		sell_flag = True
		buy_size = int(capital/close)
		leftover = buy_size*buy_size - 10
		capital = capital - buy_size*close
		#print date, 'Buying at %s, size: %s'%(close, buy_size),
		if fprint:
			print '\t\tExit capital', capital,
	elif 1*close < short_mavg and i > 30 and sell_flag and step_sell>step_sell_th:
		if fprint:
			print '\tSELL at', close, '\t\tEnter capital', capital,
		buy_flag = True
		sell_flag = False
		step_sell=0
		capital += buy_size*close-10 
		#print date, 'Selling at', signals['close'][i],
		if fprint:
			print '\t\tExit capital', capital,
	elif 1*close < short_mavg and i > 30 and sell_flag:
		step_sell+=1
	if fprint:
		print step_sell
	
if not buy_flag:
	capital += buy_size*close -10 
print
print ticker.upper(), '\t', 
print icapital, capital, '\tprofit:',capital - icapital
