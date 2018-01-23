import sys

def bwt(s):
    list=[]
    for i in range(len(s),0,-1):
        list.append(s[i:]+s[0:i])
    list.sort()

    bwtStr=""
    for items in list:
        bwtStr+=items[-1]

    print bwtStr


if __name__=="__main__":
    s=raw_input()
    bwt(s)
