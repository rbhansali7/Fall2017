import sys

countArray=[0,0,0,0]
tally=[[],[],[],[]]

def symbolVal(symbol):
    if symbol=='A':
        return 0
    if symbol=='C':
        return 1
    if symbol=='G':
        return 2
    if symbol=='T':
        return 3

def findFirstLast(k,top,bottom,symbol,s):
    #finding first occ:
    if s[top] == symbol and tally[k][top] == tally[k][bottom]:
        return top,top

    for i in range(top,bottom+1):
        if s[i]==symbol:
            firstIndex=i
            break

    for i in range(bottom,top-1,-1):
        if s[i]==symbol:
            lastIndex=i
            break

    return firstIndex,lastIndex




def precalculate(s):

    for i in range(len(s)):
        if s[i]=='A':
            countArray[0]+=1
        if s[i]=='C':
            countArray[1]+=1
        if s[i]=='G':
            countArray[2]+=1
        if s[i]=='T':
            countArray[3]+=1


        flag=False
        for i in range (0,len(s)):
            if s[i]=='A':
                if not flag:
                    tally[0].append(1)
                    tally[1].append(0)
                    tally[2].append(0)
                    tally[3].append(0)
                    flag=True
                else:
                    tally[0].append(tally[0][i-1]+1)
                    tally[1].append(tally[1][i-1])
                    tally[2].append(tally[2][i-1])
                    tally[3].append(tally[3][i-1])
            if s[i]=='C':
                if not flag:
                    tally[0].append(0)
                    tally[1].append(1)
                    tally[2].append(0)
                    tally[3].append(0)
                    flag=True
                else:
                    tally[0].append(tally[0][i-1])
                    tally[1].append(tally[1][i-1]+1)
                    tally[2].append(tally[2][i-1])
                    tally[3].append(tally[3][i-1])
            if s[i]=='G':
                if not flag:
                    tally[0].append(0)
                    tally[1].append(0)
                    tally[2].append(1)
                    tally[3].append(0)
                    flag=True
                else:
                    tally[0].append(tally[0][i-1])
                    tally[1].append(tally[1][i-1])
                    tally[2].append(tally[2][i-1]+1)
                    tally[3].append(tally[3][i-1])
            if s[i]=='T':
                if not flag:
                    tally[0].append(0)
                    tally[1].append(0)
                    tally[2].append(0)
                    tally[3].append(1)
                    flag=True
                else:
                    tally[0].append(tally[0][i-1])
                    tally[1].append(tally[1][i-1])
                    tally[2].append(tally[2][i-1])
                    tally[3].append(tally[3][i-1]+1)
            if s[i]=='$':
                if not flag:
                    tally[0].append(0)
                    tally[1].append(0)
                    tally[2].append(0)
                    tally[3].append(0)
                    flag=True
                else:
                    tally[0].append(tally[0][i-1])
                    tally[1].append(tally[1][i-1])
                    tally[2].append(tally[2][i-1])
                    tally[3].append(tally[3][i-1])





def lastToFirst(s,index):

    #count = 0
    #for i in range(0,index+1):
    #    if s[i]==s[index]:
    #        count+=1

    if s[index]=='$':
        return 0

    if s[index]=='A':
        return tally[0][index]
        #return count

    if s[index]=='C':
        return 1 + countArray[0] + tally[1][index] - 1
        #return 1+countArray[0]+count-1

    if s[index]=='G':
        return 1 + countArray[0] + countArray[1] + tally[2][index] - 1
        #return 1+countArray[0]+countArray[1]+count-1

    if s[index]=='T':
        return 1 + countArray[0] + countArray[1] + countArray[2] + tally[3][index] - 1
        #return 1+countArray[0]+countArray[1]+countArray[2]+count-1


def bwmatching(s,pattern):
    lastcol=s
    firstcol=''.join(sorted(s))

    top=0
    bottom=len(lastcol)-1

    while top<=bottom:
        if pattern:
            symbol=pattern[-1]
            pattern=pattern[:-1]

            k=symbolVal(symbol)
            if lastcol[top]!=symbol and tally[k][top]==tally[k][bottom]:
                return 0
            else:
                topIndex, bottomIndex =findFirstLast(k,top,bottom,symbol,s)
                top=lastToFirst(s,topIndex)
                bottom=lastToFirst(s,bottomIndex)
        else:
            return bottom-top+1





if __name__=="__main__":

    s=raw_input()
    tmp=raw_input()
    patterns=tmp.split()

    precalculate(s)
    l=[]
    for pattern in patterns:
        l.append(str(bwmatching(s,pattern)))

    print " ".join(l)