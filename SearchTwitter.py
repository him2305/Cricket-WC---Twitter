#  SearchTwitter.py
#  
#  Copyright 2015[Himanshu Bansal, Natasha A. Thomas]
#  
#  This program is free software; you can redistribute it 
#  and/or modify it under the terms of the GNU General 
#  Public License as published by the Free Software 
#  Foundation; either  version 3 of the License, or 
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be 
#  useful,  but WITHOUT ANY WARRANTY; without  even the 
#  implied warranty of  MERCHANTABILITY or FITNESS FOR  
#  A PARTICULAR PURPOSE.  See the  GNU General Public 
#  License for more details.
#  
#  You should have received a copy of the GNU General 
#  Public License along with this program; if not,
#  write to the Free Software Foundation, Inc., 
#  51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
import sys
import multiprocessing
import tweepy
import couchdb
import jsonpickle
import json
import pdb
import threading
import time

class ClientDetails:
	
	def __init__(self, access_token, access_token_secret, consumer_key, consumer_secret, clientid):
		self.access_token = access_token
		self.access_token_secret = access_token_secret
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.clientid = clientid
		
	def OAuth(self):
		auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		auth.set_access_token(self.access_token, self.access_token_secret)
		client = tweepy.API(auth)
		return client

clients = []
clientDet1 = ClientDetails("2984460830-WCBUxmhV3pliyddNOTRK4gYNcHCdvUjRFGx6mVa", "dGh3xpZ86K4B41oyJdVVnCUWQHT7v2VupsvLiyUuNibHD", "AyNjHZkEuhM8wIzZOIpqrSa99", "0gJDee03DkAXM4O3HLDB3bmHt7xANY3IOyHtML6ipHq8G9TUlo", 1)
clientDet1.handle = clientDet1.OAuth()
clients.append(clientDet1)
clientDet2 = ClientDetails("2984423418-6gO70vPwWr7aFNCoVvaQGMUtuyORbkcfp2a8ZkP", "oa67l0mkhZ9BEr1z7tMoSRqkWcTc4Hz9oTELfxYdQn49K", "o1luqAm8P8HwMfMDAi0ZJbe59", "MyjgvHjW6TfF5Rwv6ooCDLykSbR5o8B24QVQKuXwz4DtBH5Y6G", 2)
clientDet2.handle = clientDet2.OAuth()
clients.append(clientDet2)
clientDet3 = ClientDetails("2984425194-4gAC2lovoxsivZt4TCtUsudquilUf75NSm9YwdH", "j1rQRZp95yX68XtzXR6pYXlgUYjhXtGyS3QF9CLKXAKGg", "Tnx0tjkahzSO0hfQVIZXMv6Ki", "IUXAdKi5qQ6jciDneelgbC4S2sE7DIkYBwr5E5HPOLyQJNKax6", 3)
clientDet3.handle = clientDet3.OAuth()
clients.append(clientDet3)
clientDet4 = ClientDetails("2984465426-m5i7t6WZ55vvvJCFcojjtFMAAtVOt2usGARp1pY", "OilzClAxBdQkI64Bov9TKJHtyvmxcYUfk4rwh9RpwcXOR", "Ulsn7ngH6w8NZUSsxMg9gJUGa", "EftOa1wRVFtv393Laqjm0CxfcpZl0n1hVTEJNnWLEFxFct8dAa", 4)
clientDet4.handle = clientDet4.OAuth()
clients.append(clientDet4)
clientDet5 = ClientDetails("2984488333-Yhxe3ORiHaV2oH2nn9auvTXh5kivXNOXKnBM6Mx", "5YEl6OhonaGdtoEBpf8nptHjSGZFqdjft3EWXLJytg5Qg", "JFDVZND8bkt7jn1RGULkuF5PA", "Sn6zH4u3j4NZocvXr5PEuHfK0bYoX7yxOBlBrj0bJJ7eQEisL7", 5)
clientDet5.handle = clientDet5.OAuth()
clients.append(clientDet5)
clientDet6 = ClientDetails("2984489719-ihgA3iJyR6uaORXahRPTqoeeTRLQywELPd8eOAF", "pwKXWZEvAsPrZmXArHt8VR7467hxDnQ3c6MY41KNQCMPT", "DsO7lSqWV8odC6A7yuz1tqdn7", "m2tXXMV8tjLhZHT9jqjMTyn1CxlFUUB2jtogflcj6nsMyEdVLW", 6)
clientDet6.handle = clientDet6.OAuth()
clients.append(clientDet6)



maxTweets = 1000000
tweetsPerQry = 100



def SearchProcess(location, db, hashtag):
	latitude = location[1]
	longitude = location[2]
	radius = location[3]
	
	t = threading.Thread(target = SearchThread, args = (hashtag, latitude, longitude, radius, )) 
	t.start()
	t.join()	


	
