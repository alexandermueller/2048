#!/usr/bin/python

from datetime import datetime
from random import *

gameSeed = datetime.now()
score    = 0

def areNotEqual(prevMap, gameMap):
    for i in xrange(4):
        for j in xrange(4):
            if prevMap[i][j] != gameMap[i][j]:
                return True
    return False

def copyMap(gameMap):
    result = []
    for i in xrange(4):
        result.append([])
        for j in xrange(4):
            result[i].append(gameMap[i][j])

    return result

def cw(gameMap):
    return zip(*gameMap[::-1])

def ccw(gameMap):
    return zip(*gameMap)[::-1]

def moveMap(direction, gameMap):
    if direction == 'up':
        gameMap = cw(solve(ccw(gameMap)))
    elif direction == 'down':
        gameMap = ccw(solve(cw(gameMap)))
    elif direction == 'right':
        gameMap = cw(cw(solve(cw(cw(gameMap)))))
    elif direction == 'left':
        gameMap = solve(gameMap)

    return gameMap

def solve(gameMap):
    global score
    result = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

    for i in xrange(4):
        posn   = 0
        mapRow = gameMap[i]
        resRow = result[i]

        for j in xrange(4):
            mapNum = mapRow[j]
            resNum = resRow[posn]

            if mapNum != 0:
                if resNum == 0:
                    result[i][posn] += mapNum
                elif resNum == mapNum:
                    result[i][posn] += mapNum
                    posn += 1
                    score += mapNum * 2
                else:
                    posn += 1
                    result[i][posn] = mapNum
   
    return result

def addNumber(gameMap, start = False):
    result = copyMap(gameMap)

    while True:
        row    = randint(0,3)
        column = randint(0,3)
        
        if gameMap[row][column] == 0:
            result[row][column] = 2 if start or random() < 0.8 else 4
            return result

def initMap():
    gameMap = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

    for i in xrange(2):
        gameMap = addNumber(gameMap, True)

    return gameMap

# def printMap(gameMap):
#     for row in gameMap:
#         print '\t'.join(map(str, row))

# testGameMap = [[0,0,2,8], [8,8,2,0], [0,2,2,8], [2,2,8,8]]

# printMap(testGameMap)

# for direction in ['left', 'right', 'up', 'down']:
#     print direction
#     printMap(moveMap(direction, testGameMap))    