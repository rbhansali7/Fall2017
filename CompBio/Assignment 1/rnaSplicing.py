import sys
import re

class RNASplicer:
	
	dict={'ATG':'','TAA':'','TGA':'','TAG':'','GCT':'A','GCC':'A','GCA':'A',
	'GCG':'A','CGT':'R','CGC':'R','CGA':'R','CGG':'R','AGA':'R','AGG':'R',
	'AAT':'N','AAC':'N','GAT':'D','GAC':'D','TGT':'C','TGC':'C','CAA':'Q',
	'CAG':'Q','GAA':'E','GAG':'E','GGT':'G','GGC':'G','GGA':'G','GGG':'G',
	'CAT':'H','CAC':'H','ATT':'I','ATC':'I','ATA':'I','TTA':'L','TTG':'L',
	'CTT':'L','CTC':'L','CTA':'L','CTG':'L','AAA':'K','AAG':'K','ATG':'M',
	'TTT':'F','TTC':'F','CCT':'P','CCC':'P','CCA':'P','CCG':'P','TCT':'S',
	'TCC':'S','TCA':'S','TCG':'S','AGT':'S','AGC':'S','ACT':'T','ACC':'T',
	'ACA':'T','ACG':'T','TGG':'W','TAT':'Y','TAC':'Y','GTT':'V','GTC':'V',
	'GTA':'V','GTG':'V'
	}


	def __init__(self,rna,introns):
		self.rna=""
		self.introns=[]


	def getInput(self):
	
		count=0
		f=open("rosalind_splc.txt","rU")
		
		for line in f:
			if line.startswith('>'):
				count+=1
				continue
			else:
				if count<=1:
					self.rna+=line.strip('\n')
				else:
					self.introns.append(line.strip('\n'))		


	def rnaSplicing(self):
	
		s=[self.rna]
		i=0
		for intron in self.introns:
			s.append(self.splicer(s[i],intron))
			i+=1

		return self.translate(s[-1])
	

	def splicer(self,rna,intron):
	
		s=""
		j=0
		list = []
		for match in re.finditer(intron,rna):
			list.append(match.start())
		for index in list:
			s+=rna[j:index]
			j=index+len(intron)
		s+=rna[j:]
		return s


	def translate(self, mRNA):
		protein=""
		i=0
		while i+2<len(mRNA):
			protein+=self.dict[mRNA[i:i+3]]
			i+=3
		return protein


def main():
	
	obj = RNASplicer("",[])
	obj.getInput()
	print obj.rnaSplicing()
	
	
	
if __name__=="__main__":
	main()
	