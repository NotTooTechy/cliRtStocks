import sys
import urllib2
import json
import time
from ast import literal_eval
from commands import getoutput
import datetime
from tmx_learn import stock




def main(symb, ndays, _date):


	link_base = "https://web.tmxmoney.com/json/getPriceHistory.json.php?jsoncallback=?&qm_symbol=%s&date=DDD&webmasterId=101020"
	#link = link_base.replace("DDD", _date)
	link = link_base%symb
	today = datetime.datetime.today()
	current_date=today
	#share = stock(symb)
	print
	i=0
	for loop in range(ndays):
		current_date = current_date + datetime.timedelta(i)
		date = current_date.strftime('%Y/%m/%d')
		link = link_base.replace("DDD", date)
		try:
			share = stock(symb, link)
			print loop,
			print date,
			share.print_attr()
		except:
			pass
		i=-1
		print

#share.print_attr()
if __name__ == "__main__":
	date = datetime.datetime.today().strftime('%Y/%m/%d')
	symbol=sys.argv[0]
	numdays=sys.argv[1]
	print symbol, numdays
	main(symbol, int(numdays), date)
