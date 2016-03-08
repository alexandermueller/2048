#!/usr/bin/python
# -*- coding: utf-8 -*- 

import curses
from mechanics import *

screen  = curses.initscr()
event   = 0
buttons = {curses.KEY_RIGHT : 'right', curses.KEY_LEFT : 'left', curses.KEY_DOWN : 'down', curses.KEY_UP : 'up'}

def printMap(gameMap):
    for row in gameMap:
        screen.addstr('\t'.join(map(str, row)) + '\n')

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
    global gameSeed, screen, event, score
    
    seed(gameSeed)
 
    highScore = getHighScore() 
    gameMap   = initMap()

    while True:
        screen.clear()
        
        highScore = highScore if highScore > score else score
        screen.addstr('-- 2048 / Highscore: %s, Current Score: %d --\n\n' % (highScore, score))

        printMap(gameMap)

        if not capturePresses():
            break
        elif event in buttons.keys():
            prevMap = copyMap(gameMap)
            gameMap = moveMap(buttons[event], gameMap)

            if areNotEqual(prevMap, gameMap):
                gameMap = addNumber(gameMap)

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

    curses.endwin()

curses.wrapper(main)