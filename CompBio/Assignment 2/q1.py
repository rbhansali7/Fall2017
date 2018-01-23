import sys

def rabbitDP():

    dp=list()
    dp.append(1)
    dp.append(1)

    for i in range(2,n):
        if(i<m):
            dp.append(dp[i-1]+dp[i-2])
        elif i==m:
            dp.append(dp[i-1] + dp[i-2]-1)
        else:
            dp.append(dp[i-1]+dp[i-2]-dp[i-m-1])

    return dp[n-1]


def main():
    ans=rabbitDP()
    print ans


if __name__=="__main__":
    s = raw_input()
    t=s.split()
    n=int(t[0])
    m=int(t[1])
    main()
