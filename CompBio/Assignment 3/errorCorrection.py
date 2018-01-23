readDict = {}
revReadDict = {}

def hammingDist(s,t):
    c=0
    for i in range(len(s)):
        if s[i]!=t[i]:
            c+=1
    return c


def revComplement(read):

    s = ""
    for j in range(len(read)):
        if read[j] == 'A':
            s += 'T'
        elif read[j] == 'T':
            s += 'A'
        elif read[j] == 'C':
            s += 'G'
        elif read[j] == 'G':
            s += 'C'
    t = s[::-1]

    return t

def findCorrection(s):

    for key in readDict.keys():
        if key!=s and readDict[key]>1 and hammingDist(key,s)==1:
            return s+"->"+key

    return ""


def correctedReads(reads):

    for read in reads:
        if read not in readDict.keys():
            readDict[read]=1
        else:
            readDict[read]+=1

        comp  = revComplement(read)

        if comp not in readDict.keys():
            readDict[comp]=1
        else:
            readDict[comp]+=1

    ans=[]
    for read in reads:
        if readDict[read]==1:
            corr = findCorrection(read)
            if corr!="":
                ans.append(corr)

    return ans






if __name__=="__main__":

    s = ""
    reads=list()
    f = open("sample.txt", "rU")
    for line in f:
        if line.startswith('>'):
            s=""
            continue
        else:
            s = line.strip('\n')
            reads.append(s)

    ansList = correctedReads(reads)

    for item in ansList:
        print (item)