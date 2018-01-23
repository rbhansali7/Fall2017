import sys

dp = []
gap = 1
MOD=134217727
ways=[]


def cost(a,b):
    if a==b:
        return 0
    return 1


def countWays(i,j,s,t):

    if i==0 or j==0:
        return 1

    if ways[i][j]!=-1:
        return ways[i][j]

    minVal = min(cost(s[i-1], t[j-1]) + dp[i - 1][j - 1], gap + dp[i - 1][j], gap + dp[i][j - 1])
    ans=0
    if minVal==cost(s[i-1], t[j-1]) + dp[i - 1][j - 1]:
        ans=(ans+countWays(i-1,j-1,s,t))%MOD
    if minVal==gap + dp[i - 1][j]:
        ans = (ans+countWays(i - 1, j , s, t))%MOD
    if minVal==gap + dp[i][j - 1]:
        ans = (ans+countWays(i , j - 1, s, t))%MOD

    ways[i][j]=ans

    return ans


def editDistance(s,t):
    m=len(s)
    n=len(t)

    #construct 2D array
    for i in range(m+1):
        tmp=[]
        for j in range(n+1):
            tmp.append(0)
        dp.append(tmp)

    for i in range(m+1):
        tmp=[]
        for j in range(n+1):
            tmp.append(-1)
        ways.append(tmp)

    for i in range(m+1):
        ways[i][0]=1
    for i in range(n+1):
        ways[0][i]=1


    #initialize base cases
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

    #print dp[m][n]
    print countWays(m,n,s,t)

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
