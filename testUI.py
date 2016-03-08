#!/usr/bin/python
# -*- coding: utf-8 -*- 

import curses
import * from mechanics

screen = curses.initscr()
event  = 0

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
    global screen, event
    score     = 0
    highScore = getHighScore() 
    
    while True:
        screen.clear()
        
        highScore = highScore if highScore > score else score
        screen.addstr('-- 2048 / Highscore: %s, Current Score: %d --' % (highScore, score))
        
        x = 1
        
        if not capturePresses():
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

    curses.endwin()

curses.wrapper(main)