# Reference: http://www.karambelkar.info/2015/01/how-to-use-twitter-search-rest-api-most.html
def SearchThread(keyword, latitude, longitude, radius):
	searchQuery = keyword
	location = str(latitude) + ',' + str(longitude) + ',' + str(radius) + 'km'
	sinceId = None
	max_id = -1L
	tweetCount = 0
	for eachClient in clients:
		client = eachClient.handle
		try:
			g = client.rate_limit_status()
			remaining = g[u'resources'][u'search'][u'/search/tweets'][u'remaining']
		except Exception:
			remaining = 0
		if remaining > 0:
			print eachClient.clientid, " started"
			break
		
	while tweetCount < maxTweets:
		print "harvesting tweets"
		try:
			if max_id <= 0:
				if not sinceId:
					new_tweets = client.search(q=searchQuery, count=tweetsPerQry)
				else:
					new_tweets = client.search(q=searchQuery, count=tweetsPerQry, since_id=sinceId)
			else:
				if not sinceId:
					new_tweets = client.search(q=searchQuery, count=tweetsPerQry, max_id=str(max_id - 1))
				else:
					new_tweets = client.search(q=searchQuery, count=tweetsPerQry, max_id=str(max_id - 1), since_id=sinceId)
			if not new_tweets:
				print "No more tweets found"
				break
			for tweet in new_tweets:
				jsonString = jsonpickle.encode(tweet)
				jsonObj = json.loads(jsonString)
				tweetText = jsonObj['py/state']
				#print tweetText['text']
				StoreTweet(db, tweetText)
			tweetCount += len(new_tweets)
			print("Downloaded {0} tweets".format(tweetCount))
			max_id = new_tweets[-1].id
		except tweepy.TweepError as e:
			print("some error : " + str(e))
			print "Switching user"
			for eachClient in clients:
				client = eachClient.handle
				try:
					g = client.rate_limit_status()
					remaining = g[u'resources'][u'search'][u'/search/tweets'][u'remaining']
				except Exception:
					remaining = 0
				if remaining > 0:
					print eachClient.clientid, " started"
					break
			#c = client
			#client = SwitchUser(c)
			#break
            
				
def StoreTweet(db, tweet):
	if 'id' in tweet and 'text' in tweet:
				tweet['doc_type'] = "tweet"
				try:
					db.save(tweet)
					#print "tweet stored"
				except Exception:
					pass


def StartupDatabase():
	server = couchdb.Server()
	try:
		db = server.create('aus_vs_nz_final')
	except Exception:
		db = server['aus_vs_nz_final']
	return db



if __name__ == '__main__':
	db = StartupDatabase()
	threading.stack_size(32768)
	
	splitLocation = []
	with open("Location.txt") as fin:
		for location in fin:
			splitLocation.append(location.split())
			
	with open("hashtag.txt") as fin:
		hashtagList = []
		for tag in fin:
			newTag = tag[:-1]
			hashtagList.append(newTag)
		
	#hT = ['#SLvRSA', '#RSAvSL', '#RSAvsSL', '#SLvsRSA', '#SLvSA', '#SAvSL', '#SAvsSL', '#SLvsSA', '#ProteaFire', '#LionsRoar']	
	#hT = ['#BANGvIND', '#BANGvsIND', '#INDvBANG', '#INDvsBANG', '#RiseOfTheTigers', '#WontGiveItBack', '#INDIAvsBANG', '#INDIAvBANG', '#BANGvsINDIA', '#BANGLADESHvsINDIA', '#BANGLADESHvINDIA', '#INDIAvBANGLADESH', '#INDIAvsBANGLADESH']
	#hT = ['#GoGold', '#SupportPakistan', '#AUSvPAK', '#AUSvsPAK', '#PAKvAUS', '#PAKvsAUS', '#AUSTRALIAvPAKISTAN', '#AUSTRALIAvsPAKISTAN', '#PAKISTANvAUSTRALIA', '#PAKISTANvsAUSTRALIA', '#PAKvsAUSTRALIA', '#AUSvPAKISTAN', '#AUSvsPAKISTAN', '#OZvsPAK', '#PAKvOZ', '#PAKvsOZ']
	#hT = ['#NZvWI', '#NZvsWI', '#WIvNZ', '#WIvsNZ', '#BackTheBlackCaps', '#WindiesvsNZ', '#NZvWindies', '#NZvsWindies', '#MaroonFire', '#Windies', '#NZ']
	#hT = ['#NZvSA', '#NZvsSA', '#NZvRSA', '#NZvsRSA', '#SAvNZ', '#SAvsNZ', '#RSAvNZ', '#RSAvsNZ', '#ProteaFire', '#BackTheBlackCaps', '#SAvsKiwis', '#KiwisvsSA', '#cwc15semifinal']
	#hT = ['#cwc15']
	#hT = ['#AUSvIND', '#WontGiveItBack', '#GoGold', '#AUSvsIND', '#INDvAUS', '#INDvsAUS', '#INDIAvAUSTRALIA', '#INDIAvsAUSTRALIA', '#AUSTRALIAvINDIA', '#AUSTRALIAvsINDIA', '#AUSSIESvsINDIANS', '#OZvsIND', '#OZvIND', '#INDvsOZ']
	hT = ['#AUSvNZ', '#AUSvsNZ', '#NZvAUS', '#NZvsAUS', '#GoGold', '#BackTheBlackCaps', '#NewZealandvsAustralia', '#AustraliavNewZealand', '#AustraliavsNewZealand', '#AussiesvKiwis', '#AussiesvsKiwis', '#KiwisvsAussies', '#OzvNZ', '#OzvsNZ', '#NZvOz', '#NZvsOz', '#OzvsKiwis', '#KiwisvsOz', '#cwc15final', '#cwcfinal', '#worldcupfinal', '#cricketfinal', '#cricketworldcupfinal']
	for hashtag in hT:	
		processes = []
		for location in splitLocation:
			p = multiprocessing.Process(target = SearchProcess,args = (location, db, hashtag, ))
			p.start()	
			processes.append(p)
		for p in processes:
			p.join()
			
				
