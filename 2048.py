#!/usr/bin/python
# -*- coding: utf-8 -*- 

import curses
from mechanics import *

screen   = curses.initscr()
buttons  = {curses.KEY_RIGHT : 'right', curses.KEY_LEFT : 'left', curses.KEY_DOWN : 'down', curses.KEY_UP : 'up'}
event    = 0
moves    = 0
mistakes = 0

def printMap(gameMap):
    for row in gameMap:
        screen.addstr('\t'.join(map(str, row)) + '\n')

def setHighScore(highScore):
    highScoreFile = open('HighScores.txt', 'w')
    highScoreFile.write(str(highScore))
    highScoreFile.close()

def getHighScore():
    highScoreFile = open('HighScores.txt', 'r')
    highScore     = highScoreFile.read()

    highScoreFile.close()
    return int(highScore)

def capturePresses():
    global event

    if event != ord('q'):
        event = screen.getch() 
    
    return event != ord('q')

def mainMenu():
    global screen, event

    screen.clear()
    screen.addstr('-- 2048 / Instructions --\n') 
    screen.addstr('1. Use directional keys on keyboard to make moves. Press "q" to quit.\n')
    screen.addstr('2. Combine equal tiles together to create tiles with 2x the value. Try to get to 2048 to win! \n')
    screen.addstr('3. Press space to start the game!')
    
    while capturePresses():
        if event == ord(' '):
            break

def gameLoop():
    global screen, event, moves, mistakes
    
    seed(getGameSeed())
 
    highScore = getHighScore() 
    gameMap   = initMap()

    while True:
        screen.clear()

        score     = getScore()
        highScore = highScore if highScore > score else score
        screen.addstr('-- 2048 / Highscore: %s, Current Score: %d --\n\n' % (highScore, score))

        printMap(gameMap)

        if isTheEnd(gameMap) or not capturePresses():
            break
        elif event in buttons.keys():
            prevMap = copyMap(gameMap)
            gameMap = moveMap(buttons[event], gameMap)

            if areNotEqual(prevMap, gameMap):
                gameMap = addNumber(gameMap)
                moves += 1
            else:
                mistakes += 1
    
    setHighScore(highScore)     

def endGame():
    global screen, event, moves, mistakes

    screen.clear()
    screen.addstr('-- 2048 / Game Over --\n') 
    screen.addstr('----- Game Stats -----\n')
    screen.addstr('Score:\t\t%d\n' % getScore())
    screen.addstr('Moves:\t\t%d\n' % moves)
    screen.addstr('Mistakes:\t%d\n\n' % mistakes)
    screen.addstr('Press space to try again! Otherwise, hit q to leave.')
    
    while capturePresses():
        if event == ord(' '):
            break

def main(stdscr):
    global screen, event
    screen = stdscr
    screen.clear()
    
    curses.noecho() 
    curses.curs_set(0) 
    screen.keypad(1) 

    while event != ord('q'):
        mainMenu()
        gameLoop()
        endGame()

    curses.endwin()

curses.wrapper(main)