#!/usr/bin/python

def cw(gameMap):
    return zip(*gameMap[::-1])

def ccw(gameMap):
    return zip(*gameMap)[::-1]

def printMap(gameMap):
    for row in gameMap:
        print '\t'.join(map(str, row))

def moveMap(direction, gameMap):
    print direction
    if direction == 'up':
        gameMap = cw(solve(ccw(gameMap)))
    elif direction == 'down':
        gameMap = ccw(solve(cw(gameMap)))
    elif direction == 'right':
        gameMap = cw(cw(solve(cw(cw(gameMap)))))
    else:
        gameMap = solve(gameMap)
    return gameMap

def solve(gameMap):
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
                else:
                    posn += 1
                    result[i][posn] = mapNum
   
    return result

# while true:

# randomly place a 2 or 4 somewhere


testGameMap = [[0,0,2,8], [8,8,2,0], [0,2,2,8], [2,2,8,8]]

printMap(testGameMap)
printMap(moveMap('left', testGameMap))
printMap(moveMap('right', testGameMap))
printMap(moveMap('down', testGameMap))
printMap(moveMap('up', testGameMap))

# Steps:
# Create a 
#
#
#
#