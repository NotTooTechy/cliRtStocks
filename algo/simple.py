import mvg
import datetime
import sys
import json

fprint = False
if 'debug' in sys.argv:
	fprint = True
fjson= False
if 'json' in sys.argv:
	fjson= True
if any("days" in s for s in sys.argv):
                index = [i for i, s in enumerate(sys.argv) if 'days' in s][0]
                days = sys.argv[index].split('=')[1]
                days = int(days)
if any("ticker" in s for s in sys.argv):
                index = [i for i, s in enumerate(sys.argv) if 'ticker' in s][0]
                t = sys.argv[index].split('=')[1]
		stocks = [t]
else:
	stocks = ['hou.to', 'acb.to', 'bb.to', 'cpg.to', 'pd.to', 'obe.to', 'meg.to', 'bbd-b.to', 
			'aapl', 'et.to', 'jtr.v', 'pyr.v', 'cve.to', 'gbtc']
	#stocks = ['et.to', 'sev.to', 'pyr.v', 'obe.to', 'bb.to', 'jtr.v', 'hwo.to']
#Estocks = ['bb.to']
#stocks = ['ge']
BEGIN = datetime.datetime(2017, 7, 1)
END = datetime.datetime.now()
#BEGIN = datetime.datetime(2018, 1, 1)
#END = datetime.datetime(2017, 11, 5)
#days = 14
total_initial = 0
total = 0
mvg_dict = {}
for ticker in stocks:
	window_dict= {}
	max_list = []
	max_window = -1.0
	max_profit = -9999.0
	max_capital = -9999.0
	stock = mvg.sma_return(ticker)
	stock.INITIAL_CAPITAL = 5000.0
	#now = datetime.datetime.now()
	stock.start = BEGIN
	stock.end = END
	#stock.end = END
	#stock.step_buy_th = 2
	print "%-20s\t"%stock.ticker, stock.start.date(), "\t", stock.end.date(),"\t",
	instrument, df = stock.get_data()
	for window in range(2, 30):
		stock.reset()
		stock.short_window = window
		stock.get_signals(instrument, df)
		window_dict[window] = stock.profit
		if fprint:
			print window,"\t",
			print stock.INITIAL_CAPITAL, "\t",
			print stock.capital, "\t",
			print "%20.2f\t"%stock.profit
		if stock.profit > max_profit:
			max_window = window
			max_profit = stock.profit
		if stock.capital > max_capital:
			max_capital = stock.capital
	if fprint:
		print "-"*20
	print max_window, "\t", max_profit,
	max_list.append(max_window)
	print "\t", max_list
	total_initial += stock.INITIAL_CAPITAL
	total += max_capital
	mvg_dict[ticker]=max_window

print 'In:', total_initial, 'Out:', total
if fjson:
	with open('best_avg.json', 'w') as f:
		json.dump(mvg_dict, f, sort_keys = True, indent = 4)
