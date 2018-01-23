import sys

def lastToFirst(s,index):

    count = 0
    for i in range(0,index+1):
        if s[i]==s[index]:
            count+=1

    countArray=[0,0,0,0]
    for i in range(len(s)):
        if s[i]=='A':
            countArray[0]+=1
        if s[i]=='C':
            countArray[1]+=1
        if s[i]=='G':
            countArray[2]+=1
        if s[i]=='T':
            countArray[3]+=1

    if s[index]=='$':
        print 0

    if s[index]=='A':
        print count

    if s[index]=='C':
        print 1+countArray[0]+count-1


    if s[index]=='G':
        print 1+countArray[0]+countArray[1]+count-1

    if s[index]=='T':
        print 1+countArray[0]+countArray[1]+countArray[2]+count-1





if __name__=="__main__":
    s=raw_input()
    ind=raw_input()
    index=int(ind)
    lastToFirst(s,index)
