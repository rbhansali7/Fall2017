import sys

dp = []
ways=[]

def cost(a,b):
    if a==b:
        return 200
    return -99999999

def gap():
    return -1


def countWays(i,j,s,t):

    m=len(s)
    n=len(t)

    for i in range(1,m+1):
        for j in range(1,n+1):
            maxVal = max(cost(s[i - 1], t[j - 1]) + dp[i - 1][j - 1], gap() + dp[i - 1][j], gap() + dp[i][j - 1])

            if maxVal == cost(s[i - 1], t[j - 1]) + dp[i - 1][j - 1]:
                ways[i][j]=max(ways[i][j],ways[i-1][j-1])

            if maxVal == gap() + dp[i - 1][j]:
                ways[i][j]=max(ways[i][j],ways[i-1][j]+1)

            if maxVal == gap() + dp[i][j - 1]:
                ways[i][j]=max(ways[i][j],ways[i][j-1]+1)

    return ways[m][n]


def editDistance(s,t):
    m=len(s)
    n=len(t)

    #construct 2D array
    for i in range(m+1):
        tmp=[]
        for j in range(n+1):
            tmp.append(0)
        dp.append(tmp)

    #initialize base cases
    for i in range(m+1):
        dp[i][0]=i*gap()
    for i in range(n+1):
        dp[0][i]=i*gap()

     #initializing ways array
    for i in range(m+1):
        tmp=[]
        for j in range(n+1):
            tmp.append(0)
        ways.append(tmp)

    for i in range(m+1):
        ways[i][0]=i
    for i in range(n+1):
        ways[0][i]=i



    #calculate edit dist
    for i in range(1,m+1):
        for j in range(1,n+1):
            dp[i][j]=max(cost(s[i-1],t[j-1])+dp[i-1][j-1],gap()+dp[i-1][j],gap()+dp[i][j-1])

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