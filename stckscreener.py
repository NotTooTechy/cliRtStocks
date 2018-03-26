import urllib2
import json
from string import ascii_lowercase
from BeautifulSoup import BeautifulSoup

#start_web="http://www.tmxmoney.com/TMX/HttpController?GetPage=ListedCompanyDirectory&Page=1&SearchIsMarket=Yes&Market=T&Language=en&SearchCriteria=Name&SearchType=Contain&SearchKeyword=a&SUBMIT=Search"
start_web="http://www.tmxmoney.com/TMX/HttpController?GetPage=ListedCompanyDirectory&Page=1&SearchIsMarket=Yes&Market=T&Language=en&SearchCriteria=Name&SearchType=StartWith&SearchKeyword=a&SUBMIT=Search"
baseweb="http://www.tmxmoney.com/TMX/HttpController?"
getpage="GetPage=ListedCompanyDirectory&Page=%s"
search="&SearchIsMarket=Yes&Market=T&Language=en&SearchCriteria=Name&SearchType=StartWith&SearchKeyword=%s&SUBMIT=Search"

def link_search_start_char(acharacter, pg=1):
    webb = baseweb + getpage%str(pg) + search%acharacter
    return webb

def num_of_pages(web):
    soup = BeautifulSoup(urllib2.urlopen(web).read())
    table=soup.find('table')
    td=table('td')
    page_text=td[1].string
    return int(page_text.split('of')[1])

def collect_stocks_from_one_starting_letter():
    webb=link_search_start_char('a')
    total_pages=num_of_pages(webb)
    all_links={}
    for char in ascii_lowercase:
        for i in range(total_pages):
            dynamic_web=link_search_start_char(char, str(i+1))
            links=collect_all_stck(dynamic_web)
            #all_links = links.copy()
            all_links.update(links)
    return all_links
        
    

def collect_all_stck(web):
    soup = BeautifulSoup(urllib2.urlopen(web).read())
    links = {}
    for row in soup('table', {'class': 'tablemaster'})[0].tbody('tr'):
        tds = row('td')
        a = row('a')
        try:
        	symbol = a[1].string.strip()
        	full_name = a[0].string.strip()
        	link= a[0]['href']
        	#print '%s\t\t%s\t\t%s'%(symbol, full_name, link)
        	links[symbol]=link
        except:
        	pass
    return links

class stck_screener:
    def __init__(self, share):
        #self.tags="quotes,charts,news,company,finances,price_history,options,research,dividents"
        self.baseweb="http://web.tmxmoney.com/%s.php?qm_symbol=%s"
        self.quote_web=self.baseweb%('quote', share)
        self.charts_web=self.baseweb%('charts', share)
        self.news_web=self.baseweb%('news', share)
        self.company_web=self.baseweb%('company', share)
        self.finances_web=self.baseweb%('finances', share)
        self.price_history_web=self.baseweb%('price_history', share)
        self.options_web=self.baseweb%('options', share)
        self.research_web=self.baseweb%('research', share)
        self.divident_web=self.baseweb%('dividents', share)

    def fetch_web(self):
        self.soup = BeautifulSoup(urllib2.urlopen(self.quote_web).read())

    def ticker(self):
        self.div = self.soup('div', {'class' : 'quote-ticker tickerLarge'})
        return self.div[0].string

    def name(self):
        self.div = self.soup('div', {'class' : 'quote-name'})
        self.name=self.div[0]('h2')
        return self.name[0].string

    def price_quote(self):
       # self.soup = BeautifulSoup(urllib2.urlopen(self.quote_web).read())
        self.div = self.soup('div', {'class' : 'quote-price priceLarge'})
        self.quote_price=self.div[0]('span')
        self.current_price=self.quote_price[0].string
        return self.current_price
    
    def price_change(self):
        #self.div = self.soup('div', {'class' : 'quote-change changeLarge change-up'})
        self.div = self.soup('div', {'class' : 'quote-price priceLarge'})
        self.change= self.div[0].nextSibling
        self.change=self.change.nextSibling
        self.change=self.change('span', {'class':"quote-small-text"})[0]
        self.nextchange=self.change.next
        self.nextchange=self.nextchange.next
        self.change_list=self.nextchange.next.strip().split()
        self.change_amount=self.change_list[0]
        self.change_perc=self.change_list[1].strip('()')
        return self.change_amount,self.change_perc

    def volume(self):
        self.div = self.soup('div', {'class' : "quote-volume volumeLarge"})
        self.volume=self.div[0]('span', {'class':"quote-small-text"})[0]
        #self.nextchange=self.volume.next
        #self.nextchange=self.nextchange.next
        self.volume=self.volume.next.next.next
        return self.volume.strip()

    def daylow_high(self):
        self.div = self.soup('div', {'class' : 'day-low'})
        self.daylow=self.div[0].next.next.next.next
        self.div = self.soup('div', {'class' : 'day-high'})
        self.high=self.div[0].next.next.next.next
        return self.daylow.strip(), self.high.strip()

    def weeklow_high(self):
        self.div = self.soup('div', {'class' : 'week-low'})
        self.weeklow=self.div[0].next.next.next.next.next
        self.div = self.soup('div', {'class' : 'week-high'})
        self.weekhigh=self.div[0].next.next.next.next.next
        return self.weeklow.strip(),self.weekhigh.strip()
    

    def nexto(self):
        self.div = self.soup('div', {'class' : 'quote-row'})
        self.nexx= self.div[0].nextSibling
       # print self.nexx.next,
        print self.nexx.next.next

