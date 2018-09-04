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
from __init__ import START_DATE, END_DATE

#INITIAL_CAPITAL = 5000.0
STEP_BUY_THERESHOLD =  -1
STEP_SELL_THRESHOLD = 6
#STEP_SELL_THRESHOLD = 1

short_window = 20
long_window = 50
long_window = 10

fprint = json.loads(os.environ.get('fprint','false').lower())

def sma_return(ticker, short_window, INITIAL_CAPITAL=17.0*1000.0, step_buy_th=STEP_BUY_THERESHOLD, step_sell_th=STEP_SELL_THRESHOLD):
	capital = INITIAL_CAPITAL
	buy_flag = True
	sell_flag = False
	step_sell = 0
	step_buy = 0
	#long_window = short_window
	instr = pdr.get_data_yahoo(ticker,
	                          #start=datetime.datetime(2017, 7, 1),
	                          start=START_DATE,
	                          end=END_DATE)
	fname = 'data/%s.csv'%ticker
	if not os.path.exists(fname):
	  instr.to_csv(fname)
	df = pd.read_csv(fname, header=0, index_col='Date', parse_dates=True)
	signals = pd.DataFrame(index=instr.index)
	signals['signal'] = 0.0
	signals['close'] = instr['Close'].rolling(window=1, min_periods=1, center=False).mean()
	signals['short_mavg'] = instr['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
	signals['short_max_avg'] = instr['Close'].rolling(window=short_window, min_periods=1, center=False).max()
	signals['long_mavg'] = instr['Close'].rolling(window=long_window, min_periods=1, center=False).mean()
	signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:]
	                                            > signals['long_mavg'][short_window:], 1.0, 0.0)
	size = len(signals['close'])
	if fprint:
		print
		print 'Date\tClose\tShort_avg\tLong_avg'
	for i in range(size):
		date = signals.index[i]
		close = round(signals['close'][i], 2)
		short_mavg= round(signals['short_mavg'][i], 3)
		long_mavg= round(signals['long_mavg'][i], 3)
		max_avg= round(signals['short_max_avg'][i], 3)
		if fprint:
			#print date.date(), close, short_mavg, max_avg, #long_mavg,
			print '%-12s%-10s%-10s%-10s'%(date.date(), close, short_mavg, max_avg), #long_mavg,
		if close > short_mavg and close > long_mavg and i > 30 and buy_flag and capital > 500 and step_buy > step_buy_th:
			if fprint:
				print '\tBUY at %.3f'%close, ' \t\tEnter capital %.3f'%capital,
			buy_flag = False
			sell_flag = True
			buy_size = int(capital/close)
			captial_at_buy_time = capital
			leftover = buy_size*buy_size - 10
			capital = capital - buy_size*close
			step_buy=0
			#print date, 'Buying at %s, size: %s'%(close, buy_size),
			if fprint:
				pass#print '\t\tExit capital', capital,
		elif close < short_mavg and i > 30 and sell_flag and step_sell>step_sell_th:
			if fprint:
				print '\tSELL at', close, '\t\tEnter capital', capital,'\t\t',
			buy_flag = True
			sell_flag = False
			step_sell=0
			step_buy=0
			capital += buy_size*close-10
			if fprint:
				print '\t\tExit capital', capital,'\t\t', capital - captial_at_buy_time,
				if  capital - captial_at_buy_time >0:
					print "\t\t", "GAIN",
				else:
					print "\t\t", "LOSS",
		elif close > short_mavg and close > long_mavg and i > 30 and buy_flag and capital > 500:
			step_sell=0
		elif 1*close < short_mavg and i > 30 and sell_flag:
			step_sell+=1
		else:
			step_buy+=1
			pass#step_sell = 0
		if fprint:
			print step_sell

	if not buy_flag:
		capital += buy_size*close -10
	if fprint or True:
		print
		print ticker.upper(), '\t',
		print "{:,}".format(INITIAL_CAPITAL), "{:,}".format(capital), '\tprofit:',"{:,}".format(capital - INITIAL_CAPITAL)
	return capital

if __name__=='__main__':
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
	_ticker = sys.argv[1]
	if any("capital" in s for s in sys.argv):
		index = [i for i, s in enumerate(sys.argv) if 'capital' in s][0]
		capital = sys.argv[index].split('=')[1]
		capital = float(capital)
		sma_return(_ticker, INITIAL_CAPITAL=capital,short_window=sshort)
	else:
		sma_return(_ticker, short_window=sshort)
