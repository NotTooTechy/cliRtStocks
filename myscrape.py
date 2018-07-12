#!/usr/bin/env python
import urllib2
import json
from string import ascii_lowercase
from BeautifulSoup import BeautifulSoup

web = '''http://www.theupside.ca/list-tsx-stocks-market-capitalization/'''


def get_list_tsx_market_cap(link=web, add_to=1):
    soup = BeautifulSoup(urllib2.urlopen(link).read())
    links = []
    for row in soup('table', {'class': 'igsv-table'})[0].tbody('tr'):
        tds = row('td')
	ticker = tds[0].string
	if add_to == 1:
		if '.' in ticker:
			ticker = ticker.replace(".", "-")
		ticker = ticker + ".TO"
	links.append(ticker)
    return links

if __name__ == '__main__':
    print get_list_tsx_market_cap()


        


