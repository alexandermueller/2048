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

def iterativeDFS(count, gameMap, move = ''):
    if count == 0:
        return getMovePoints(gameMap, list(move))
    else:
        maxMove    = ''
        maxPoint   = 0
        directions = ['left', 'right', 'up', 'down']
        moves = dict(enumerate([iterativeDFS(count - 1, moveMap(direction, gameMap, test = True), direction) for direction in directions]))
        for key in moves.keys():
            if maxPoint < moves[key]:
                maxPoint = moves[key]
                maxMove  = directions[int(key)]

        return maxMove if move == '' else maxPoint

def makeMove(gameMap):
    return greedy(gameMap)
    # return iterativeDFS(1, gameMap) !!!WIP!!!
