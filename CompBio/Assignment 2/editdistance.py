import sys

def cost(a,b):
    if a==b:
        return 0
    return 1

def editDistance(s,t):
    m=len(s)
    n=len(t)

    #construct 2D array
    dp=[]
    for i in range(m+1):
        tmp=[]
        for j in range(n+1):
            tmp.append(0)
        dp.append(tmp)

    #initialize base cases
    gap=1
    for i in range(m+1):
        dp[i][0]=i*gap
    for i in range(n+1):
        dp[0][i]=i*gap


    #calculate edit dist
    for i in range(1,m+1):
        for j in range(1,n+1):
            dp[i][j]=min(cost(s[i-1],t[j-1])+dp[i-1][j-1],gap+dp[i-1][j],gap+dp[i][j-1])

    #backtrack to create aligned strings
    a=""
    b=""
    i=m
    j=n
    while i>0 and j>0:
            minVal=min(cost(s[i-1],t[j-1])+dp[i-1][j-1],gap+dp[i-1][j],gap+dp[i][j-1])
            if minVal==gap+dp[i][j-1]:
                a+="-"
                b+=t[j-1]
                j=j-1
                continue
            elif minVal==gap+dp[i-1][j]:
                a+=s[i-1]
                b+="-"
                i=i-1
                continue
            elif minVal == dp[i - 1][j - 1] + cost(s[i-1], t[j-1]):
                a += s[i-1]
                b += t[j-1]
                i = i - 1
                j = j - 1
                continue

    a=a[::-1]
    b=b[::-1]

    print dp[m][n]
    print a
    print b


if __name__=="__main__":

    flag = False
    s = ""
    seq=[]
    f = open("samp.txt", "rU")
    for line in f:
        if line.startswith('>'):
            if s:
                seq.append(s)
                s = ""
        else:
            s += line.strip('\n')
    if s:
        seq.append(s)

    editDistance(seq[0],seq[1])
