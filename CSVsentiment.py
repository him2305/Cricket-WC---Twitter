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
import sys
import time
import csv
import re
import pdb

ipFile = open("kw.csv", "rb")
opFile = open("classified-keywords.csv", "a")
reader = csv.reader(ipFile)
writer = csv.writer(opFile)
startDay = 1
startMonth = 2
pos = 0
neg = 0
neut = 0
count = 0
for row in reader:
	print count
	count = count + 1
	#print row
	dateField = row[1].split()
	date = dateField[0]
	#time = dateField[2]
	print date
	date = date.split('-')
	month = int(date[1])
	day = int(date[2])
	if month == startMonth and day == startDay:
		print row[0]
		entry = []
		sentiment = raw_input('Enter sentiment: ')
		if sentiment == "Positive":
			pos = pos + 1
			if pos < 8:
				entry.append(sentiment)
				entry.append(row[0])
				entry.append(row[1])
				writer.writerow(entry)
		elif sentiment == "Negative":
			neg = neg + 1
			if neg < 8:
				entry.append(sentiment)
				entry.append(row[0])
				entry.append(row[1])
				writer.writerow(entry)
		elif sentiment == "skip":
			string = ""
			count = count - 1
			continue
		elif sentiment == "Neutral":
			neut = neut + 1
			if neut < 8:
				entry.append(sentiment)
				entry.append(row[0])
				entry.append(row[1])
				writer.writerow(entry)
		
	
	if pos >= 7:
		print "7 positive tweets"
	if neg >= 7:
		print "7 negative tweets"
	if neut >= 7:
		print "7 neutral tweets"
	if pos >= 7 and neg >= 7 and neut >= 7:
		#break
		startDay = startDay + 1
		if startMonth == 2 and startDay > 28:
			startMonth = 3
			startDay = 1
		#if startMonth == 3 and startDay > 6:
		#	break
		pos = 0
		neg = 0
		neut = 0
	
