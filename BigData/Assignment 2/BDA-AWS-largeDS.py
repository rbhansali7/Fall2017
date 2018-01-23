
# coding: utf-8

# In[1]:

import sys
import re
import io
import zipfile
import hashlib
import numpy as np
from pyspark import SparkConf, SparkContext
from tifffile import TiffFile
import pyspark
import random
from scipy import linalg


# In[2]:
sc = pyspark.SparkContext(appName="Rahul")

filePath = "hdfs:/data/large_sample"


# ## Part 1 (a)

zipFilesRDD = sc.binaryFiles(filePath)

def getName(s):
    l=s.split("/")
    return l[-1]

namePlusZipRDD = zipFilesRDD.map(lambda x: (getName(x[0]),x[1]))


# ## 1(b)

def getOrthoTif(zfBytes):
 #given a zipfile as bytes (i.e. from reading from a binary file),
# return a np array of rgbx values for each pixel
 bytesio = io.BytesIO(zfBytes)
 zfiles = zipfile.ZipFile(bytesio, "r")
 #find tif:
 for fn in zfiles.namelist():
  if fn[-4:] == '.tif':#found it, turn into array:
   tif = TiffFile(io.BytesIO(zfiles.open(fn).read()))
   return tif.asarray()


namePlusArrayRDD = namePlusZipRDD.map(lambda x: (x[0],getOrthoTif(x[1])))


# ## 1(c)


def partition(image):
    subImages = list()
    for i in range(0,2500,500):
        for j in range(0,2500,500):
            subImages.append(image[i:i+500,j:j+500])
    return subImages


imagePartitionedRDD = namePlusArrayRDD.map(lambda x: (x[0],partition(x[1])))


# ## 1(d)


def nameImages(x):
    t = list()
    name, arr = x
    for i in range(len(arr)):
        t.append((name+"-"+str(i),arr[i]))
    return t  


rdd5 = imagePartitionedRDD.map(lambda x: nameImages(x))


imageNameArrayRDD = rdd5.flatMap(lambda x: x)


# ## 1(e)


imagesToPrint = ['3677454_2025195.zip-0', '3677454_2025195.zip-1', '3677454_2025195.zip-18', '3677454_2025195.zip-19']
images = imageNameArrayRDD.filter(lambda x: x[0] in imagesToPrint)
l = images.collect()
for i in range(len(l)):
    print (l[i][0],l[i][1][0][0])


# # Part 2(a)

#compress RGBI into a single value
def compressRGBI(x):
    name, mat = x
    rows=len(mat)
    cols=len(mat[0])
    compressedMat = [ [0 for j in range(cols)] for i in range(rows) ]
    
    for i in range(rows):
        for j in range(cols):
            r=mat[i][j][0]
            g=mat[i][j][1]
            b=mat[i][j][2]
            infra=mat[i][j][3]
            compressedMat[i][j]= int(((r+g+b)/3)*(infra/100))
    return (name,compressedMat)


singleValuePixelRDD = imageNameArrayRDD.map(lambda x: compressRGBI(x))

#persist this RDD as its going to be used later
singleValuePixelRDD.persist()

