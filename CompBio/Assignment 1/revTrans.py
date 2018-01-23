import sys

dict= {'A':4,'R':6,'N':2,'D':2,'C':2,'Q':2,'E':2,'G':4,'H':2,
'I':3,'L':6,'K':2,'M':1,'F':2,'P':4,'S':6,'T':4,'W':1,'Y':2,
'V':4
}

def revTranslate(ps):
	count=1
	for i in range(0,len(ps)):
		count=(count*dict[ps[i]])%1000000
	count=(count*3)%1000000
	return count


def main():
	
	protein=raw_input()
	print revTranslate(protein)
	
	
if __name__=="__main__":
	main()
