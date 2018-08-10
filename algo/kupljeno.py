
kupljeno = [
#	{ "HOU.TO":[10.75, 11.13], "CVE.TO":[13.45,13.55], "JTR.V":[1.00, 0.95] },
	{ "HOU.TO":[10.75, 10.67], "CVE.TO":[13.82,13.51], "JTR.V":[1.00, 0.99] },
	{ "HOU.TO":[10.75, 10.73], "CVE.TO":[13.82,13.37], "JTR.V":[1.00, 0.98] },
	{ "HOU.TO":[10.75, 10.62], "CVE.TO":[13.82,13.4], "JTR.V":[1.00, 0.91] },
	{ "HOU.TO":[10.75, 10.83], "CVE.TO":[13.82,13.45], "JTR.V":[1.00, 0.94] },
	{ "HOU.TO":[10.75, 11.11], "CVE.TO":[13.82,13.54], "JTR.V":[1.00, 0.95] },
	{ "HOU.TO":[10.75, 11.19], "CVE.TO":[13.82,13.39], "JTR.V":[1.00, 0.94] },
	{ "HOU.TO":[10.75, 10.94], "CVE.TO":[13.82,12.97], "JTR.V":[1.00, 0.94] },
	{ "HOU.TO":[10.75, 11.29], "CVE.TO":[13.82,13.13], "JTR.V":[1.00, 0.91] },
	{ "HOU.TO":[10.75, 10.89], "CVE.TO":[13.82,13.05], "JTR.V":[1.00, 0.94] },
	{ "HOU.TO":[10.75, 10.58], "CVE.TO":[13.82,13.03], "JTR.V":[1.00, 0.92] },
	{ "HOU.TO":[10.75, 10.98], "CVE.TO":[13.82,13.11], "JTR.V":[1.00, 0.95] },
	{ "HOU.TO":[10.75, 10.84], "CVE.TO":[13.82,13.15], "JTR.V":[1.00, 0.94] },
	{ "HOU.TO":[10.75, 10.97], "CVE.TO":[13.82,13.07], "JTR.V":[1.00, 0.91] },
	{ "HOU.TO":[10.75, 10.27], "CVE.TO":[13.82,12.77], "JTR.V":[1.00, 0.90] },
	{ "HOU.TO":[10.75, 10.24], "CVE.TO":[13.82,12.92], "JTR.V":[1.00, 0.90] },
	{ "HOU.TO":[10.75, 10.55], "CVE.TO":[13.82,12.75], "JTR.V":[1.00, 0.87] },
]

kupljeno2 = [
	{ "BB.TO":[12.91, 13.06], "BBD-B.TO":[4.84, 5.11], "MEG.TO":[8.99, 8.47] },
	{ "BB.TO":[12.91, 12.86], "BBD-B.TO":[4.84, 4.96], "MEG.TO":[8.99, 8.24] },
	{ "BB.TO":[12.91, 13.42], "BBD-B.TO":[4.84, 4.76], "MEG.TO":[8.99, 8.72] },
	{ "BB.TO":[12.91, 13.66], "BBD-B.TO":[4.84, 4.73], "MEG.TO":[8.99, 8.04] },
	{ "BB.TO":[12.91, 13.48], "BBD-B.TO":[4.84, 4.66], "MEG.TO":[8.99, 7.77] },
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
print
for k in kupljeno2:
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
