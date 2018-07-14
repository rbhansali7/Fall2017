#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value alongside the marker positions
#Or return -1,[] if no solution exists for the given L

#Your backtracking function implementation

finalList = []
finalLen = 9999999999999999
finalListFC= []
finalLenFC = 9999999999999999


def noConflicts(value,mList):

    #check if this value has already been used
    for i in range(len(mList)):
        if mList[i]==value:
            return False


    #create a dictionary of the existing differences
    diffs=dict()
    for i in range(len(mList)):
        for j in range(i+1,len(mList)):
            d=abs(mList[i]-mList[j])
            if d not in diffs:
                diffs[d]=True
            else:
                print "incorrect values assigned previously"
                return False

    #check if assigning the current value satisfies the constraints or not
    for i in range(len(mList)):
        if abs(value-mList[i]) in diffs:
            return False
        else:
            diffs[abs(value-mList[i])]=True

    return True


def solveBT(L,M,count,mList,mLen):

    #invalid input checking
    if L+1<M or L<0 or M<=0:
        return False

    if count>=M:
        maxVal = max(mList)
        minVal = min(mList)
        global finalLen
        global finalList
        if abs(maxVal - minVal) < finalLen:
            finalLen = abs(maxVal - minVal)
            finalList = mList[:]
        return True

    for i in range(0,L+1):

        if(noConflicts(i, mList)):

            #add this assignment
            mList.append(i)

            #doubt solve problem recursively
            solveBT(L,M,count+1,mList,mLen)

            #remove this assignment and check with next value
            mList.pop()

    return False


def forwardChecking(L,M,val,mList,domain):

    #val has been assigned so it can't be used in the future

    #count <=m-1
    tmpdomain = dict()
    for i in range(L + 1):
        tmpdomain[i] = True

    tmpdomain[val]=False

    #numbers which will generate differences that can be generated using val and mList are no longer possible
    for i in range(len(mList)):
        diff=abs(val-mList[i])
        npVal=val+diff
        if npVal>=0 and npVal<=L:
            tmpdomain[npVal]=False

    count=0
    for i in range(L+1):
        if domain[i]==False or tmpdomain[i]==False:
            count+=1

    #no legal values left, return False
    if count==L+1:
        return False
    else:
        for i in range(L+1):
            if tmpdomain[i]==False:
                domain[i]=False
        return True



def solveBTwithFC(L,M,count,mList,mLen,domain):

    #invalid input checking
    if L+1 < M or L<0 or M<=0:
        return False

    if count>=M:
        maxVal = max(mList)
        minVal = min(mList)
        global finalLenFC
        global finalListFC
        if abs(maxVal - minVal) < finalLenFC:
            finalLenFC = abs(maxVal - minVal)
            finalListFC = mList[:]

    for i in range(0,L+1):
            if(noConflicts(i, mList)):

                #do forward checking
                if(count<M-1):
                    if not forwardChecking(L,M,i,mList,domain):
                        continue

                #add this assignment
                mList.append(i)
                domain[i]=False

                #doubt solve problem recursively
                solveBTwithFC(L,M,count+1,mList,mLen,domain)

                #remove this assignment and check with next value
                domain[i]=True
                mList.pop()

    return False



def BT(L, M):
    "*** YOUR CODE HERE ***"
    mList=[]
    mLen=L
    flag=solveBT(L,M,0,mList,mLen)
    if finalList:
        return finalLen,finalList
    return -1,[]

#Your backtracking+Forward checking function implementation
def FC(L, M):
    "*** YOUR CODE HERE ***"
    mList=[]
    mLen=L

    domain=dict()
    for i in range(L+1):
        domain[i]=True

    flag=solveBTwithFC(L,M,0,mList,mLen,domain)
    if finalListFC:
        return finalLenFC,finalListFC
    return -1,[]


#Bonus: backtracking + constraint propagation
def CP(L, M):
    "*** YOUR CODE HERE ***"
    return -1,[]


if __name__=="__main__":
    s=raw_input()
    list=s.split()
    L=int(list[0])
    M=int(list[1])
    print FC(L,M)


