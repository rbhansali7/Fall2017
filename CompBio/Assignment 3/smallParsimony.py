adjList = {}
indegree = {}
possibleVals = {}
selectedVals = {}


def assign(selected, possible):

    tempList = list()

    for i in range(len(selected)):
        if selected[i] in possible[i]:
            tempList.append(selected[i])
        else:
            s = list(possible[i])
            tempList.append(s[0])

    return tempList


def postOrder(root):

    #leaf case
    if len(adjList[root])==0:
        x=list(root)
        leafSet = list()
        for item in x:
            t = set()
            t.add(item)
            leafSet.append(t)
        return leafSet

    leftList=list()
    rightList=list()

    if adjList[root][0]:
        leftList = postOrder(adjList[root][0])
    if adjList[root][1]:
        rightList = postOrder(adjList[root][1])


    tempList = list()

    for i in range(len(leftList)):
        lset = leftList[i]
        rset = rightList[i]
        si=lset.intersection(rset)
        su=lset.union(rset)
        if si:
            tempList.append(si)
        else:
            tempList.append(su)

    if root not in possibleVals.keys():
        possibleVals[root] = tempList
    else:
        print("shouldn't happen")

    return tempList


def preOrder(root):

    #leaf
    if len(adjList[root])==0:
        if root not in selectedVals.keys():
            selectedVals[root]=list(root)
        return

    #actual root
    if indegree[root]==0:
        tempList = list()
        for i in range(len(possibleVals[root])):
            s= list(possibleVals[root][i])
            tempList.append(s[0])
        if root not in selectedVals.keys():
            selectedVals[root]=tempList

    leftList=list()
    rightList=list()

    leftChild = ""
    rightChild = ""

    if adjList[root][0]:
        leftChild = adjList[root][0]
    if adjList[root][1]:
        rightChild = adjList[root][1]


    for i in range(len(selectedVals[root])):
        if len(leftChild)>0 and leftChild in possibleVals.keys():
            leftList = assign(selectedVals[root],possibleVals[leftChild])
            if leftChild not in selectedVals.keys():
                selectedVals[leftChild]=leftList
        if len(rightChild)>0 and rightChild in possibleVals.keys():
            rightList = assign(selectedVals[root],possibleVals[rightChild])
            if rightChild not in selectedVals.keys():
                selectedVals[rightChild]=rightList

    if len(leftChild)>0:
        preOrder(leftChild)
    if len(rightChild)>0:
        preOrder(rightChild)


def hammingDist(s,t):
    c=0
    for i in range(len(s)):
        if s[i]!=t[i]:
            c+=1
    return c


def printAnswer():

    parsimonyCount = 0
    ansList=list()

    for node in adjList.keys():
        if len(adjList[node])>0:
            nodeStr = ''.join(selectedVals[node])
            if adjList[node][0]:
                lChildStr = ''.join(selectedVals[adjList[node][0]])
                ldist = hammingDist(selectedVals[node],selectedVals[adjList[node][0]])
                parsimonyCount+=ldist
                ansList.append(nodeStr+"->"+lChildStr+":"+str(ldist))
                ansList.append(lChildStr + "->" + nodeStr + ":" + str(ldist))
            if adjList[node][1]:
                rChildStr = ''.join(selectedVals[adjList[node][1]])
                rdist = hammingDist(selectedVals[node], selectedVals[adjList[node][1]])
                parsimonyCount+=rdist
                ansList.append(nodeStr + "->" + rChildStr + ":" + str(rdist))
                ansList.append(rChildStr + "->" + nodeStr + ":" + str(rdist))

    print (parsimonyCount)
    for item in ansList:
        print(item)




if __name__ =="__main__":

    f = open("sample.txt", "rU")

    firstLine = True
    nodeList = list()

    for line in f:
        if firstLine:
            leafCount = int(line)
            firstLine = False
        else:
            firstLine = False
            s = line.split('->')
            node = s[0]
            neighbor = s[1].strip('\n')

            nodeList.append(node)
            nodeList.append(neighbor)

            if node not in adjList:
                adjList[node]=[neighbor]
            else:
                adjList[node].append(neighbor)

            if neighbor not in indegree.keys():
                indegree[neighbor]=1
            else:
                indegree[neighbor]+=1

    nodeSet = set(nodeList)

    for node in nodeSet:
        if node not in indegree.keys():
            indegree[node]=0
            root = node
        if node not in adjList.keys():
            adjList[node]=[]
            #c=set(node)
            #print (c)

    #print (root)
    #print (indegree)
    #print (adjList)

    postOrder(root)
    #print (possibleVals)
    #print (root)
    preOrder(root)
    #print (selectedVals)
    printAnswer()

