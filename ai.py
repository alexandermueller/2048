#!/usr/bin/python

from mechanics import *
from random import *

def greedy(gameMap):
    seed()
    points = getMovePoints(gameMap)
    
    maxVal = 0
    maxKey = ''

    for key in points.keys():
        if maxVal < points[key]:
            maxVal = points[key]     
            maxKey = key

    return maxKey if maxKey != '' else points.keys()[randint(0, 3)]

def makeMove(gameMap):
    return greedy(gameMap)
