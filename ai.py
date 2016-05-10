#!/usr/bin/python

from mechanics import *
from random import *

def greedy(gameMap):
    points = getMovePoints(gameMap)
    
    maxVal = 0
    maxKey = ''

    for key in points.keys():
        if maxVal < points[key]:
            maxVal = points[key]     
            maxKey = key

    return maxKey if maxKey != '' else points.keys()[randint(0, 3)]

def iterativeDFS(count, gameMap, direction = False):
    points = getMovePoints(gameMap, direction)

    if count == 0:
        return [points, direction]
    else:
        directions = {}
        maxPoints  = 0

        for d in ['left', 'right', 'up', 'down']:
            (p, move) = iterativeDFS(count - 1, moveMap(d, copyMap(gameMap), True), d)
            directions[p] = move
            maxPoints     = p if p > maxPoints else maxPoints

        return [maxPoints, directions[maxPoints]]

def makeMove(gameMap):
    seed()
    return ['left', 'right', 'up', 'down'][randint(0, 3)] #iterativeDFS(2, gameMap)[1] !!WIP!!
