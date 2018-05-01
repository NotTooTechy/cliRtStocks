#!/usr/bin/env python
import sys
import urllib2
import json
import datetime
import time
from commands import getoutput
print "\033[0;0m"

link = "https://web.tmxmoney.com/json/getQuotesMini.json.php?jsoncallback=?&symbols=%s&webmasterId=101020"
_commodities = "https://web.tmxmoney.com/embed/commodities/embed.js.php?toolWidth=250&amp;locale=EN&amp;webmasterId=101020"
_history = "https://web.tmxmoney.com/json/getPriceHistory.json.php?jsoncallback=?&qm_symbol=%s&date=DDD&webmasterId=101020"


def hist(symb):
	today = datetime.datetime.today()
	date = today.strftime('%Y/%m/%d')
	link = _history.replace("DDD", date)
	content=urllib2.urlopen(link%symb).read()
	content = content.strip()
	content = content.strip("?(")
	content = content.strip(");")
	content = json.loads(content)
	print content

	
def oil():
	content=json.dumps(urllib2.urlopen(_commodities).read())
	x = json.loads(content)
	lista = x.split(";")
	return lista[31][43:][:5].strip(), lista[32][52:][1:5].strip() + "%"

def commodities(comm="oil", sleeptime=10):
	for _ in range(7200):
		print oil()
		time.sleep(int(sleeptime)),
		
	
def main(list_symb):
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
	
if __name__ == "__main__":
	data = json.load(open('intresting_symbols.json'))
	list_symb = sys.argv
	if len(list_symb) < 2:
		print data.keys()
		print "<list> argument will show all lists"
	elif list_symb[1] =="list":
		for a, b in data.iteritems():
			print "%15s%100s"%(a, b)
	elif list_symb[1] =="comm":
		commodities(sleeptime=sys.argv[2])
	elif list_symb[1] =="astock":
		print hist(sys.argv[2])
	else:
		print data[list_symb[1]]
		main(data[list_symb[1]])
