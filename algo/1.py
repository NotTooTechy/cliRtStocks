from commands import getoutput as ggout
import json

with open("sma.json", "r") as f:
	sma = json.load(f)

profit = 0
inv = 0
for a, b in sma.iteritems():
	if b is not None:
		output = ggout("python b5.py %s short=%s"%(a, b))
		res = output.split("\t")
		print res
		profit += float(res[2].strip("profit:"))
		inv+=float(res[1].split(" ")[0])

print 'Inestment:', inv, ' Current', inv+profit, 'profit(%s)'%profit