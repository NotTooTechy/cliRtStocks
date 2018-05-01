import sys
import urllib2
import json
import time
from ast import literal_eval
from commands import getoutput
import datetime
from tmx_learn import stock




def hist(symb, ndays, _date, step=1):
	link_base = "https://web.tmxmoney.com/json/getPriceHistory.json.php?jsoncallback=?&qm_symbol=%s&date=DDD&webmasterId=101020"
	link = link_base%symb
	today = datetime.datetime.today()
	current_date=today
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
		i=-1*step
		print

if __name__ == "__main__":
	date = datetime.datetime.today().strftime('%Y/%m/%d')
	symbol=sys.argv[0]
	numdays=sys.argv[1]
  	try:
		step=sys.argv[2]
   	except:
    		step = 1
	print symbol, numdays
	hist(symbol, int(numdays), date, int(step))
