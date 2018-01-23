import sys
from abc import ABCMeta, abstractmethod
from multiprocessing import Process, Manager
from pprint import pprint
import numpy as np
import string
from random import random
from pyspark import SparkConf, SparkContext


data = [(1, "The horse raced past the barn fell"),
            (2, "The complex houses married and single soldiers and their families"),
            (3, "There is nothing either good or bad, but thinking makes it so"),
            (4, "I burn, I pine, I perish"),
            (5, "Come what come may, time and the hour runs through the roughest day"),
            (6, "Be a yardstick of quality."),
            (7, "A horse is the projection of peoples' dreams about themselves - strong, powerful, beautiful"),
            (8,
             "I believe that at the end of the century the use of words and general educated opinion will have altered so much that one will be able to speak of machines thinking without expecting to be contradicted."),
            (9, "The car raced past the finish line just in time."),
            (10, "Car engines purred and the tires burned.")]


conf = SparkConf().setAppName("BDA").setMaster("local")
sc = SparkContext(conf=conf)


def removePunctuations(s):
    newS = s[1]
    for char in string.punctuation:
        newS = newS.replace(char, " ")
    output = [s.strip().lower() for s in newS.split() if s]
    return output

"""WordCount implementation below"""


rdd = sc.parallelize(data)
#map Step
rdd = sc.parallelize(data)
#map Step
lowerRDD = rdd.map(removePunctuations)
mapWords = lowerRDD.flatMap(lambda x: x).map(lambda x: (x,1))
#printing values after map step
print ("Values after map step:")
print (mapWords.collect())

#reduce Step
wordCount = mapWords.reduceByKey(lambda x, y : x + y)
#printing values after reduce step
print ("Values after reduce step:")
print (sorted(wordCount.collect()))


"""End of WordCount implementation"""





"""SetDifference implementation below"""

data1 = [('R', ['apple', 'orange', 'pear', 'blueberry']),
             ('S', ['pear', 'orange', 'strawberry', 'fig', 'tangerine'])]
data2 = [('R', [x for x in range(50) if random() > 0.5]),
             ('S', [x for x in range(50) if random() > 0.75])]


rdd = sc.parallelize(data1)
#map Step
mapRDD = rdd.flatMap(lambda x : [(a,b) for a in x[1] for b in x[0]])
# printing values after map step
print ("Values after map step:")
print (mapRDD.collect())
#reduce step
groupmap = mapRDD.groupByKey().filter(lambda x : x[0] if len(list(x[1])) == 1 and list(x[1])[0] == 'R' else None).\
    map(lambda x: x[0])
#printing values after reduce step
print ("Values after reduce step:")
print (groupmap.collect())

#2nd dataset
rdd = sc.parallelize(data2)
#map Step
mapRDD = rdd.flatMap(lambda x : [(a,b) for a in x[1] for b in x[0]])
# printing values after map step
print ("Values after map step:")
print (mapRDD.collect())
#reduce step
groupmap = mapRDD.groupByKey().filter(lambda x : x[0] if len(list(x[1])) == 1 and list(x[1])[0] == 'R' else None).\
    map(lambda x: x[0])
#printing values after reduce step
print ("Values after reduce step:")
print (groupmap.collect())

"""End of SetDifference implementation"""





