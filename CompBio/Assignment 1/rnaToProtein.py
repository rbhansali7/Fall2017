import sys

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
	
def translate(rna):
	s=""
	for i in range(0,len(rna)):
		if rna[i]=='U':
			s+='T'
		else:
			s+=rna[i]
		
	protein=""
	i=0
	while i+2<len(s):
		protein+=dict[s[i:i+3]]
		i+=3
	return protein
	
	
def main():
	f=open("rosalind_prot.txt","rU")
	rna=""
	for line in f:
		rna+=line
	print translate(rna)
	
if __name__=="__main__":
	main()