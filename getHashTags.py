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

splitLine=[]
j=3	
hashTag = []
with open("Matches.txt") as fin:
	for line in fin:
		splitLine.append(line.split())

#print splitLine
matchCount = 1	
condition = "\n"

for i in range(0,len(splitLine)) :
	try:
		flag=0
		matchNo = int(splitLine[i][0])
		country1 = splitLine[i][j].split(",")
		country2 = splitLine[i][j+1].split(",")
		print country1,"::",country2
		#break
		if flag==0:
			filename = country1[0]+"v"+country2[0]+".csv"
			flag+=1
			print filename
			#print "\n"
		fout = open(filename,"w")
		#print filename
		for k in range(0,len(country1)) :
			for l in range(0,len(country2)) :
				print len(country1)
				print len(country2)
				#break
				#if matchCount == matchNo:
				hashTag='#'+country1[k]+'v'+country2[l]+condition+'#'+country1[k]+'vs'+country2[l]+condition+'#'+country2[l]+'v'+country1[k]+condition+'#'+country2[l]+'vs'+country1[k]+condition
				print hashTag
				#print filename
				fout.writelines(hashTag)
				#else:
				#	#hashTag.append('\n')
				#	matchCount=matchCount + 1
	except:
		continue
	fout.close()



       
       
