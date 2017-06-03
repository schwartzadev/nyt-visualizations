#!/usr/bin/env python
import api
import words
import frequency

import requests
import time

'''
 * get a key at developer.nytimes.com
 * make a file named api.txt, place it in this same directory, and put your api key in the file, on the first line.
'''

def getNewest(num): # returns the most recent articles from the NYT api
	n = 1
	for i in range(0,int(num)): # num is the # of pages (groups of 10 articles)
		r = requests.get('http://api.nytimes.com/svc/search/v2/articlesearch.json?' + 
			'fl=source,snippet,headline,web_url,pub_date&' +
			'page=' + str(i) + '&' +
			'api-key=' + api.key)
		data = r.json()
		try:
			print(data['message'])
		except KeyError as e:
			for doc in data['response']['docs']:
				print('  ' + str(n) + '\t' + doc['snippet'])
				n += 1
		time.sleep(.9)

api.set() # gets key from file **cannot perform requests without this**
# words.graph('putin')
frequency.graph('google', 1998, 2016)
