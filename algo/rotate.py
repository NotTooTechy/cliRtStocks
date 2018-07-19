import mvg
import datetime
import sys

fprint = False
if 'debug' in sys.argv:
	fprint = True
if any("days" in s for s in sys.argv):
                index = [i for i, s in enumerate(sys.argv) if 'days' in s][0]
                days = sys.argv[index].split('=')[1]
                days = int(days)
if any("ticker" in s for s in sys.argv):
                index = [i for i, s in enumerate(sys.argv) if 'ticker' in s][0]
                t = sys.argv[index].split('=')[1]
		stocks = [t]
else:
	stocks = ['hou.to']
#Estocks = ['bb.to']
#stocks = ['ge']

#days = 14
for ticker in stocks:
	window_dict= {}
	max_list = []
	max_window = -1.0
	max_profit = -9999.0
	stock = mvg.sma_return(ticker)
	now = datetime.datetime.now()
	for i in range(5):
		start_dayshift = i*days + 365 - 150
		end_dayshift = i*days 
		stock.start = now - datetime.timedelta(days=start_dayshift)
		stock.end = now - datetime.timedelta(days=end_dayshift)
		print stock.ticker, stock.start.date(), stock.end.date(),
		instrument, df = stock.get_data()
		for window in range(2, 30):
			stock.reset()
			stock.short_window = window
			stock.get_signals(instrument, df)
			window_dict[window] = stock.profit
			if fprint:
				print window,
				print stock.INITIAL_CAPITAL,
				print stock.capital, 
				print stock.profit
			if stock.profit > max_profit:
				max_window = window
				max_profit = stock.profit
		print max_window, max_profit
		print
		max_list.append(max_window)

print max_list


