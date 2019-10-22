#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 15:53:25 2017

@author: apple
"""
import random

myList = []
for i in range(1, 101):
    myList.append(i)
      
trainingPoints = myList[:]

numItemsToPartition = int(len(myList) * .2)
print numItemsToPartition
holdout_points = random.sample(myList, numItemsToPartition)    

print holdout_points

for i in holdout_points:
    trainingPoints.remove(i)
    
print myList
print trainingPoints