def google_fin(list_of_stocks):
    ''' http://www.google.com/finance/info?q=NSE:et,bgm,..
    '''
    base="http://www.google.com/finance/info?q=NSE:"
    url=base
    for stck in list_of_stocks:
        url+=stck + ','
    url=url.strip(',')
  #  soup = BeautifulSoup(urllib2.urlopen(full_weblist).read())
    response = urllib2.urlopen(url)
    html = response.read()
    html.strip('/')
    html=html[4:]
    import ast
    x = ast.literal_eval(html)
    #print x
    for loop in x:
        print loop['t'], '\t', loop['l_cur'], '\t', loop['cp']
   # html=html.strip('\/\/')
   # data=json.loads(html)
   # print data

        
class investing:
    def __init__(self):
        self.curdeoil='http://www.investing.com/commodities/crude-oil'

    def fetch_crude(self):
        self.req= urllib2.Request(self.curdeoil, headers={'User-Agent' : "Magic Browser"}) 
        self.soup = BeautifulSoup(urllib2.urlopen(self.req).read())
        #self.soup = BeautifulSoup(urllib2.urlopen(self.curdeoil).read())

    def lastprice(self):
        self.div = self.soup('span', {'class' : 'arial_16 midNum pid-8849-last'})
        return self.div[0].string




def main(symbols):
    '''
    link_dict=collect_stocks_from_one_starting_letter()
    with open('links.json', 'w') as fp:
        json.dump(link_dict, fp, sort_keys = True, indent=4)
    print len(link_dict.keys())
    print len(link_dict)
    '''
    import time
    startt=time.time()
    with open('links.json') as data_file:
        data = json.load(data_file)
    #print data
    #print data
   # symbols=['cxv', 'pyr', 'lsg', 'phm', 'mfc', 'sev', 'SMU.UN', 'tnt.un', 'iip.un']
   # symbols=['cxv', 'pyr', 'sev', 'mfc', 'lsg', 'bgm', 'abr']
    liso=[]
    for symbol in symbols:
        stck=stck_screener(symbol) 
        stck.fetch_web()
        print '%8s'%stck.ticker(),
        #print stck.quote_web
        print '%10s'%stck.price_quote(),
        print '%10s'%stck.price_change()[1],
        print '%10s'%stck.volume(),
        print '%8s%8s'%stck.daylow_high(),
        print '%8s%8s'%stck.weeklow_high(),
        print '\t',stck.name()


    

if __name__ == '__main__':
    import sys
    if len(sys.argv) <2:
        sybls=['tsx', 'acb', 'pd', 'cpg', 'obe', 'bb', 'plc', 'sev', 'et', 'pyr', 'tnt.un', 'msft:us']
        #sybls=['cxv', 'pyr', 'et']
        main(sybls)
    elif sys.argv[1] == 'gold':
        sybls=['mto', 'txg', 'bgm', 'abr', 'hou', 'hcg']
        main(sybls)
    elif sys.argv[1] == 'oil':
	inv=investing()
        inv.fetch_crude()
        print '%8s'%inv.lastprice(),
    else:
        sybls=['tnt.un', 'iip.un', 'srv.un', 'mfc']
        main(sybls)



        


