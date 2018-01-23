
tally=[[],[],[],[],[]]
counts = [0, 0, 0, 0, 0]
firstOcc = []

def symbolVal(symbol):
    if symbol=='$':
        return 0
    if symbol=='A':
        return 1
    if symbol=='C':
        return 2
    if symbol=='G':
        return 3
    if symbol=='T':
        return 4

def preCalculate(s):

    for i in range(len(s)):
        if s[i] == 'A':
            counts[1] += 1
        if s[i] == 'C':
            counts[2] += 1
        if s[i] == 'G':
            counts[3] += 1
        if s[i] == 'T':
            counts[4] += 1

    firstOcc.append(0)
    count=0
    for i in range(1,5):
        firstOcc.append(count+1)
        count+=counts[i]

    flag=False
    for i in range (len(s)):
        if s[i]=='A':
            if not flag:
                tally[0].append(0)
                tally[1].append(1)
                tally[2].append(0)
                tally[3].append(0)
                tally[4].append(0)
                flag=True
            else:
                tally[0].append(tally[0][i-1])
                tally[1].append(tally[1][i-1]+1)
                tally[2].append(tally[2][i-1])
                tally[3].append(tally[3][i-1])
                tally[4].append(tally[4][i-1])
        if s[i]=='C':
            if not flag:
                tally[0].append(0)
                tally[1].append(0)
                tally[2].append(1)
                tally[3].append(0)
                tally[4].append(0)
                flag=True
            else:
                tally[0].append(tally[0][i-1])
                tally[1].append(tally[1][i-1])
                tally[2].append(tally[2][i-1]+1)
                tally[3].append(tally[3][i-1])
                tally[4].append(tally[4][i-1])
        if s[i]=='G':
            if not flag:
                tally[0].append(0)
                tally[1].append(0)
                tally[2].append(0)
                tally[3].append(1)
                tally[4].append(0)
                flag=True
            else:
                tally[0].append(tally[0][i-1])
                tally[1].append(tally[1][i-1])
                tally[2].append(tally[2][i-1])
                tally[3].append(tally[3][i-1]+1)
                tally[4].append(tally[4][i-1])
        if s[i]=='T':
            if not flag:
                tally[0].append(0)
                tally[1].append(0)
                tally[2].append(0)
                tally[3].append(0)
                tally[4].append(1)
                flag=True
            else:
                tally[0].append(tally[0][i-1])
                tally[1].append(tally[1][i-1])
                tally[2].append(tally[2][i-1])
                tally[3].append(tally[3][i-1])
                tally[4].append(tally[4][i-1]+1)
        if s[i]=='$':
            if not flag:
                tally[0].append(1)
                tally[1].append(0)
                tally[2].append(0)
                tally[3].append(0)
                tally[4].append(0)
                flag=True
            else:
                tally[0].append(tally[0][i-1]+1)
                tally[1].append(tally[1][i-1])
                tally[2].append(tally[2][i-1])
                tally[3].append(tally[3][i-1])
                tally[4].append(tally[4][i-1])


def bwmatching(s,pattern):

    top=1
    bottom=len(s)-1
    while top<=bottom:
        if pattern:
            symbol=pattern[-1]
            pattern=pattern[:-1]
            k=symbolVal(symbol)
            if s[top]==symbol or tally[k][top]<tally[k][bottom]:
                top=firstOcc[k]+tally[k][top-1]
                bottom=firstOcc[k]+tally[k][bottom]-1
            else:
                return 0
        else:
            return bottom-top+1

if __name__=="__main__":

    s=raw_input()
    tmp=raw_input()
    patterns=tmp.split()
    preCalculate(s)
    l=[]
    for pattern in patterns:
        l.append(str(bwmatching(s,pattern)))

    print " ".join(l)




