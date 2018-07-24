
kupljeno = [
	{
		"HOU.TO":[10.75, 10.67],
		"CVE.TO":[13.82,13.51],
		"JTR.V":[1.00, 0.99]
	},
	{
		"HOU.TO":[10.75, 10.73],
		"CVE.TO":[13.82,13.37],
		"JTR.V":[1.00, 0.98]
	},
	{
		"HOU.TO":[10.75, 10.62],
		"CVE.TO":[13.82,13.4],
		"JTR.V":[1.00, 0.91]
	}
]

for k in kupljeno:
	cap = 4000.0
	tot = 0.0
	captot = 0.0
	leftover=0
	for stck, prices in k.iteritems():
		nstock = (cap-10.0)/prices[0]
		leftover += cap - nstock*prices[0] -10
		tot += nstock*prices[1]
		captot += cap
	print "IN: %s, OUT: %s, diff: %s"%(captot, tot+leftover, leftover + tot-captot)
