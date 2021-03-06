#  GenerateArff.py
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
import csv
def writetoFile(string):
	#Making Training readable file for Weka
	fout = open("Original_Set.arff","a")
	#Making Dev readable file for Weka
	#fout = open("Dev_full_feature.arff","a")
	fout.writelines(string)
	if "NUMERIC" in string:
		fout.writelines("\n")

writetoFile("@RELATION Set-data\n");
		
#Read Feature file
try:
	featurefile = open("feature.txt","r")
except:
	print "File not found"
lst = []
tweet = {}
for feature in featurefile:
	string = "@attribute " + feature.replace(" ", "_") + " NUMERIC"
	writetoFile(string.replace("\n",""))
	lst.append(feature)

writetoFile("@attribute sentiment {P,Ne,Nu}\n")
writetoFile("\n@data\n")
		
#Read Tweet File 
try:
	#Get Training Data
	readTweets = csv.reader(open('getFeatureSet.csv', 'rb'), delimiter=',', quotechar='|')
	#Get Dev Data
	#readTweets = csv.reader(open('Dev_Tweets.csv', 'rb'), delimiter=',', quotechar='|')
	for readTweet in readTweets:
		sentiment = readTweet[0].lower()
		tweetText = readTweet[1].lower()
		for getFeature in lst:
			getFeature = getFeature.lower()
			getFeature = getFeature.replace("\n","")
			#chk = tweetText.find(getFeature)
			if not getFeature in tweetText:
				writetoFile("0,")
			else:
				writetoFile("1,")
		if sentiment == "positive":
			writetoFile("P\n")
		elif sentiment == "negative":
			writetoFile("Ne\n")
		else:
			writetoFile("Nu\n")
		#break
except:
	print "File not found"
	


	



