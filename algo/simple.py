#!/usr/bin/env python

import mvg
import datetime
import sys
import json
from __init__ import START_DATE, END_DATE, chk_arg
import os



fprint = False
if 'debug' in sys.argv:
	fprint = True
fjson=None
if chk_arg("json") is not None:
	fjson = chk_arg("json")
SELL_THRESHOLD = 6
if chk_arg("sell_thresh") is not None:
	SELL_THRESHOLD = int(chk_arg("sell_thresh"))

if chk_arg("days") is not None:
	days = int(chk_arg("days"))
if chk_arg("ticker") is not None:
	stocks = [chk_arg("ticker")]
elif any("links" in s for s in sys.argv):
		with open("../links.json", 'r') as g:
			links = json.load(g)
		stocks = []
		for a, b in links.iteritems():
			tmp = a.lower()
			if "." in a:
				tmp=tmp.replace(".","-")
			tmp += ".to"
			stocks.append(tmp)
elif 'tsx' in sys.argv:
	with open("json/tsx_best.json", 'r') as g:
		data = json.load(g)
		stocks = data.keys()
elif chk_arg('load_from') is not None:
        load_from = chk_arg("load_from")
	with open(load_from, 'r') as g:
		data = json.load(g)
		stocks = data.keys()
                print stocks
else:
	stocks = ['hou.to', 'acb.to', 'bb.to', 'cpg.to', 'pd.to', 'obe.to', 'meg.to', 'bbd-b.to',
			'aapl', 'et.to', 'jtr.v', 'pyr.v', 'cve.to', 'gbtc', 'vff.to', 'dol.to', 'vle.to', 'th.to']
        t = "ZXB,ZXC,ZXD,ZAG,ZDV,ZWB,ZWU,ZDB,ZRE,ZUT,ZEL,ZLC,ZFL,ZPL,ZLB,ZCM,ZFM,ZMP,ZRR,ZCN,ZEB,ZIN,ZEO,ZPR,ZCS,ZFS,ZPS,ZST,BXF,FDV,FRF,AXF,LXF,CXF,OXF,FXF,MXF,CED,KXF,GXF,DXM,WXM,FXM,QXM,RWC,PXF,FDY,HAD,HFR,HPR,HXD,HXU,HIX,HED,HEU,HFD,HFU,HOG,HII,HBB,HEE,HEX,HEF,HEW,HXT,HXT.U,HXE,HXF,CBB,CBB.A,CBH,CLG,CBO,CLF,XCB,XTR,CRQ,XGB,XCG,XHB,XRB,XDV,XCV,XSB,XBB,CVD,XLB,XSH,XQB,XIC,XEI,XSQ,CEW,XFR,HUT,XEN,XMV,CMR,XIU,CDZ,CPD,XST,XEG,XFN,XIT,XMA,XRE,XUT,XMD,XCS,XVX,PFL,PSB,PDC,PPS,PXC,PZC,HUT.A,TLV,PGL,PSA,RBO,RCD,RCE,RQC,RQD,RQE,RQF,RQG,RQH,RQI,VAB,VSB,VSC,VCN,VCE,VRE,VDY,FDV.A,FRF.A,AXF.A,LXF.A,CXF.A,OXF.A,FXF.A,MXF.A,CED.A,KXF.A,GXF.A,DXM.A,WXM.A,FXM.A,QXM.A,RWC.A,PXF.A,FDY.A,FIE,HAD.A,HAL.A,FIE.A,HFR.A,HEE.A,HEX.A,HEF.A,CBH.A,CLG.A,CBO.A,CLF.A,HAA.A,CRQ.A,CVD.A,XQB.A,CEW.A,CMR.A,CDZ.A,CPD.A"
        t = t.split(",")
        stocks = []
        for i, loop in enumerate(t):
            if "." in loop:
                loop = loop.replace(".", "-")
                t[i] = loop
            stocks.append("%s.to"%loop)
        stockes = [ 'CCX', 'CGL', 'CGL-C', 'GAS', 'HBD', 'HBU', 'HND', 'HNU', 'HOD', 'HOU', 'HUC', 'HUG', 'HUN', 'HUZ', 'HZD', 'HZU', 'SBT', 'SBT-B', 'SBT.U', 'SVR', 'SVR-C' ]
	#stocks = ['et.to', 'sev.to', 'pyr.v', 'obe.to', 'bb.to', 'jtr.v', 'hwo.to']
#Estocks = ['bb.to']
#stocks = ['ge']
#BEGIN = datetime.datetime(2017, 7, 1)
BEGIN = START_DATE
END = END_DATE
#BEGIN = datetime.datetime(2018, 1, 1)
#END = datetime.datetime(2017, 11, 5)
#days = 14
total_initial = 0
total = 0
mvg_dict = {}
for ticker in stocks:
	window_dict= {}
	max_list = []
	max_window = -1.0
	max_profit = -9999.0
	max_capital = -9999.0
	stock = mvg.sma_return(ticker)
	stock.INITIAL_CAPITAL = 5000.0
	#stock.INITIAL_CAPITAL = 17000.0
	#now = datetime.datetime.now()
	stock.start = BEGIN
	stock.end = END
	#stock.end = END
	#stock.step_buy_th = 2
	stock.step_sell_th = SELL_THRESHOLD
	instrument = stock.get_data()
	if instrument is None:
		continue
	print "%-20s\t"%stock.ticker, stock.start.date(), "\t", stock.end.date(),"\t",
	for window in range(2, 160):
		stock.reset()
		stock.short_window = window
		try:
			stock.get_signals(instrument)
		except:
			print None
			break
		window_dict[window] = stock.profit
		if fprint:
			print window,"\t",
			print stock.INITIAL_CAPITAL, "\t",
			print stock.capital, "\t",
			print "%20.2f\t"%stock.profit
		if stock.profit > max_profit:
			max_window = window
			max_profit = stock.profit
		if stock.capital > max_capital:
			max_capital = stock.capital
	if fprint:
		print "-"*20
	print max_window, "\t", max_profit,
	max_list.append(max_window)
	print "\t", max_list
	total_initial += stock.INITIAL_CAPITAL
	total += max_capital
	mvg_dict[ticker]=[max_window, max_profit]
	#mvg_dict[ticker]=max_window

print 'In:', total_initial, 'Out:', total
if fjson is not None:
	with open(fjson, 'w') as f:
		json.dump(mvg_dict, f, sort_keys = True, indent = 4)
