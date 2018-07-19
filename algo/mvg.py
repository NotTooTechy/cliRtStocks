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

#INITIAL_CAPITAL = 5000.0
STEP_BUY_THERESHOLD =  -1
STEP_SELL_THRESHOLD = 6

class sma_return:
	def __init__(self, ticker, short_window=None):
		self.ticker = ticker.upper()
		self.short_window = short_window
		self.long_window = short_window
		self.step_buy_th = -1
		self.step_sell_th = 6 
		self.INITIAL_CAPITAL = 17000.0
		self.capital = None
		self.step_sell = 0 
		self.step_buy = 0
		self.buy_flag = True
		self.sell_fleg = False
		self.start = datetime.datetime(2017, 1, 1)
		self.end = datetime.datetime(2019, 1, 1)
		self.instr = None
		self.signals = None
		self.fprint = None
		self.profit = None
	
	def reset(self):
		self.long_window = self.short_window
		self.capital = None
		self.step_sell = 0 
		self.step_buy = 0
		self.buy_flag = True
		self.sell_fleg = False
		self.signals = None
		self.profit = None
	
	def get_data(self, fresh=True):
		fname = 'data/%s.csv'%self.ticker.lower()
		instr = pdr.get_data_yahoo(self.ticker, start=self.start, end=self.end)
		instr.to_csv(fname)
		df = pd.read_csv(fname, header=0, index_col='Date', parse_dates=True)
		return instr, df

	def get_signals(self, instr, df):
		self.capital = self.INITIAL_CAPITAL
		self.long_window = self.short_window
		#instr, df = self.get_data()
		self.signals = pd.DataFrame(index=instr.index)
		self.signals['signal'] = 0.0
		self.signals['close'] = instr['Close'].rolling(window=1, min_periods=1, center=False).mean()
		self.signals['short_mavg'] = instr['Close'].rolling(window=self.short_window, min_periods=1, center=False).mean()
		self.signals['long_mavg'] = instr['Close'].rolling(window=self.long_window, min_periods=1, center=False).mean()
		self.signals['signal'][self.short_window:] = np.where(self.signals['short_mavg'][self.short_window:] 
					> self.signals['long_mavg'][self.short_window:], 1.0, 0.0)
		size = len(self.signals['close']) 
		if self.fprint:
			print
			print 'Date\tClose\tShort_avg\tLong_avg'
		for i in range(size):
			date = self.signals.index[i]
			close = round(self.signals['close'][i], 2)
			short_mavg= round(self.signals['short_mavg'][i], 3)
			long_mavg= round(self.signals['long_mavg'][i], 3)
			if self.fprint:
				print date.date(), close, short_mavg, long_mavg,
			if close > short_mavg and close > long_mavg and i > 30 and self.buy_flag and self.capital > 500 and self.step_buy > self.step_buy_th:
				if self.fprint:
					print self.step_buy, '\tBUY at %.3f'%close, ' \t\tEnter capital %.3f'%self.capital,
				self.buy_flag = False
				self.sell_fleg = True
				buy_size = int(self.capital/close)
				captial_at_buy_time = self.capital
				leftover = buy_size*buy_size - 10
				self.capital = self.capital - buy_size*close
				self.step_buy=0
				#print date, 'Buying at %s, size: %s'%(close, buy_size),
				if self.fprint:
					pass#print '\t\tExit capital', capital,
			elif close < short_mavg and i > 30 and self.sell_fleg and self.step_sell>self.step_sell_th:
				if self.fprint:
					print '\tSELL at', close, '\t\tEnter capital', capital,'\t\t',
				self.buy_flag = True
				self.sell_fleg = False
				self.step_sell=0
				self.capital += buy_size*close-10
				if self.fprint:
					print '\t\tExit capital', self.capital,'\t\t', self.capital - captial_at_buy_time,
					if  self.capital - captial_at_buy_time >0:
						print "\t\t", "GAIN",
					else:
						print "\t\t", "LOSS",
			elif close > short_mavg and close > long_mavg and i > 30 and self.buy_flag and self.capital > 500:
				self.step_sell=0
				self.step_buy+=1
			elif 1*close < short_mavg and i > 30 and self.sell_fleg:
				self.step_sell+=1
			else:
				pass#self.step_sell = 0
			if self.fprint:
				print self.step_sell
		if not self.buy_flag:
			self.capital += buy_size*close -10
		self.profit = self.capital - self.INITIAL_CAPITAL
		if self.fprint:
			print
			print self.ticker.upper(), '\t',
			print "{:,}".format(self.INITIAL_CAPITAL), "{:,}".format(self.capital), '\tprofit:',"{:,}".format(self.profit)
		return self.capital
