import sys
import urllib2
import json
import time
from ast import literal_eval
from commands import getoutput
import datetime

_date = datetime.datetime.today().strftime('%Y/%m/%d')


link = "https://web.tmxmoney.com/json/getPriceHistory.json.php?jsoncallback=?&qm_symbol=%s&date=DDD&webmasterId=101020"
link = link.replace("DDD", _date)
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
SLEEP=0
list_symb = sys.argv
list_symb.pop(0)
print list_symb
print getoutput("date")
keys = '''unadjustedhigh sharevolume changepercent high unadjustedask unadjustedvwap close triv open vwap low @attributes unadjustedbidsize unadjustedopen bid unadjustedasksize unadjustedclose ask change asksize unadjustedlow unadjustedbid bidsiz'''
keys = '''unadjustedclose sharevolume change changepercent high open low'''
keys = keys.split(" ")
print "%.12s"%"..........".ljust(12),
print '%.12s'%'symbol'.ljust(12),
for loop in keys:
	tmp = str(loop)
	print '%.12s'%tmp.ljust(12),
print

class stock:
		def __init__(self, symb, link=link):
			self.symb = symb
			self.content = urllib2.urlopen(link%symb).read()
			self.content = literal_eval(self.content)
			self.content = self.content['history']['eoddata']
			
			self.current = self.content['unadjustedclose']
			self.volume = self.content['sharevolume']
			self.change = self.content['change']
			self.change_percentage = self.content['changepercent']
			self.high = self.content['high']
			self.open = self.content['open']
			self.low = self.content['low']
		
		def test_open(self):
			if self.current > self.open:
				return True
			return False
		
		def test_high(self):
			if self.current >= self.high:
				return True
			return False
		
		def test_low(self):
			if self.current <= self.low:
				return True
			return False
		
		def print_attr(self, spacer=12):
			print self.symb.ljust(spacer),
			print "%.12s"%self.current.ljust(spacer),
			print "%.12s"%self.volume.ljust(spacer),
			print "%.12s"%self.change.ljust(spacer),
			print "%.12s"%self.change_percentage.ljust(spacer),
			print "%.12s"%self.high.ljust(spacer),
			print "%.12s"%self.open.ljust(spacer),
			print "%.12s"%self.low.ljust(spacer),
			if self.test_open():
				print '>Open',
			else:
				print '<Open',
			if self.test_high():
				print 'DHigh',
			else:
				print ' ',
			if self.test_low():
				print 'DLow',
			else:
				print ' ',
																 
if __name__ == '__main__':
	tmp_current=-100
	tmp_volume=-100
	tmp_open=-100
	tmp_high=-100
	tmp_low=-100
	tracker = {}
	uptick=0
	downtick=0
	values = []
	uptick_avg ={'nticks':5, 'collected_values' : []}
	collect_upticks =[]
	for i in range(1):
		for symb in list_symb:
			stime = time.time()
			share = stock(symb)
			share.print_attr()
			print time.time() - stime
			if share.volume > tmp_volume:
				if share.current > tmp_current:
					uptick +=1
				elif share.current == tmp_current:
					pass
				else:
					downtick+=1
			values.append(float(share.current))
			curr_avg = sum(values)/len(values)
			tmp_current = share.current
			tmp_volume = share.volume
		time.sleep(SLEEP)
	'''
			
	print "uptick", uptick
	print "downtick", downtick
	print 'avg', curr_avg
	'''	

