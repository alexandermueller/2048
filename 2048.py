#!/usr/bin/python
# -*- coding: utf-8 -*- 

import curses
from mechanics import *
import os.path

screen   = curses.initscr()
buttons  = {curses.KEY_RIGHT : 'right', curses.KEY_LEFT : 'left', curses.KEY_DOWN : 'down', curses.KEY_UP : 'up'}
defaults = {'play_mode' : 'P', 'win_mode' : '0', 'map_size' : 'N', 'drop_type' : '+', 'custom_map_size' : '4x4'}
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
    highScore = 0
    fileName = 'Highscores.txt'

    if os.path.isfile(fileName): 
        highScoreFile = open(fileName, 'r')
        highScore     = highScoreFile.read()
        highScoreFile.close()
    
    return int(highScore)

def setSettings(settings):
    settingsFile = open('GameSettings.txt', 'w')
    settingsList = []

    for setting in settings.keys():
        settingsList.append('%s:%s' % (setting, settings[setting]))

    settingsFile.write('\n'.join(settingsList))
    settingsFile.close()

def getSettings():
    global defaults
    
    settings = dict(defaults)
    fileName = 'GameSettings.txt'
    
    if os.path.isfile(fileName):
        settingsFile = open(fileName, 'r')

        for assignment in settingsFile.read().split('\n'):
            setting = assignment.split(':')
            if len(setting) == 2: 
                settings[setting[0]] = str(setting[1])
    
        settingsFile.close()
    
    return settings

def capturePresses():
    global event

    if event != ord('q'):
        event = screen.getch() 
    
    return event != ord('q')

def mainMenu():
    global screen, event, defaults

    while True:
        settings = getSettings()

        screen.clear()
        screen.addstr('-- 2048 / Instructions --\n') 
        screen.addstr('1. Use directional keys on keyboard to make moves. Press "q" to quit.\n')
        screen.addstr('2. Combine equal tiles together to create tiles with 2x the value. Try to get to 2048 to win!\n')
        screen.addstr('3. Press the keys inside the square braces to set up the game according to your tastes.\n\n')
        screen.addstr('---------------------- Settings ----------------------\n')
        screen.addstr('| Play Mode..([A]I/[P]layer).....................: %s |\n' % settings['play_mode'] if 'play_mode' in settings else defaults['play_mode'])
        screen.addstr('| Win Mode...(2[0]48/409[6]/81[9]2/[L]imitless)..: %s |\n' % settings['win_mode'] if 'win_mode' in settings else defaults['win_mode'])
        screen.addstr('| Map Size...([C]ustom/[R]andom/[N]ormal)........: %s |\n' % settings['map_size'] if 'map_size' in settings else defaults['map_size'])
        screen.addstr('| Drop Type..([2]/[4]/2[+]4).....................: %s |\n' % settings['drop_type'] if 'drop_type' in settings else defaults['drop_type'])
        screen.addstr('-------- Set To [D]efault (P,0,N,+) Settings? --------\n\n')
        screen.addstr('Press space anytime to begin playing!')

        mode = ''

        if not capturePresses() or event == ord(' '):
            break
        elif chr(event) in ['a', 'p']:
            mode = 'play_mode'
        elif chr(event) in ['0', '6', '9', 'l']:
            mode = 'win_mode'
        elif chr(event) in ['c', 'r', 'n']:
            mode = 'map_size'
        elif chr(event) in ['2', '4', '+']:
            mode = 'drop_type'
        elif event == ord('d'):
            setSettings(defaults)
        
        if mode != '':
            settings[mode] = chr(event).upper()
            setSettings(settings)


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