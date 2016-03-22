#!/usr/bin/python

from datetime import datetime
from random import *

gameSeed   = datetime.now()
score      = 0
largest    = 2
dimensions = [4, 4]

def setDimensions(x, y):
    global dimensions
    dimensions = [x, y]

def getDimensions(gameMap = False):
    global dimensions
    if gameMap:
       return [len(gameMap[0]), len(gameMap)]
    
    return dimensions

def getDefaultMap(x = False, y = False):
    default = []
    (x, y)  = [x, y] if x and y else getDimensions()
    
    for i in xrange(y):
        default.append([])
        for j in xrange(x):
            default[i].append(0)

    return default


def getGameSeed():
    global gameSeed
    return gameSeed

def resetScore():
    global score
    score = 0

def getScore():
    global score
    return score

def getMovePoints(gameMap):
    points = { 'up' : 0, 'down' : 0, 'right' : 0, 'left' : 0 }
    for direction in points.keys():
        if direction == 'up':
            points[direction] = solve(ccw(gameMap), True, True)
        elif direction == 'down':
            points[direction] = solve(cw(gameMap), True, True)
        elif direction == 'right':
            points[direction] = solve(cw(cw(gameMap)), True, True)
        elif direction == 'left':
            points[direction] = solve(gameMap, True, True)
    return points

def resetLargest():
    global largest
    largest = 0

def getLargest():
    global largest
    return largest

def areNotEqual(prevMap, gameMap):
    (x, y) = getDimensions()
    
    for i in xrange(y):
        for j in xrange(x):
            if prevMap[i][j] != gameMap[i][j]:
                return True
    return False

def hasWon(winMode):
    if getLargest() == int(winMode):
        return True
    return False

def isTheEnd(gameMap):
    for direction in ['right', 'left', 'down', 'up']:
        if areNotEqual(gameMap, moveMap(direction, gameMap, test = True)):
            return False
    
    return True

def copyMap(gameMap):
    result = []
    (x, y) = getDimensions()

    for i in xrange(y):
        result.append([])
        for j in xrange(x):
            result[i].append(gameMap[i][j])

    return result

def cw(gameMap):
    return zip(*gameMap[::-1])

def ccw(gameMap):
    return zip(*gameMap)[::-1]

def moveMap(direction, gameMap, test = False):
    if direction == 'up':
        gameMap = cw(solve(ccw(gameMap), test))
    elif direction == 'down':
        gameMap = ccw(solve(cw(gameMap), test))
    elif direction == 'right':
        gameMap = cw(cw(solve(cw(cw(gameMap)), test)))
    elif direction == 'left':
        gameMap = solve(gameMap, test)

    return gameMap

def solve(gameMap, test = False, points = False):
    global score, largest
    
    (x, y) = getDimensions(gameMap)
    result = getDefaultMap(x, y)
    total  = 0

    for i in xrange(y):
        posn   = 0
        mapRow = gameMap[i]
        resRow = result[i]

        for j in xrange(x):
            mapNum = mapRow[j]
            resNum = resRow[posn]

            if mapNum != 0:
                if resNum == 0:
                    result[i][posn] += mapNum
                elif resNum == mapNum:
                    result[i][posn] += mapNum
                    posn += 1

                    if test or points:
                        total += mapNum * 2
                    elif not test:
                        score  += mapNum * 2
                        largest = max(2 * mapNum, largest)
                else:
                    posn += 1
                    result[i][posn] = mapNum
   
    return result if not points else total

def addNumber(gameMap, drops, start = False):
    global largest

    result = copyMap(gameMap)
    (x, y) = getDimensions()

    while True:
        row    = randint(0, y - 1)
        column = randint(0, x - 1)
        
        if gameMap[row][column] == 0:
            if start:
                result[row][column] = drops[-1][1]
            else:
                chance = random()
                for i in xrange(len(drops)):
                    (frequency, drop) = drops[i]
                    if chance < frequency:
                        result[row][column] = drop
                        largest = max(drop, largest)
                        break

            return result

def initMap(drops):
    gameMap = getDefaultMap()

    for i in xrange(2):
        gameMap = addNumber(gameMap, drops, start = True)

    return gameMap
