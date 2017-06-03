import api

import requests
import time
import pylab as pl
import numpy as np


def get(term, yr):
	data = {'api-key': api.key,
	'fq' : 'headline:(\"' + term + '\")',
	'fl' : 'headline,snippet,pub_date',
  	'begin_date' : str(yr) + '0101',
  	'end_date' : str(yr) + '1231',
  	'sort' : 'oldest'}
	r = requests.get('http://api.nytimes.com/svc/search/v2/articlesearch.json', params=data)
	d = r.json()
	try:
		print(d['message'])
		return None
	except Exception as e:
		'''for doc in d['response']['docs']:
			print(doc['headline']['main'])
		# this prints each of the articles in the given year'''
		print(str(yr) + ': ' + str(d['response']['meta']['hits']) + ' hits')
		return d['response']['meta']['hits']

def graph(query, startYr, endYr):
	x = []
	y = []
	for i in range(startYr, endYr+1):
		y.append(get(query, i))
		x.append(i)
		time.sleep(.8) # prevents API limit, adjust as needed
	pl.xlabel('Year')
	pl.ylabel('Frequency of Query')
	prstr = 'NYT Headlines\' frequency of "%s"' % query
	pl.title(prstr)
	pl.grid(True)
	pl.plot(x, y, 'b*')
	coefs = np.polyfit(x, y, 10) # number of curves, will frequently return RankWanring
	y_poly = np.polyval(coefs, x)
	pl.plot(x, y_poly)
	name = 'nyt-img/%s--%d-%d.svg' % (query, startYr, endYr)
	print('saved to ' + name)
	pl.savefig(name, bbox_inches='tight')
	pl.show()