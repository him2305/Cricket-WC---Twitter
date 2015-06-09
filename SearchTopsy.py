#  SearchTopsy.py
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
from datetime import datetime

page = 1
api_key = "09C43A9B270A470B8EB8F2946A9369F3"
last_offset = 0
# Setting min and max time to fetch tweets from topsy.
mintime = 1422805800
maxtime = 1422806400

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
			
			# Downloading tweets from topsy on the basis of min and max time. 
			
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
