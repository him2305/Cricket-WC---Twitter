#  CSVsentiment.py
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
import requests
import couchdb
import json 
import tweepy
import time
import sys
import csv
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
		client = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
		return client

# Multiple clients created for switching between clients when "rate limiting error" occurs on any client.
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


# read tweet id  
ipFile = open("tweetid.txt", "r")
c = csv.writer(open("locationdetails.csv", "wb"))
server = couchdb.Server()
# create couch database.
try:
	db = server.create('topsydata')
except Exception:
	db = server['topsydata']

try:
	for eachClient in clients:
		client = eachClient.handle
		try:
			g = client.rate_limit_status()
			remaining = g[u'resources'][u'statuses'][u'/statuses/show/:id'][u'remaining']
		except Exception:
			remaining = 0
		finally:	
			if remaining > 0:
				print eachClient.clientid, " started"
				break
	for line in ipFile:
		try:
			print "searching id"
			tweet = client.get_status(id=int(line))
			print "id found"
			successful = True
			# Saving missing attributes to database.
			if 'id' in tweet and 'text' in tweet:
				try:
					print "saving"
					entry = []
					del tweet['contributors']
					del tweet['coordinates']
					del tweet['entities']
					del tweet['extended_entities']
					del tweet['favorited']
					del tweet['geo']
					del tweet['id_str']
					del tweet['in_reply_to_screen_name']
					del tweet['in_reply_to_status_id']
					del tweet['in_reply_to_status_id_str']
					del tweet['in_reply_to_user_id']
					del tweet['in_reply_to_user_id_str']
					del tweet['lang']
					del tweet['place']
					del tweet['possibly_sensitive']
					del tweet['possibly_sensitive_appealable']
					del tweet['truncated']
					tweet['userid'] = tweet['user']['id']
					tweet['userlocation'] = tweet['user']['location']
					tweet['username'] = tweet['user']['screen_name']
					del tweet['user']
					entry.append(tweet['created_at'])
					entry.append(str(tweet['favorite_count']))
					entry.append(str(tweet['id']))
					entry.append(str(tweet['retweet_count']))
					entry.append(str(tweet['retweeted']))
					entry.append(tweet['source'])
					entry.append(tweet['text'])
					entry.append(str(tweet['userid']))
					entry.append(tweet['userlocation'])
					entry.append(tweet['username'])
					
					c.writerow(entry)
					#sys.exit()
					db[tweet['text']] = tweet
					tweetsStored = tweetsStored + 1
					print "tweet stored"
				except couchdb.http.ResourceConflict:
					print "already exists"
				except Exception:
					pass
		except tweepy.TweepError as e:
			# Switch to available client when rate limiting error occurs on the active client.
			if 'Rate limit exceeded' in str(e.message):
				print "Switching user"
				for eachClient in clients:
					client = eachClient.handle
					try:
						g = client.rate_limit_status()
						remaining = g[u'resources'][u'statuses'][u'/statuses/show/:id'][u'remaining']
					except Exception:
						remaining = 0
					finally:
						if remaining > 0:
							print eachClient.clientid, " started"
							break
									
			else:
				print "Some other error"
				successful = True
				pass
		except Exception as e:
			print str(e)
except Exception as e:
	print str(e)
