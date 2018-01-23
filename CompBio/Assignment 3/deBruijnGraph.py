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


def dbG(kmers):

    tmp = list()
    adjList = list()
    k=len(kmers[0])

    for kmer in kmers:
        tmp.append(kmer)
        tmp.append(revComplement(kmer))

    s = set(tmp)

    for item in s:
        t = "("+item[0:k-1]+", "+item[1:]+")"
        adjList.append(t)

    return adjList



if __name__=="__main__":
    kmers=list()
    f=open("sample.txt","rU")
    for line in f:
        tmp = line.strip('\n')
        kmers.append(tmp)

    items=dbG(kmers)
    for item in items:
        print (item)