import requests
import couchdb
import json 
import tweepy
import time
import sys
from datetime import datetime

'''class ClientDetails:
	
	def __init__(self, access_token, access_token_secret, consumer_key, consumer_secret, clientid):
		self.access_token = access_token
		self.access_token_secret = access_token_secret
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.clientid = clientid
		
	def OAuth(self):
		auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		auth.set_access_token(self.access_token, self.access_token_secret)
		client = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
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
clients.append(clientDet6)'''


#outputFile = open("OtterResults.txt", "a")
page = 1
api_key = "09C43A9B270A470B8EB8F2946A9369F3"
last_offset = 0
mintime = 1422805800
maxtime = 1422806400

#mintime = 1423465920
#maxtime = 1423468080


'''access_token = "2961294528-F0He0msmblxpAIqsC3c9v5ooJDFTfnPWC56hsS1"
access_token_secret = "tYY4J1oOCDHJw7RzVKa2o4hE6jsNl2nAiF836Z1Pjiul6"
consumer_key = "NNHpQgXBI3LfyBNUPXor2HgHu"
consumer_secret = "BUJ85s0LULXrmXebD2MKBSdjMbrHsJmEuyRTZvHWDI5UEYyw9J"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
client = tweepy.API(auth, parser=tweepy.parsers.JSONParser())'''


tweetsDownloaded = 0
tweetsStored = 0
server = couchdb.Server()
try:
	db = server.create('topsydata_datechanged')
except Exception:
	db = server['topsydata_datechanged']

try:
	'''for eachClient in clients:
		client = eachClient.handle
		try:
			g = client.rate_limit_status()
			remaining = g[u'resources'][u'statuses'][u'/statuses/show/:id'][u'remaining']
		except Exception:
			remaining = 0
		finally:	
			if remaining > 0:
				print eachClient.clientid, " started"
				break'''
	while True:
		print page
		try:
			r = requests.get("http://otter.topsy.com/search.json?q=%s&perpage=100&page=%s&mintime=%s&maxtime=%s&offset=%s&apikey=%s&allow_lang=en" % ("%23cwc15", page, mintime, maxtime, last_offset, api_key))
			#page = page + 1
			tweet = r.content
			data = json.loads(tweet)
			last_offset = data['response']['last_offset']
			for line in data['response']['list']:
				tweetsDownloaded = tweetsDownloaded + 1
				link = line['trackback_permalink']
				tweetId = link[-18:]
				print tweetId
				date = line['trackback_date']
				line['tweet_date'] = str(datetime.fromtimestamp(float(date)))
				#print line['tweet_date']
				try:
					print "saving"
					db[line['content']] = line
					tweetsStored = tweetsStored + 1
					print "tweet stored"
				except couchdb.http.ResourceConflict:
					print "already exists"
				except Exception as e:
					print str(e)
			page = page + 1
			if page == 11:
				page = 1
				mintime = maxtime
				maxtime = maxtime + 600
				if maxtime > 1426377600:
					print "time exceeded"
					sys.exit()
		except Exception as e:
			print str(e)
			print "Sleeping for 5 seconds"
			time.sleep(5)
			

except KeyboardInterrupt:
	print "Program terminated by user"

print maxtime	
print "tweets downloaded: ", tweetsDownloaded
print "tweets stored: ", tweetsStored
	

#("http://otter.topsy.com/search.json?q=%23cwc15&perpage=100&page=%s&window=d100&last_offset=%s&apikey=09C43A9B270A470B8EB8F2946A9369F3" % (page, last_offset)).read()
#http://api.topsy.com/v2/content/bulktweets.json?query=cwc15&apikey=09C43A9B270A470B8EB8F2946A9369F3&window=d100&limit=20000
