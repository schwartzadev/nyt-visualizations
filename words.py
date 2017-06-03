import api
import numpy as np
import pylab as pl
from collections import Counter
import requests
import time

def articlesToString(term, pg):
	wordList = ''
	data = {'api-key': api.key,
	'fq' : 'headline:(\"' + term + '\")',
	'fl' : 'headline,snippet,pub_date,lead_paragraph',
	'page' : pg}
	r = requests.get('http://api.nytimes.com/svc/search/v2/articlesearch.json', params=data)
	d = r.json()
	try:
		print(d['message']) # if api limit exceeded
	except KeyError as e:
		for doc in d['response']['docs']:
			wordList += ' '
			wordList += doc['headline']['main']
			wordList += ' '
			wordList += doc['lead_paragraph']
	return wordList

def graph(term): # bar graph of word frequency in a given query
	x = []
	y = []
	for num in range(1,6):
		print('pg #' + str(num))
		wList = articlesToString(term, num)
		wList += ' '
		time.sleep(.6)
	blacklist = ['the', 'says', 'said', 'with', 'that', 'and', 'for', 'his', 'her', 'had', 'was']
	wList = wList.lower().replace(':', '').replace(',', '')
	wList = Counter(wList.split()).most_common()
	for item in wList:
		if (item[0] in blacklist) or len(item[0]) < 3 or item[1] < 3:
			pass
		else:
			print(item)
			x.append(item[0].title().replace("'S", "'s"))
			y.append(item[1])

	y_pos = np.arange(len(x))
	pl.bar(y_pos, y, align='center', alpha=0.5)
	pl.xticks(y_pos, x, rotation = 315)
	pl.ylabel('Frequency')
	pl.title('NYT Word Frequency in query "' + term + '"')
	pl.show()