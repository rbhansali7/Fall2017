ans = list()
outdegree = {}
indegree = {}

"""
def dfs(node, edgeDict, adjList, edgeCount, count):

    if edgeCount == count:
        return True

    if adjList[node]!=-1:
        for neighbor in adjList[node]:
            #print (neighbor)
            if edgeDict[(node, neighbor)] == False:
                edgeDict[(node, neighbor)]= True
                ans.append(neighbor)
                if dfs(neighbor,edgeDict,adjList, edgeCount, count+1):
                    return True
                del ans[-1]
                edgeDict[(node,neighbor)]=False

    return False
"""


def dfs(node, edgeDict, adjList, edgeCount, count):


    stack = list()

    while len(stack)>0 or len(adjList[node])>0:
        if len(adjList[node])<=0:
            ans.append(node)
            node = stack[-1]
            del stack[-1]
        else:
            stack.append(node)
            for neighbor in adjList[node]:
                adjList[node].remove(neighbor)
                node=neighbor
                break


if __name__ == "__main__":

    f=open("sample.txt","rU")

    adjList = {}
    edgeDict = {}
    nodeList = list()
    edgeCount = 0

    for line in f:
        s = line.split('->')
        node = s[0].strip()
        neighbors = s[1].strip('\n').strip().split(',')

        if node not in adjList:
            adjList[node]=neighbors

        edgeCount += len(neighbors)
        #Create edgeDict, indegree and outdegree count for each node
        nodeList.append(node)

        for neighbor in neighbors:

            nodeList.append(neighbor)

            if neighbor not in edgeDict.keys():
                edgeDict[(node, neighbor)]=False

            if neighbor not in indegree.keys():
                indegree[neighbor]=1
            else:
                indegree[neighbor]+=1

        if node not in outdegree.keys():
            outdegree[node]=len(neighbors)
        else:
            outdegree[node]+=len(neighbors)

    nodeSet = set(nodeList)

    for node in nodeSet:
        if node not in indegree.keys():
            indegree[node]=0
        if node not in outdegree.keys():
            outdegree[node]=0
        if node not in adjList.keys():
            adjList[node]=[]

    #print (adjList)
    #print (nodeSet)
    #print (len(nodeSet))
    #print (edgeCount)

    for node in outdegree.keys():
        if outdegree[node]-indegree[node]==1:
            startNode = node
            break
        #check if endNode is also needed
    #print (startNode)
    #dfs(startNode,edgeDict,adjList)

    #print (indegree)
    #print (outdegree)
    #print (edgeDict)
    #print (startNode)
        #print (node, neighbors)
    #print(edgeCount)
    if startNode:
        dfs(startNode, edgeDict, adjList, edgeCount, 0)
        ans.append(startNode)
        ans.reverse()


    print('->'.join(ans))
