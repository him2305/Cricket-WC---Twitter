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

import re,csv,pprint,nltk.classify
#from svmutil import *
from nltk.corpus import stopwords # Import the stop word list
from nltk.stem.snowball import SnowballStemmer # stemmer 
from nltk.stem import  WordNetLemmatizer

def removePunctuation(word):
	#replace two or more with two occurrences 
	pattern = re.compile(r"(.)\1{1,}", re.DOTALL) 
	word=pattern.sub(r"\1\1", word)
	#strip punctuation
	word = word.strip('\'"?,.')
	#check if it consists of only words
	val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", word)
	return val,word

def stem_lemmatize(word):
	stemmer = SnowballStemmer("english")
	
	
	match = re.compile("\\P{InBasic_Latin}")
	items = re.findall(match,word)
	for item in items:
		word = word.replace(item, "")
	word = word.replace("\\P{InBasic_Latin}", "")
	try:
		word = unicode ( word , 'utf-8')
	except:
		word = word.encode('ascii',errors='ignore')
	
	try:
		word = stemmer.stem(word)
	except:
		print word
	return word
	
def getFeatureVector(tweet, stopWords):
	
	#Unigrams
    featureVector = []
    featureVector1 = []
    featureVector2 = []
    words = tweet.split()
    for word in words:
        val,word = removePunctuation(word)
        
        #Stemming the features
        word = stem_lemmatize (word)
        if(word in stopWords or val is None):
            continue
        else:
            featureVector.append(word.lower())
    # Remove featureList duplicates
    #featureVector = set(featureVector)
    length = len(featureVector)
  
    #Bigrams
    for i in xrange(0,(length-1),2):
		word1 = featureVector[i]
		word2 = featureVector[i+1]
		word = word1+" "+word2
		featureVector1.append(word.lower())
		featureVector.append(word.lower())
    
    #Trigrams
    for i in xrange(0,(length-1),3):
		word1 = featureVector[i]
		word2 = featureVector[i+1]
		word3 = featureVector[i+2]
		word = word1+" "+word2+" "+word3
		#print word
		featureVector2.append(word.lower())
		featureVector.append(word.lower())
    
    #Unigrams with POS
    
    return {featureVector1,featureVector2}

def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features

inpTweets = csv.reader(open('getFeatureSet.csv', 'rb'), delimiter=',', quotechar='|')
stopWords = []
stopWords.append('AT_USER')
stopWords.append('URL')
fp = open('stopwords.txt')
line = fp.readline()
while line:
	word = line.strip()
	stopWords.append(word)
	line = fp.readline()
	
fp.close()
count = 0;
featureList = []
tweets = []
for row in inpTweets:
    sentiment = row[0]
    #print row[1]
    tweet = row[1]
    tweet = tweet.lower()
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    tweet = re.sub('@[^\s]+','AT_USER',tweet)    
    tweet = re.sub('[\s]+', ' ', tweet)
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #Stripping all the punctuations
    tweet = tweet.strip('\'":-)(;|@/$>}&^*#!?.,')
    #Removing all the unicode emoticons
    try:
    tmp = re.compile(u'['u'\U0001F300-\U0001F64F'u'\U0001F680-\U0001F6FF'u'\u2600-\u26FF\u2700-\u27BF]+',re.UNICODE)
    tweet = re.sub(tmp,'',tweet)
	except re.error:
		tmp = re.compile(u'['u'\ud83c[\udf00-\udfff]|'u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'u'[\u2600-\u26FF\u2700-\u27BF])+',re.UNICODE)
		tweet=tmp.sub(tmp,'',tweet)
    featureVector = getFeatureVector(tweet, stopWords)
    featureList.extend(featureVector)
    tweets.append((featureVector, sentiment))

# Remove featureList duplicates
featureList = list(set(featureList))
fp = open('feature_new.txt',"a")

#for feature in featureList:
fp.write("\n".join(featureList))
fp.close()
