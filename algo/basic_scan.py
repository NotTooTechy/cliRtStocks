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
import json

g = open('consider2.txt', 'w')
with open("/home/cabox/workspace/cliRtStocks/links.json", 'r') as f:
	data = json.load(f)
for symb in data.keys():
	ticker = symb.replace(".", "-")
	ticker += ".TO"
	try:
		instr = pdr.get_data_yahoo(ticker, 
				  start=datetime.datetime(2018, 1, 1), 
				  end=datetime.datetime(2018, 8, 1))
		print instr.tail()
	except:
		continue

	adj_close_px = instr['Adj Close']
	moving_avg = adj_close_px.rolling(window=20).mean()
	# Inspect the result
	print(moving_avg[-10:])

	# Short moving window rolling mean

	# Plot the adjusted closing price, the short and long windows of rolling means
	# Show plot
	if adj_close_px[-1] >moving_avg[-1]:
		g.write('->' + ticker)
		print '\t'*9, 'Consider'.upper(), ticker
g.close()
