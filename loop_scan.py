import sys
import urllib2
import json
import time
from commands import getoutput
print "\033[0;0m"

link = "https://web.tmxmoney.com/json/getQuotesMini.json.php?jsoncallback=?&symbols=%s&webmasterId=101020"
'''
https://web.tmxmoney.com/json/getPriceHistory.json.php?jsoncallback=?&qm_symbol=et&date=2017-10-05&webmasterId=101020
https://web.tmxmoney.com/json/getPriceHistory.json.php?jsoncallback=?&qm_symbol=et&date=2017/10/05&webmasterId=101020
'''

list_symb = sys.argv
list_symb.pop(0)
print list_symb
print getoutput("date")
symbols_list_str = ""
for symb in list_symb:
		symbols_list_str+=symb 
		symbols_list_str+=','
symbols_list_str=symbols_list_str.strip(',')
content=urllib2.urlopen(link%symbols_list_str).read()
content = content.strip('?').strip(';').strip('(').strip(')')
x = json.loads(content)


quotes = {}
tab_quotes = {}
tab = 29
for quote in x['results']['quote']:
	print "%s\t%s\t"%(quote['symbolstring'], quote['last']), quote['lasttradedatetime'].split('T')
	quotes[quote['symbolstring']] =  quote['lasttradedatetime'].split('T')
	tab_quotes[quote['symbolstring']] = tab
	tab+=1
print
print quotes
print '*'*100
for _ in range(7200):
	content=urllib2.urlopen(link%symbols_list_str).read()
	content = content.strip('?').strip(';').strip('(').strip(')')
	x = json.loads(content)
	for quote in x['results']['quote']:
		if quotes[quote['symbolstring']] !=  quote['lasttradedatetime'].split('T'):
			#print "\e[48;5;18m%%03d",#%(tab_quotes[quote['symbolstring']]),
			print "\033[1;%d;%dm"%(tab_quotes[quote['symbolstring']], 80),
			print "%s\t%s\t"%(quote['symbolstring'], quote['last']), quote['lasttradedatetime'].split('T'),
			print "\033[0;0m"
			quotes[quote['symbolstring']] =  quote['lasttradedatetime'].split('T')
	time.sleep(0.2)
