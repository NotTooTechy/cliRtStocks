import urllib,time,datetime
import  pandas as pd


# symbol, minutes = 60*m, number of days
LINK = '''https://www.google.com/finance/getprices?q=%s&i=%d&p=%dd&f=d,o,h,l,c,v'''




class gstock:
	LINK = '''https://www.google.com/finance/getprices?q=%s&i=%d&p=%dd&f=d,o,h,l,c,v'''
	def __init__(self, ticker):
		self.ticker = ticker.upper()
		self.minutes = 1 # 60 seconds
		self.ndays = 1
		self.df = None
		self.csv_fname = "data/%s.csv"%self.ticker.lower()
	
	def pull_data_to_csv(self):
		url = self.LINK%(self.ticker, self.minutes*60, self.ndays)
		csv = urllib.urlopen(url).readlines()
		df = pd.DataFrame(csv)
		df.to_csv(self.csv_fname)

	def read_csv(self):
		self.df = pd.read_csv(self.csv_fname)

if __name__=='__main__':
	import sys
	stock = gstock(sys.argv[1])
	stock.pull_data_to_csv()
	stock.read_csv()
	print stock.df.head()
	print stock.df.index
