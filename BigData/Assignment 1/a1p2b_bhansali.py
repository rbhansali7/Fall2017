import sys
import string
from abc import ABCMeta, abstractmethod
from multiprocessing import Process, Manager
from pprint import pprint
import numpy as np
from random import random
from pyspark import SparkConf, SparkContext

def removePunctuations(x):
    s = x[1]
    for char in string.punctuation:
        if char != '-':
            s = s.replace(char, " ")
            res = s.lower().split(" ")
    return (x[0], res)


conf = SparkConf().setAppName("BDA").setMaster("local")
sc = SparkContext(conf=conf)

#Get list of (filenames,content) as RDD
filePath = "file:///Users/rahulbhansali1/Desktop/BDA/blogs/*.xml"
filesRDD = sc.wholeTextFiles(filePath)

"""Getting an RDD of Filenames"""
#Store the filenames in fileNameRDD
fileNameRDD = filesRDD.map(lambda x: x[0])

"""Using transformations to get an RDD of different possible industries"""
#Extract the (lowercased) distinct industry field names from the filename, and store it in an RDD of tuple (x,1)
industriesRDD = fileNameRDD.map(lambda x: x.lower().split(".")).map(lambda x: x[3]).distinct().map(lambda x: (x, 1))

#print (industriesRDD.collect())

"""Broadcasting the RDD"""
#Broadcast the industriesRDD after making it a map
broadcastRDD = sc.broadcast(industriesRDD.collectAsMap())

"""Getting the content of each file in a single RDD"""
contentRDD = filesRDD.map(lambda x: x[1])

"""Splitting the contentRDD using <date> and </date> to obtain an RDD of the form: [(date,content)]"""
#also filtering out the unrequired "<Blog>" entry that remains in the list
tmpRDD = contentRDD.flatMap(lambda x: x.split("<date>")).map(lambda x: x.split("</date>"))\
        .filter(lambda x: "Blog" not in x[0])

"""Splitting the contentRDD to obtain an RDD of the form [(year-month, content)]"""
tmpDateContentRDD = tmpRDD.map(lambda x: [x[0].split(','), x[1]]).map(lambda x: (x[0][2]+"-"+x[0][1], x[1]))
#remove punctuations from the content to take care that industry words are properly matched
dateContentRDD = tmpDateContentRDD.map(removePunctuations)

"""Match each word in the content with broadcastRDD and create an RDD of the form [(industryWord, year-month)]"""
mapResultRDD = dateContentRDD.map(lambda x: [(word, x[0]) for word in x[1] if word in broadcastRDD.value])\
        .filter(lambda x: [y for y in x if y != []] )

"""1. Convert RDD from [(industryWord, year-month)] to [((industryWord, year-month), 1)]
    2. Reduce it to get the count of the particular occurrence of the industryWord in the particular year-month
    Tuple now stores [((industryWord, year-month), count)] 
"""
freqCountRDD = mapResultRDD.flatMap(lambda x: x).map(lambda x: ((x[0],x[1]), 1)).reduceByKey(lambda x,y: x+y)

"""Convert RDD tuple into the form [( industryWord, (year-month, count)  )] and then groupByKey using industryWord
and sort according to year-month for each industryWord to get the final output
of the form [( industryWord, ((year-month, count), ...)  )]"""
outputRDD = freqCountRDD.map(lambda x: (x[0][0], (x[0][1], x[1]))).groupByKey()\
    .map(lambda x: (x[0], [(item[0], item[1]) for item in sorted(list(x[1]))]))

print (outputRDD.mapValues(tuple).collect())
