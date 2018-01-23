import sys

class DNA:
	
	def __init__(self,nodes,dnas,dict,list):
		self.nodes=nodes
		self.dnas=dnas
		self.dict=dict
		self.list=list


	def getInput(self):
	
		count=0
		s=""
		f=open("rosalind_grph.txt","rU")
		
		for line in f:
			if line.startswith('>'):
				l=line.strip('\n')
				self.nodes.append(l.strip('>'))
				if count==0:
					count=1
				else:
					self.dnas.append(s)
					s=""	
			else:
				s+=line.strip('\n')
		if s:
			self.dnas.append(s)
			
		for i in range(0,len(self.nodes)):
			self.dict[self.dnas[i]]=self.nodes[i]
		
		#print '\n'.join(self.dnas)
	
	
	def findEdges(self):
		
		for i in range(0,len(self.dnas)):
			for j in range(i+1,len(self.dnas)):
				if self.findOverlap(self.dnas[i],self.dnas[j]):
					self.list.append(self.dict[self.dnas[i]]+" "+self.dict[self.dnas[j]])
				if self.findOverlap(self.dnas[j],self.dnas[i]):
					self.list.append(self.dict[self.dnas[j]]+" "+self.dict[self.dnas[i]])
		
		print '\n'.join(self.list)
		#print len(self.list)
		
	
	def findOverlap(self,str1,str2):
		
		#if len(str1)<=len(str2):
		#	minLength=len(str1)
		#else:
		#	minLength=len(str2)
		
		#for i in range(3,minLength):
		if str1.endswith(str2[0:3]):
			return True
		return False

def main():
	
	obj=DNA([],[],{},[])
	obj.getInput()
	obj.findEdges()
	
if __name__=="__main__":
	main()