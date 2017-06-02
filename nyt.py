#!/usr/bin/env python

import requests
import time
from datetime import datetime
import numpy as np
import pylab as pl

'''
make a file named api.txt, place it in this same directory, and put your api key in the file, on the first line.
get a key at developer.nytimes.com
'''

def getNewest(num):
	n = 1
	for i in range(0,int(num)):
		r = requests.get('http://api.nytimes.com/svc/search/v2/articlesearch.json?' + 
			'fl=source,snippet,headline,web_url,pub_date&' +
			'page=' + str(i) + '&' +
			'api-key=' + apiKey)
		data = r.json()
		try:
			print(data['message'])
		except KeyError as e:
			for doc in data['response']['docs']:
				print('  ' + str(n) + '\t' + doc['snippet'])
				n += 1
		time.sleep(.9)

def setApiKey():
	with open('api.txt', 'r') as myfile:
		data = myfile.read()
		return data

def getFrequency(term, yr):
	data = {'api-key': apiKey,
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
		print(str(yr) + ': ' + str(d['response']['meta']['hits']) + ' hits')
		return d['response']['meta']['hits']

def graphFrequency(query, startYr, endYr):
	x = []
	y = []
	for i in range(startYr, endYr+1):
		y.append(getFrequency(query, i))
		x.append(i)
		time.sleep(.8) # prevents API limit, adjust as needed

	pl.xlabel('Year')
	pl.ylabel('Frequency of Query')
	prstr = 'NYT Headlines\' frequency of "%s"' % query
	pl.title(prstr)
	pl.grid(True)
	pl.plot(x, y, 'c*')
	coefs = np.polyfit(x, y, 6) # number of curves, will frequently return RankWanring
	y_poly = np.polyval(coefs, x)
	pl.plot(x, y_poly)
	name = 'nyt-img/%s--%d-%d.svg' % (query, startYr, endYr)
	print('saved to ' + name)
	pl.savefig(name, bbox_inches='tight')
	pl.show()

apiKey = setApiKey() # gets ket from file **cannot perform requests without this**
graphFrequency('climate change', 1980, 2016)