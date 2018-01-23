import sys

def countDNA(dna):
	
	a=c=g=t=0
	for i in range(0,len(dna)):
		if dna[i]=='A':
			a+=1
		if dna[i]=='C':
			c+=1
		if dna[i]=='G':
			g+=1
		if dna[i]=='T':
			t+=1
	
	print a,c,g,t


def main():
		
	countDNA(raw_input())
	
if __name__=="__main__":
	main()