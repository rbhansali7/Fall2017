#LPS from geeksforgeeks as its a standard algorithm
#http://www.geeksforgeeks.org/searching-for-patterns-set-2-kmp-algorithm/
def LPSArray(pat):

    M = len(pat)
    lps = [0] * M
    j = 0
    lens = 0  # length of the previous longest prefix suffix

    lps[0] = 0 # lps[0] is always 0
    i = 1

    # the loop calculates lps[i] for i = 1 to M-1
    while i < M:
        if pat[i] == pat[lens]:
            lens += 1
            lps[i] = lens
            i += 1
        else:
            if lens != 0:
                lens = lps[lens - 1]
            else:
                lps[i] = 0
                i += 1

    maxlen=lps[0]
    for i in range(M):
        if lps[i]>maxlen:
            maxlen=lps[i]

    return maxlen

def generateKmers(kmer):
    l=list()
    k=len(kmer)
    l.append(kmer[0:k-1])
    l.append(kmer[1:])
    return l

def isNotPossible(ans, startMer, nextMer):
    s=startMer+nextMer[-1]
    tans=ans+ans
    if s in tans:
        return False
    else:
        return True

def genomeAssembly(kmers,k):

    graph = {}
    kmerDict = {}


    for kmer in kmers:
        smallMers = generateKmers(kmer)
        leftMer = smallMers[0]
        rightMer = smallMers[1]

        if leftMer not in kmerDict:
            kmerDict[leftMer]=False
        if rightMer not in kmerDict:
            kmerDict[rightMer]=False

        #checkThis
        if leftMer not in graph:
            graph[leftMer]=rightMer

    #print (kmerDict)
    #print (graph)

    kmerCount = len(kmerDict)
    ans=""

    for key in graph.keys():
        startMer = key
        ans+=startMer
        nextMer = graph[startMer]
        break

    #print (ans)
    while kmerDict[startMer] is not True:
        ans+=nextMer[-1]
        #print (startMer, nextMer, nextMer[-1])
        kmerDict[startMer]=True
        startMer = nextMer
        nextMer = graph[nextMer]

    x = LPSArray(ans)


    return ans[x:]




if __name__=="__main__":

    f=open("sample.txt","rU")
    kmers = list()
    for line in f:
        kmers.append(line.strip('\n'))
    #print (kmers)

    print (genomeAssembly(kmers,len(kmers[0])))
