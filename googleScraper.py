# Get the first link from a Google search result

import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys  

# Changed default string encoding from 'ascii' to 'utf8'
reload(sys)  
sys.setdefaultencoding('utf8') 

# Read input list file
f = 'PNC_Real_Estate_Match.csv'
df = pd.read_csv(f, skiprows=None)
df = df.dropna(how='all')
df = df.head(50)

# These domains are frequently incorrect
skipDomains = ['www.sec.gov', 'wwww.bloomberg.com', 'whalewisdom.com', 'www.hoovers.com', \
	'www.manta.com', 'www.yellowpages.com', 'www.buzzfile.com']

#--------------------------------------------------------------------------------

class Analysis:
	def __init__(self, term):

		# Search Term
		self.term = term
		self.url = 'https://www.google.com/search?q={0}'.format(self.term)

	# Get the first domain in google search result
	def run(self):
		response = requests.get(self.url)
		soup = BeautifulSoup(response.text, 'html.parser')

		aTags = soup.find_all('a')

		c = 0

		#print domains
		for text in aTags:
			if text.has_attr('href'):
				#print text.attrs['href']
				if ('/url?q' in text.attrs['href']) & (c < 1):

					c += 1
					domain = text.attrs['href']
					domain = domain.split('=')
					domain = domain[1]
					domain = domain.split('/')
					domain = domain[2]
					
		return domain

#-------------------------------------------------------------------------------

def getFirstDomain(name):

	# Got utf-8 codec error before adding this
	name = unicode(name, errors='replace')

	if '.' in name:
		name = name.replace('.', '')

	if ',' in name:
		name = name.replace(',', '')

	# Run a search
	a = Analysis(name)
	return a.run()

#-------------------------------------------------------------------------------

def getDomains(name):

	df['Domain'] = name.apply(getFirstDomain)
	return df

#---------------------------------------------------------------------------------

df = getDomains(df['Account Name'])
print df['Domain']


