#!/usr/bin/env python

import sys
import json
from commands import getoutput as gout

kupljeno = {
        "HOU.TO":10.75,
        "CVE.TO":13.82,
        "JTR.V":1.00
}

def check_entry(cmd_arg):
	if any(cmd_arg in s for s in sys.argv):
			index = [i for i, s in enumerate(sys.argv) if cmd_arg in s][0]
			lines = sys.argv[index].split('=')[1]
			return lines
	return None


l = check_entry("lines")
if l is not None:
	lines = int(l)
else:
	lines = 15

fjson = check_entry("json")
if fjson is None:
	with open("json/best_avg.json", 'r') as f:
		data = json.load(f)
else:
	with open(fjson, 'r') as f:
		data = json.load(f)
	
'''
with open("tsx_best.json", 'r') as f:
	data = json.load(f)
'''

cmd = "python d5.py %s short=%s debug capital=5000| tail -n %d"
profits = []
for ticker, short in sorted(data.iteritems()):
        gout("rm data/%s.csv"%ticker)
	if type(short) is list:
		sshort = short[0]
	else:
		sshort = short
	print "-"*80
	out = gout(cmd%(ticker, sshort, lines))
	print out
	if 'profit:' in out:
		profits.append(out.split('profit:')[1].strip())

total = 0
for aprofit in profits:
	try:
		tmp = aprofit.replace(',', '')
	except:
		tmp = aprofit
	total += float(tmp)


print "Total profit:", total
	