#reduce resolution of image by a factor of k
def reduceImageResolution(image,k):
    
    image=np.array(image)
    rows=len(image)//k
    cols=len(image[0])//k
    compressedMat = [ [0 for j in range(cols)] for i in range(rows) ]

    for i in range(0,500,k):
        for j in range(0,500,k):
            subImage=image[i:i+k,j:j+k]
            avg=0
            for m in range(k):
                for n in range(k):
                    avg+=subImage[m][n]
            avg=(avg/(k*k))
            compressedMat[i//k][j//k]=avg
                    
    return compressedMat


def rowDiff(x):
    rows=len(x)
    cols=len(x[0])-1
    
    rowDiffMat = [ [0 for i in range(cols)]  for i in range(rows)]
    
    for i in range(rows):
        for j in range(cols):
            diff=x[i][j+1]-x[i][j]
            if diff<-1:
                diff=-1
            elif diff>1:
                diff=1
            else:
                diff=0
            rowDiffMat[i][j]=diff
    
    return rowDiffMat


def colDiff(x):
    rows=len(x)-1
    cols=len(x[0])
    
    colDiffMat = [ [0 for i in range(cols)]  for i in range(rows)]
    
    for i in range(cols):
        for j in range(rows):
            diff=x[j+1][i]-x[j][i]
            if diff<-1:
                diff=-1
            elif diff>1:
                diff=1
            else:
                diff=0
            colDiffMat[j][i]=diff
    
    return colDiffMat


def flatten(rowMat, colMat):
    features = list()
    
    row=len(rowMat)
    col=len(rowMat[0])
    for i in range(row):
        for j in range(col):
            features.append(rowMat[i][j])
    
    row=len(colMat)
    col=len(colMat[0])
    for i in range(row):
        for j in range(col):
            features.append(colMat[i][j])
    
    return features


#Creating 39 or 38 sized chunks. First 36 chunks are sized 39 and rest of the chunks are sized 38.
def createChunks(x):
    name , features = x
    chunks = 128
    chunkSize= int(len(features)/chunks)
    remainder = len(features) - (chunkSize*chunks)
    chunkList = list()
    
    i=0
    for j in range(chunks):
        if j<remainder:
            arr = np.array(features[i:i+chunkSize+1])
            i+=(chunkSize+1)
        else:
            arr = np.array(features[i:i+chunkSize])
            i+=(chunkSize)
        chunkList.append(arr)
        
    return (name,chunkList)

#Pick up the last bit (LSB) of the hash value returned by each chunk and combine them to get the signature.
def getHash(x):
    name, chunkList = x
    #chunkList is a numpy array list
    #features = np.array(features)
    
    signature = ""
    for chunk in chunkList:
        h=hashlib.md5()
        h.update(chunk)
        s=h.hexdigest()
        b = bin(int(s, 16))
        num = b[-1]
        signature+=num
    
    return (name,signature)


#For each image, create a list of the bucket values returned by passing each band of the image to the hash function.
def findHashBuckets(x, bands, buckets):
    #bands = 10
    #buckets = 1249
    rows = int(128/bands)
    hashList = list()
    
    name, hVal = x
    j=0
    for i in range(bands):
        hashList.append(hash(hVal[j:j+rows])%buckets)
        j+=rows
    
    return (name,hashList)


#Create a tuple of ((bucketValue, band_no) , name_of_image) as (key,value) pairs, so that it can be grouped
#together to get a complete list of images that map to a particular (bucketValue, band_no).
#i.e. finally bucketsBandsImagesRDD stores 
#-> ( (bucketValue, band_no), [list of images with this (bucketValue, band_no)])
def flatHash(x):
    name,hashes = x
    resList = list()
    i=0
    for h in hashes:
        resList.append(((h,i),name))
        i+=1
    return resList

#Get the candidate list
def makeCandidateList(x):
    name, cList = x
    candList = list()
    
    for i in range(len(cList)):
        for item in cList[i]:
            if item!=name:
                candList.append(item)
    
    finalList = list(set(candList))
    
    return (name,finalList)  


#Apply SVD on the chosen sample to get the Vh transposed matrix
def generateVh(x):
    batchNum , images = x
    
    featureMatrix = list()
    for item in images:
        name, feature = item
        featureMatrix.append(feature)
        
    featureMatrix=np.array(featureMatrix)    
    mu, std = np.mean(featureMatrix, axis=0), np.std(featureMatrix, axis=0)
    #std can be 0 handle that => do fm_zs=0
    std[std==0]=1
    fm_zs = (featureMatrix - mu) / std  
    #U, s, Vh = linalg.svd(fm_zs, full_matrices=1)
    U, s, Vh = linalg.svd( fm_zs, full_matrices=0, compute_uv=1 )
    low_dim_p = 10
    #lowDimMatrix = U[:,0:low_dim_p]
    
    Vtrans = Vh.transpose()
    return Vtrans[:,0:10]

#multiply each image x to the broadcastRDD to get the reduced dimension matrix for each image
def multiplyWithVh(x, broadcastRDD):
    name, features =x
    features=np.array(features)
    reducedMat = np.matmul(features, np.array(broadcastRDD.value))
    
    #reducedMat is a 2-D matrix of just one row, so returning that row as reducedMat[0]
            
    return (name,reducedMat[0])

#calculate Euclidean distance between two vectors of length k  
def euclideanDistance(a, b, k):
    name_a, x = a
    name_b, y = b
    dist=0
    for i in range(k):
        dist+=((x[i]-y[i])*(x[i]-y[i]))
    return (name_b,np.sqrt(dist))


#Call Master Function with parameters (singleValuePixelRDD, factor, band, bucket) values
def MasterFunction(singleValuePixelRDD, factor, bands, buckets):

    reducedImageResRDD = singleValuePixelRDD.map(lambda x: (x[0], reduceImageResolution(x[1],factor)))

    rowDiffMat = reducedImageResRDD.map(lambda x: (x[0],rowDiff(x[1])))
    colDiffMat = reducedImageResRDD.map(lambda x: (x[0],colDiff(x[1])))
    rowAndColCombinedRDD = reducedImageResRDD.map(lambda x: (x[0],rowDiff(x[1]),colDiff(x[1])))

    #stores records of the form (name, featureVector)
    nameFeaturesRDD = rowAndColCombinedRDD.map(lambda x: (x[0],flatten(x[1],x[2])))

    if factor==10:
        featuresToPrint = ['3677454_2025195.zip-1', '3677454_2025195.zip-18']
        featuresRDD = nameFeaturesRDD.filter(lambda x: x[0] in featuresToPrint)
        printRDD = featuresRDD.map(lambda x: (x[0],np.array(x[1]))).collect()
        print (printRDD)

    #create chunks of the featureVector
    chunkRDD = nameFeaturesRDD.map(lambda x: createChunks(x))

    #get the signature for each image: records of the form (name, signature)
    nameSignatureRDD = chunkRDD.map(lambda x: getHash(x))

    #apply LSH on the signature using bands, bucket values passed in the MasterFunction
    nameHashedSignatureRDD = nameSignatureRDD.map(lambda x: findHashBuckets(x,bands,buckets))


    rdd13 = nameHashedSignatureRDD.flatMap(lambda x: flatHash(x))

    #get an RDD that stores records as -> ( (band,bucketValue) , (list of images that mapped to that (band,bucketValue) ) )
    bucketsBandsImagesRDD = rdd13.groupByKey().mapValues(list)

    queryList = ['3677454_2025195.zip-0', '3677454_2025195.zip-1', '3677454_2025195.zip-18', '3677454_2025195.zip-19']
    #Filter out the required (queryImage, list of hashed signature values of that image)
    rdd15 = nameHashedSignatureRDD.filter(lambda x: x[0] in queryList)

    #Get an RDD that contains tuples of the form ( (bucketValue, band_no) , queryImage)
    #of all (bucketValue, band_no) returned while hashing queryImage's signature.
    rdd16 = rdd15.flatMap(lambda x: flatHash(x))

    #Get tuples of the form -> 
    #( (bucketValue, band_no) , (queryImage, [list of all images that mapped to (bucketValue, band_no)]))
    #Here (bucketValue, band_no) are the values which the hash of chunks of signature of queryImage returned.
    rdd17 = rdd16.join(bucketsBandsImagesRDD)

    #From above RDD, we can now use queryImage as the key to get the list of all images
    #that mapped to any of the (bucketValue, band_no) which was returned by hashing chunks of signature of queryImage.
    rdd18 = rdd17.map(lambda x: (x[1][0],x[1][1])).groupByKey().mapValues(list)

    #Get the list of candidates in the RDD
    candidatesListRDD = rdd18.map(lambda x: makeCandidateList(x))

    #Print the candidate lists
    queryPrintList = ['3677454_2025195.zip-1', '3677454_2025195.zip-18']
    rdd20 = candidatesListRDD.filter(lambda x: x[0] in queryPrintList)
    l3 = rdd20.collect()
    print("List of similar candidates when running for factor "+str(factor)+" are")
    for i in range(len(l3)):
        print (l3[i][0], l3[i][1])

    #Make a list of 10 image samples randomly chosen out of all the images
    sampleList = nameFeaturesRDD.map( lambda x: x[0]).takeSample(False, 10)
    #Get the feature vector of all the chosen images in an RDD
    tmpFeaturesRDD = nameFeaturesRDD.filter( lambda x: x[0] in sampleList)
    #Use any key (used 7) to convert RDD to the form -> (  (key, (name-1,features)) , (key,(name-2,features)) )
    #Then use groupByKey to get -> (key, ((name-1,features),(name-2,features)...))
    sampleRDD = tmpFeaturesRDD.map( lambda x: (7, x)).groupByKey().mapValues(list)

    #VhMatrix stores the Vh transposed matrix
    VhMatrix = sampleRDD.map(lambda x: generateVh(x)).collect()

    #Broadcasting the VhMatrix so that it can be used to calculate reduced dimension features of all images
    broadcastRDD = sc.broadcast(VhMatrix)

    #Now we'll use this broadcastRDD to multiply it to all images to get their reduced dimensions.
    #Store it in reducedRDD
    reducedRDD = nameFeaturesRDD.map(lambda x: multiplyWithVh(x,broadcastRDD) )


    #Below code is to collect, calculate and print the candidate value distances for each query image
    candList1 = l3[0][1]
    candList2 = l3[1][1]
    name1 = l3[0][0]
    name2 = l3[1][0]

    name1Vals = reducedRDD.filter(lambda x: x[0]==name1).collect()


    name2Vals = reducedRDD.filter(lambda x: x[0]==name2).collect()


    candList1Vals = reducedRDD.filter(lambda x: x[0] in candList1).collect()


    candList2Vals = reducedRDD.filter(lambda x: x[0] in candList2).collect()

    dist1Vals = list()
    dist2Vals = list()

    for j in range(len(candList1Vals)):
        dist1Vals.append(euclideanDistance(name1Vals[0], candList1Vals[j],10))
            
    for j in range(len(candList2Vals)):
        dist2Vals.append(euclideanDistance(name2Vals[0], candList2Vals[j],10))

    dist1Vals.sort(key=lambda x:x[1])
    dist2Vals.sort(key=lambda x:x[1])

    print("Euclidean Distances when running for factor "+str(factor)+" are")
    for i in range(len(dist1Vals)):
        print(name1 , dist1Vals[i][0], dist1Vals[i][1])

    for i in range(len(dist2Vals)):
        print(name2 , dist2Vals[i][0], dist2Vals[i][1])


#Call the MasterFunction with appropriate parameters of (factor,band,bucket) values


MasterFunction(singleValuePixelRDD,10,10,1201)

MasterFunction(singleValuePixelRDD,5,10,1201)


