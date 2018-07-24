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
		self.csv_fname = "data_google/%s.csv"%self.ticker.lower()
	
	def pull_data_to_csv(self):
		url = self.LINK%(self.ticker, self.minutes*60, self.ndays)
		print url
		out = urllib.urlopen(url).read()
		f = open(self.csv_fname, 'w')
		f.write(out)
		f.close()
		df = pd.DataFrame(out)
		df.to_csv(self.csv_fname)
		return df

	def read_csv(self):
		self.df = pd.read_csv(self.csv_fname)

if __name__=='__main__':
	import sys
	stock = gstock(sys.argv[1])
	stock.pull_data_to_csv()
	stock.read_csv()
	print stock.df.head()
	print stock.df.index
	index_list = stock.df.index.tolist()
	for index, row in stock.df.iterrows():
		#print index, row.tolist()
		#print dir(row)
		if index > 7:
			rowlist = row.tolist()
			data = rowlist[1].split(",")
			print rowlist[0], data[1].strip(), data[5].strip()
			if index > 12:
				break
	 #df = pd.read_csv(fname, header=0, index_col='Date', parse_dates=True)
		
