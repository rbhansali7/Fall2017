import sys

class SCS:
	
	
	def __init__(self,dnas):
		self.dnas=dnas
		
		
	def getInput(self):
		flag=False
		s=""
		f=open("rosalind_long.txt","rU")
		for line in f:
			if line.startswith('>'):
				if not flag:
					flag=True
				else:
					self.dnas.append(s)
					s=""	
			else:
				s+=line.strip('\n')
		if s:
			self.dnas.append(s)
		#print self.dnas				

	
	def findOverlapCount(self,str1,str2):
		if len(str1)<=len(str2):
			minLength=len(str1)
		else:
			minLength=len(str2)
		
		curIndex=0
		found=False
		for i in range(1,minLength+1):
			if str1.endswith(str2[:i]):
				curIndex=i
				found=True
		
		if not found:
			return (0,"")
		else:
			return (curIndex,str1+str2[curIndex:])


	def findMaxOverlapPair(self,list):
		maxCount=0
		maxI=0
		maxJ=0
		count=0
		for i in range(0,len(list)):
			for j in range(i+1,len(list)):
				#print i,j
				(count,combStr)=self.findOverlapCount(list[i],list[j])
				#print count,combStr
				#print "count",count
				#print "maxCount",maxCount
				if count>maxCount:
					maxI=i
					maxJ=j
					maxCount=count
				(count,combStr2)=self.findOverlapCount(list[j],list[i])
				#print "count2",count
				#print "maxCount",maxCount
				#print count,combStr2
				if count>maxCount:
					maxI=j
					maxJ=i
					maxCount=count
				#print "max",maxI,maxJ
		
		#print maxI, maxJ
		(c,cstr)=self.findOverlapCount(list[maxI],list[maxJ])
		
		newList=[]
		for i in range(0,len(list)):
			if i==maxI or i==maxJ:
				continue
			else:
				newList.append(list[i])
		newList.append(cstr)
		
		return newList
		
	def generateSCS(self,list):
		length=len(list)
		for k in range(1,length):
			list=self.findMaxOverlapPair(list)
		print '\n'.join(list)

def main():
	
	obj=SCS([])
	obj.getInput()
	#(count,strs)=obj.findOverlapCount("DEFG","ABCDE")
	#print count,strs
	#list=["ABCDE","DEFG","GH"]
	#list=obj.findMaxOverlapPair(list)
	#print list
	obj.generateSCS(obj.dnas)


if __name__=="__main__":
	main()