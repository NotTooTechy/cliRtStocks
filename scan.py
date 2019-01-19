#!/usr/bin/env python
import sys
import urllib2
import json
import datetime
import time
import collections as clt
from stckscreener import oil
from commands import getoutput
print "\033[0;0m"
# 
link = "https://web.tmxmoney.com/json/getQuotesMini.json.php?jsoncallback=?&symbols=%s&webmasterId=101020"
_commodities = "https://web.tmxmoney.com/embed/commodities/embed.js.php?toolWidth=250&amp;locale=EN&amp;webmasterId=101020"
_history = "https://web.tmxmoney.com/json/getPriceHistory.json.php?jsoncallback=?&qm_symbol=%s&date=DDD&webmasterId=101020"


def hist(symb):
	today = datetime.datetime.today()
	date = today.strftime('%Y/%m/%d')
	link = _history.replace("DDD", date)
	content=urllib2.urlopen(link%symb).read()
  	try:
		content = content.strip()
		content = content.strip("?(")
		content = content.strip(");")
		content = json.loads(content)
	except:
		pass
	return content['history']['eoddata']

	
def woil():
	content=json.dumps(urllib2.urlopen(_commodities).read())
	x = json.loads(content)
	lista = x.split(";")
	return lista[31][43:][:5].strip(), lista[32][52:][1:5].strip() + "%"

def commodities(comm="oil", sleeptime=10):
	tmp='x'
	suma = 0
	val_arr = clt.deque(maxlen=20)
	maxval = 0
	minval = 9999
	for _ in range(17200):
		wtioil = oil()
        	wtioil.fetch_web()
		today = datetime.datetime.today()
        	ret =  wtioil.find_oil_div() 
		curr_price = float(ret[0])
		if ret[0] !=  tmp:
			val_arr.append(curr_price)
			suma = sum(val_arr)
			avg = suma/len(val_arr)
			if curr_price - avg < 0:
				trend = "DOWN"
			elif curr_price - avg ==0:
				trend = ""
			else:
				trend = "UP"
			print ret, today, " (%.2f, %.2f)"%(avg, curr_price - avg), trend,
			if curr_price > maxval:
				maxval = curr_price
				print "\tNEW_MAX =", maxval,
			if curr_price < minval:
				minval = curr_price
				print "\t\tNEW_MIN =", minval,
			print
			tmp = ret[0]
		
		#print oil()
		time.sleep(int(sleeptime))
		
	
def main(list_symb):
	print getoutput("date")
	symbols_list_str = ""
	for symb in list_symb:
			symbols_list_str+=symb 
			symbols_list_str+=','
	symbols_list_str=symbols_list_str.strip(',')
	print '-'*30
	content=(link%symbols_list_str)
	print content
	print '-'*30
	content=urllib2.urlopen(link%symbols_list_str).read()
	print '-'*30
	print content
	print '-'*30
	content = content.strip('?').strip(';').strip('(').strip(')')
	print '*'*30
	print content
	print '*'*30
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
		ret = hist(sys.argv[2])
		c = []
		for a, b in ret.iteritems():
			if 'unadj' not in a:
				print "\t%s"% a, 
				c.append(a)
		print
		for d in c:
			print "\t%s"%ret[d],
		print
	else:
		print data[list_symb[1]]
		main(data[list_symb[1]])
