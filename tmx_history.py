import sys
import urllib2
import json
from ast import literal_eval
from commands import getoutput
import datetime
import time

today = datetime.datetime.today()
date = today.strftime('%Y/%m/%d')
link_base = "https://web.tmxmoney.com/json/getPriceHistory.json.php?jsoncallback=?&qm_symbol=%s&date=DDD&webmasterId=101020"
link = link_base.replace("DDD", date)

'''
https://web.tmxmoney.com/json/getPriceHistory.json.php?jsoncallback=?&qm_symbol=et&date=2017-10-05&webmasterId=101020
https://web.tmxmoney.com/json/getPriceHistory.json.php?jsoncallback=?&qm_symbol=et&date=2017/10/05&webmasterId=101020
Fri Oct  6 11:46:47 EDT 2017
unadjustedlow 2.18
unadjustedopen 2.18
changepercent 0.22831
unadjustedhigh 2.21
sharevolume 1,060,572
vwap 2.1928
high 2.21
low 2.18
unadjustedclose 2.195
unadjustedvwap 2.1928
@attributes {'date': '2017-10-06'}
close 2.195
triv N\/A
open 2.18
change 0.005

'''

list_symb = sys.argv
list_symb.pop(0)
print list_symb
keys = ['close', 'sharevolume', 'changepercent', 'change', 'unadjustedhigh', 'unadjustedopen', 'unadjustedlow']
print_keys = ['close', 'sharevolume', 'changepercent', 'change', 'unadjustedhigh', 'unadjustedopen', 'unadjustedlow']

print '%.12s'%'symbol'.ljust(12),
for loop in keys:
	tmp = str(loop)
	print '%.12s'%tmp.ljust(12),
print

tmp_vol = ""
for _ in range(7200):
	for symb in list_symb:
		content=urllib2.urlopen(link%symb).read()
		content = literal_eval(content)
		if content['history']['eoddata']["sharevolume"] != tmp_vol:
			print symb.ljust(12),
			for a in keys:
				print "%.12s"%content['history']['eoddata'][a].ljust(12),
			print
			tmp_vol = content['history']['eoddata']["sharevolume"]
		else:
			time.sleep(0.5)

