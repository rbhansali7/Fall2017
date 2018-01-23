import sys
import math

class Random:
	
	def __init__(self,dna,probs,list):
		self.dna=dna
		self.probs=probs
		self.list=list

	def getInput(self):
		f=open("rosalind_prob.txt","rU")
		count=0
		for line in f:
			if count==0:
				self.dna=line.strip('\n')
				count+=1
			else:
				self.probs=line.split()
		
	def compute(self):
		
		ans=[]
		for prob in self.probs:
			atCount=gcCount=0
			atLog=gcLog=0
			for i in range(0,len(self.dna)):
				if self.dna[i]=='A' or self.dna[i]=='T':
					atCount+=1
				if self.dna[i]=='G' or self.dna[i]=='C':
					gcCount+=1
			p=float(prob)
			atLog=math.log10((1-p)/2)
			gcLog=math.log10(p/2)
			t=atCount*atLog+gcLog*gcCount
			ans.append("%.3f" %(atCount*atLog+gcLog*gcCount))
		print " ".join(ans)

def main():
	obj = Random("",[],[])
	obj.getInput()
	obj.compute()
	
if __name__=="__main__":
	main()