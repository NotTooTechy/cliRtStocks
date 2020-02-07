#!/usr/bin/env python

import pandas as pd
import datetime as dt
import sys
import os
import json
import plotly
import plotly.graph_objs as go

# Import Matplotlib's `pyplot` module as `plt`
import numpy as np
from copy import deepcopy as cp
from __init__ import START_DATE, END_DATE, chk_arg

FONT_BUY=dict(family='Courier New, monospace', size=12, color='grey')
FONT_SELL_GREEN=dict(family='Courier New, monospace', size=16, color='green')
FONT_SELL_RED=dict(family='Courier New, monospace', size=18, color='red')


class tmethods:

	def __init__(self, ticker, cash, start=START_DATE, end=END_DATE):
		self.ticker = ticker
		self.cash = cash
		self.start = start
		self.end= end
		self.df = None
		self.mavg1 = 6
		self.mavg2 = 21
		self.annotations = []
		self.comment = None

	def load_data_from_csv(self):
		fname = 'ALPHA_STORAGE/%s.csv'%self.ticker
		df = pd.read_csv(fname, header=0, index_col='timestamp', parse_dates=True)
		df = df.iloc[::-1] # reversing dataframe
		self.df = df[(df.index > self.start) & (df.index <= self.end)]

	def set_moving_averages(self):
		min1 = "Min_%s"%self.mavg1
		avg1 = "Avg_%s"%self.mavg1
		max1 = "Max_%s"%self.mavg1

		min2 = "Min_%s"%self.mavg2
		avg2 = "Avg_%s"%self.mavg2
		max2 = "Max_%s"%self.mavg2
		# moving minimums
		self.df['min1'] = self.df['adjusted_close'].rolling(window=self.mavg1).min()
		self.df['min2'] = self.df['adjusted_close'].rolling(window=self.mavg2).min()
		# moving averages
		self.df['avg1'] = self.df['adjusted_close'].rolling(window=self.mavg1).mean()
		self.df['avg2'] = self.df['adjusted_close'].rolling(window=self.mavg2).mean()
		# moving maximums
		self.df['max1'] = self.df['adjusted_close'].rolling(window=self.mavg1).max()
		self.df['max2'] = self.df['adjusted_close'].rolling(window=self.mavg2).max()
		# differencies
		self.df['avg1-close'] = self.df['avg1'] - self.df['adjusted_close']
		self.df['avg2-close'] = self.df['avg2'] - self.df['adjusted_close']
		self.df['avg2-avg1'] = self.df['avg2'] - self.df['avg1']

	def strategy1(self):
		print ">"*20, self.start.date(), self.end.date(), "<"*20
		df_shifted_1 = self.df.shift(-1, axis=0)
		df_shifted_2 = self.df.shift(-2, axis=0)
		self.df['buy_signal'] = 0
		self.df['sell_signal'] = 0
		self.df['buy_signal'] = self.df[(self.df['avg1-close'] > 0) & (self.df['avg2-close'] <0) & (self.df['avg2-avg1'] <0)]
		self.df['sell_signal'] = self.df[(self.df['avg1-close'] > 0) & (self.df['avg2-close'] >0)&(self.df['avg2-avg1']>0)]
		self.df['trend'] = 10
		#df.loc[df['c1'] == 'Value', 'c2'] = 10
		self.df.loc[(self.df['close'] > df_shifted_1['close'])&(self.df['close']>df_shifted_2['close']), 'trend'] = 2
		#self.df['buy_signal'] = self.df[(self.df['avg1-close'] > 0) & (self.df['avg2-close'] <0) & (self.df['avg2-avg1'] <0) &(self.df['buy_signal'].notna())]
		self.result()

	def result(self, debug=False):
		df_shifted_1 = self.df.shift(1, axis=0)
		buy_flag = False
		sell_flag = False
		buy_price = 0
		sell_price = 0
		balance = 0
		count = 0
		nprofit = 0
		nloss = 0
		for i, row in self.df.iterrows():
			count+=1
			if debug and count>2:
				#print("%10s %8s(%5.2f) %8.2f %8.2f %8s %8s"%(i.date(), row['close'], df_shifted_1[df_shifted_1.index == i]['close'], row['avg2'], row['max2'], row['buy_signal'], row['sell_signal']))
				print("%10s %8s(%5.2f, %5.2f) %8.2f %8.2f .. %8s %8s"%(i.date(), row['close'], row['low'], row['high'], row['avg1'], row['avg1-close'], row['buy_signal'], row['sell_signal']))
			if row['buy_signal'] > 0 and not buy_flag:
				buy_flag = True
				sell_flag = False
				buy_price = row['close']
				buy_date = i.date()
				#print(buy_price)
				if balance == 0:
					self.cash -= 10
					nstock = int(self.cash/row['close']) 
					start_balance = buy_price*nstock
					balance = buy_price*nstock
				else:
					nstock = int(balance/buy_price)
				buy_balance = buy_price*nstock
				x = dict( x=i, y=row['close'], xref='x', yref='y', text='BUY', showarrow=True, arrowhead=1, ax=-40, ay=-70, font=FONT_BUY)
				self.annotations.append(x)
			elif row['sell_signal'] > 0 and buy_flag:
				buy_flag = False
				sell_price = row['close']
				balance = sell_price*nstock - 20
				sell_date = i.date()
				if (sell_price - buy_price) >=0 :
					nprofit += 1
					x = dict( x=i, y=row['close'], xref='x', yref='y', text='SELL', showarrow=True, arrowhead=1, ax=-30, ay=-70, font=FONT_SELL_GREEN)
					print("\tDate:%s\tBuy:\t%s\t\tDate:%s\tSell:\t%s\t\t\tPROFIT:\t%10s\t(%10s, %10s)"%(buy_date, buy_price, sell_date, sell_price, balance - buy_balance, start_balance, balance))
				else:
					x = dict( x=i, y=row['close'], xref='x', yref='y', text='SELL', showarrow=True, arrowhead=3, ax=-30, ay=-70, font=FONT_SELL_RED)
					print("\tDate:%s\tBuy:\t%s\t\tDate:%s\tSell:\t%s\t\t\t*LOSS:\t%10s\t(%10s, %10s)"%(buy_date, buy_price, sell_date, sell_price, balance - buy_balance, start_balance, balance))
					nloss += 1
				self.comment = "(start_capital:%s, balance:%s)"%(start_balance, balance)
				self.annotations.append(x)
		if buy_flag:
			print 'Still Holding: ... '
			current_price = row['close']
			balance = nstock*current_price
			print("Date:%s\tBuy:\t%s\t\tDate:%s\tCurrent :\t%s\t\t\tprofit:\t%s\t(%s, %s)"%(buy_date, buy_price, i, current_price, current_price - buy_price, start_balance, balance))
		print("nprofit: {}, nloss: {}".format(nprofit, nloss))
		#print self.df.info()

	def strategy2(self):
		#df_shifted_1 = self.df.shift(1, axis=0)
		print ">"*20, self.start.date(), self.end.date(), "<"*20
		self.df['buy_signal'] = 0
		self.df['sell_signal'] = 0
		#self.df['buy_signal'] = self.df[(self.df['close'] > self.df['avg2'])&(self.df['close'] >= self.df['max1'])]
		self.df['buy_signal'] = self.df[(self.df['close'] > self.df['avg2'])&(self.df.shift(1, axis=0)['close'] < self.df['close'])]
		#self.df['sell_signal'] = self.df[self.df['close'] >= self.df['max2']]
		self.df['sell_signal'] = self.df[self.df['close'] >= self.df['max2']]
		self.result()

	def strategy3(self):
		print ">"*20, self.start.date(), self.end.date(), "<"*20
		self.df['buy_signal'] = 0
		self.df['sell_signal'] = 0
		self.df['sell_signal'] = self.df[self.df['close'] < self.df['avg1']]
		self.df['buy_signal'] = self.df[(self.df['close'] > self.df['avg1'])&(self.df.shift(-1, axis=0)['close'] > self.df['close'])]
		#self.df['sell_signal'] = self.df[self.df['close'] >= self.df['max2']]


	def plotter(self):
		trace1 = go.Scatter(
			x=self.df.index, y=self.df['close'], # Data
			mode='lines', name='close'# Additional options
                )
		trace2 = go.Scatter(
			x=self.df.index, y=self.df['close'].rolling(window=self.mavg1, min_periods=1, center=False).mean(), # Data
			mode='lines', name="mean_%s"%self.mavg1, # Additional options
			visible="legendonly"
                )
		trace3 = go.Scatter(
			x=self.df.index, y=self.df['close'].rolling(window=self.mavg2, min_periods=1, center=False).mean(), # Data
			mode='lines', name="mean_%s"%self.mavg2, # Additional options
			visible="legendonly"
                )
		trace4 = go.Scatter(
			x=self.df.index, y=self.df['close'].rolling(window=self.mavg1, min_periods=1, center=False).max(), # Data
			mode='lines', name="max_%s"%self.mavg1, # Additional options
			visible="legendonly"
                )
		traces = []
		traces.append(trace1)
		traces.append(trace2)
		traces.append(trace3)
		traces.append(trace4)

		trace5 = go.Scatter(
			#x=self.df.index, y=self.df['trend'], #.rolling(window=50, min_periods=1, center=False).mean(), # Data
			#mode='lines', name="trend",
			x=self.df.index, y=self.df['close'].rolling(window=self.mavg2, min_periods=1, center=False).max(), # Data
			mode='lines', name="max_%s"%self.mavg2, # Additional options
			visible="legendonly"
                )
		traces.append(trace5)

		layout = go.Layout(title="%s, %s"%(self.ticker.upper(),self.comment), plot_bgcolor='rgb(230, 230,230)', annotations=self.annotations)
		fig = go.Figure(data=traces, layout=layout)
		plot_filename = "%s.html"%self.ticker
		plotly.offline.plot(fig, filename=plot_filename)

	def run_routine(self):
		self.load_data_from_csv()
		self.mavg1=6
		self.mavg2=21
		self.set_moving_averages()
		#self.strategy1()
		self.strategy2()
		self.plotter()

	def run_routine2(self, debug=False):
		self.load_data_from_csv()
		for i in range(6, 7):
			print i
			self.mavg1=i
			self.set_moving_averages()
			self.strategy3()
			self.result(debug)
			print
		#self.plotter()

if __name__=='__main__':
	import sys
	debug = False
	cash = 17000
	if 'debug' in sys.argv:
		debug = True
	if any('cash' in x for x in sys.argv[1:]):
		for x in sys.argv[1:]:
			if 'cash' in x:
				cash = float(x.split("=")[1])
		
	hou = tmethods('hou.to', cash)
	hou.run_routine2(debug)
