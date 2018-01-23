import random
import pickle as pkl
import argparse
import csv
import numpy as np
import pandas as pd
from scipy.stats import chisquare
import sys

sys.setrecursionlimit(10000)

'''
TreeNode represents a node in your decision tree
TreeNode can be:
    - A non-leaf node: 
        - data: contains the feature number this node is using to split the data
        - children[0]-children[4]: Each correspond to one of the values that the feature can take
        
    - A leaf node:
        - data: 'T' or 'F' 
        - children[0]-children[4]: Doesn't matter, you can leave them the same or cast to None.

'''

# Get the size of tree
nodeCounter = 0

# DO NOT CHANGE THIS CLASS
class TreeNode():
    def __init__(self, data='T', children=[-1]*5):
        self.nodes = list(children)
        self.data = data

    def save_tree(self,filename):
        obj = open(filename,'w')
        pkl.dump(self,obj)

# loads Train and Test data
def load_data(ftrain, ftest):
    Xtrain, Ytrain, Xtest = [],[],[]
    with open(ftrain, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            rw = map(int,row[0].split())
            Xtrain.append(rw)

    with open(ftest, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            rw = map(int,row[0].split())
            Xtest.append(rw)

    ftrain_label = ftrain.split('.')[0] + '_label.csv'
    with open(ftrain_label, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            rw = int(row[0])
            Ytrain.append(rw)

    print('Data Loading: done')
    return Xtrain, Ytrain, Xtest


num_feats = 274

# #A random tree construction for illustration, do not use this in your code!
# def create_random_tree(depth):
#     if(depth >= 7):
#         if(random.randint(0,1)==0):
#             return TreeNode('T',[])
#         else:
#             return TreeNode('F',[])
#
#     feat = random.randint(0,273)
#     root = TreeNode(data=str(feat))
#
#     for i in range(5):
#         root.nodes[i] = create_random_tree(depth+1)
#
#     return root


# Calculate the entropy value
def entropy(attribute, examples):
    # Count the number of all examples
    n = examples[attribute].count()
    # Count the number of distinct attribute values
    uniqueValues = examples[attribute].unique()

    entropySum = 0

    # Compute the entropy for each attribute value
    for value in uniqueValues:
        count = (examples[attribute] == value).sum()
        p = float(count)/n

        # Create a temporary dataframe of attribute and output columns
        tempdf = examples.filter([attribute, 'output'], axis=1)
        tempdf = tempdf.loc[(tempdf[attribute] == value)]
        tempdfLen = tempdf['output'].count()

        # Get the probability of each label within the current attribute value
        zeroCount = (tempdf['output'] == 0).sum()
        oneCount = (tempdf['output'] == 1).sum()
        pZero = float(zeroCount)/tempdfLen
        pOne = float(oneCount)/tempdfLen

        # Compute the entropy values
        if pZero == 0:
            entropyZero = 0
        else:
            entropyZero = pZero*(np.log2(pZero))

        if pOne == 0:
            entropyOne = 0
        else:
            entropyOne = pOne*(np.log2(pOne))

        # Get the total entropy for all outputs
        tEntropy = -(entropyZero + entropyOne)

        entropySum += p*float(tEntropy)

    return float(entropySum)

def chooseBestAttribute(examples, attributes):
    # default values
    minEntropy = 9999999999
    bestAttribute = attributes[0]

    # Find the attribute with the minimum entropy value
    for attribute in attributes:
        newEntropy = entropy(attribute, examples)
        if newEntropy < minEntropy:
            bestAttribute = attribute
            minEntropy = newEntropy

    return bestAttribute

def checkChiSquare(examples, bestAttribute, pValue):
    fObs = list()
    fExp = list()

    # Count the number of positive and negative examples
    zeroCount = (examples['output'] == 0).sum()
    oneCount = (examples['output'] == 1).sum()
    n = examples['output'].count()

    # Compute the frequencies of positive and negative examples
    zeroRatio = float(zeroCount)/n
    oneRatio = float(oneCount)/n

    # Count the number of distinct attribute values
    uniqueValues = examples[bestAttribute].unique()
    for value in uniqueValues:
        tempdf = examples.filter([bestAttribute, 'output'], axis=1)
        tempdf = tempdf.loc[(tempdf[bestAttribute] == value)]
        valueCount = tempdf['output'].count()

        # Get the observed frequencies in each case (zero or one)
        observedZeroes = float((tempdf['output'] == 0).sum())
        observedOnes = float((tempdf['output'] == 1).sum())

        # Get the expected frequencies in each case (zero or one)
        expectedZeroes = float(zeroRatio)*valueCount
        expectedOnes = float(oneRatio)*valueCount

        fObs.append(observedZeroes)
        fObs.append(observedOnes)
        fExp.append(expectedZeroes)
        fExp.append(expectedOnes)

    # Calculate the p-value of chi-square test
    chiSq, p = chisquare(fObs, fExp)

    # Compare the p-value with the p-value threshold
    if p <= pValue:
        return True
    else:
        return False

def ID3(examples, attributes, pValue):
    global nodeCounter

    # Check if all examples are positive
    if (examples['output'] == 1).sum() == examples['output'].count():
        root = TreeNode('T')
        nodeCounter+=1
        return root

    # Check if all examples are negative
    if (examples['output'] == 0).sum() == examples['output'].count():
        root = TreeNode('F')
        nodeCounter+=1
        return root

    # If there is no attribute left
    #  then select the majority element as output value
    if len(attributes) == 0:
        oneCount = (examples['output'] == 1).sum()
        zeroCount = (examples['output'] == 0).sum()
        if oneCount >= zeroCount:
            root = TreeNode('T')
            nodeCounter+=1
            return root
        else:
            root = TreeNode('F')
            nodeCounter+=1
            return root

    # Choose the best attribute with the minimum entropy
    A = chooseBestAttribute(examples, attributes)

    # Check for the Chi-squared criterion
    if checkChiSquare(examples, A, pValue):
        nodeCounter += 1
        root = TreeNode(A+1)

        attributes.remove(A)
        i = 0
        for value in range(1,6):
            examplesSubset = examples.loc[examples[A] == value]
            
            if examplesSubset.empty:
                oneCount = (examples['output'] == 1).sum()
                zeroCount = (examples['output'] == 0).sum()
                if oneCount >= zeroCount:
                    nodeCounter+=1
                    root.nodes[i] = TreeNode('T')
                else:
                    nodeCounter+=1
                    root.nodes[i] = TreeNode('F')
            else:
                root.nodes[i] = ID3(examplesSubset, attributes, pValue)
            i += 1
    else:
        # Choose the majority element when split is stopped
        zeroCount = (examples['output'] == 0).sum()
        oneCount = (examples['output'] == 1).sum()

        if oneCount >= zeroCount:
            nodeCounter+=1
            root = TreeNode('T')
            return root
        else:
            root = TreeNode('F')
            nodeCounter+=1
            return root

    return root

# Print the decision tree
def BFS(root):
    queue = list()
    queue.append(root)

    while len(queue) > 0:
        n = len(queue)
        r = list()
        for i in range(n):
            node = queue[0]
            queue.remove(node)

            r.append(node.data)
            for children in node.nodes:
                if children != -1:
                    queue.append(children)

        print (r)


# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p', required=True)
parser.add_argument('-f1', help='training file in csv format', required=True)
parser.add_argument('-f2', help='test file in csv format', required=True)
parser.add_argument('-o', help='output labels for the test dataset', required=True)
parser.add_argument('-t', help='output tree filename', required=True)

args = vars(parser.parse_args())

pval = args['p']
Xtrain_name = args['f1']
Ytrain_name = args['f1'].split('.')[0]+ '_labels.csv' #labels filename will be the same as training file name but with _label at the end

Xtest_name = args['f2']
Ytest_predict_name = args['o']

tree_name = args['t']

# Load training dataset (training features and labels)
#  and test dataset (test features)
Xtrain, Ytrain, Xtest = load_data(Xtrain_name, Xtest_name)

trainfeat = pd.DataFrame(Xtrain)
trainlabs = pd.DataFrame(Ytrain)
trainlabs.columns = range(trainlabs.shape[1])

examples = trainfeat
examples['output'] = trainlabs[0]

attributes = [i for i in range(examples.shape[1]-1)] # attributes: 0 ~ 273
pval = float(pval)

print("Training...")

# Train using ID3 algorithm
root = ID3(examples, attributes, pval)

# print ("BFS Traversal of the Tree")
# BFS(root)

#print ("Size of the tree is "+str(nodeCounter))
root.save_tree(tree_name)

print("Testing...")

# Evaluate data points in test dataset
def evaluate_datapoint(root, datapoint):
    if root.data == 'T': return 1
    if root.data == 'F': return 0
    return evaluate_datapoint(root.nodes[datapoint[int(root.data)-1]-1], datapoint)

Ypredict = []
for i in range(0,len(Xtest)):
    Ypredict.append(evaluate_datapoint(root,Xtest[i]))

with open(Ytest_predict_name, "wb") as f:
    writer = csv.writer(f,delimiter=',')
    for y in Ypredict:
        writer.writerow([y])

print("Output files generated")
