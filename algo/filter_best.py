import json
import time
from copy import deepcopy as cp
from __init__ import chk_arg


fname = "tsx_scan.json"
fname = "tsx_from_2018_1_11.json"
fname=None
if chk_arg("json") is not None:
        fname= chk_arg("json")

with open(fname, 'r') as f:
	data = json.load(f)

top = {}
loops =0
for a, b in data.iteritems():
  loops+=1
  tmp_top = {}
  ticker = a
  avg = b[0]
  profit = b[1]
  lentop = len(top.keys())
  if lentop < 20:
     top[ticker] = round(profit)
  else:
    tmp_top = cp(top)
    for c, d in top.iteritems():
      if d < profit:
        del tmp_top[c]
        tmp_top[a] = [avg, round(profit)]
        break
    top = cp(tmp_top)
    
#print top

for a, b in top.iteritems():
  print a, data[a]
        
        
with open('filtered_%s'%fname, 'w') as f:
	json.dump(top, f, indent=4) 
