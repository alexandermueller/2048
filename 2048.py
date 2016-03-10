#!/usr/bin/python
# -*- coding: utf-8 -*- 

import curses
from mechanics import *
import os.path

screen   = curses.initscr()
buttons  = {curses.KEY_RIGHT : 'right', curses.KEY_LEFT : 'left', curses.KEY_DOWN : 'down', curses.KEY_UP : 'up'}
moves    = {'left' : 0, 'right' : 0, 'down' : 0, 'up' : 0, 'total' : 0, 'useless' : 0}
settings = {}
stats    = {}
event    = 0

def printStat(stat, maxLen):
    stat = str(stat)
    return ' ' * (maxLen - len(stat)) + stat

def printMap(gameMap):
    for row in gameMap:
        screen.addstr('\t'.join(map(str, row)) + '\n')

def setAssignments(filename, assignments):
    assignmentsFile = open(filename, 'w')
    assignmentsList = []

    for assignment in assignments.keys():
        assignmentsList.append('%s:%s' % (assignment, assignments[assignment]))

    assignmentsFile.write('\n'.join(assignmentsList))
    assignmentsFile.close()

def getAssignments(filename, defaults):
    assignments = defaults
    
    if os.path.isfile(filename):
        assignmentsFile = open(filename, 'r')

        for line in assignmentsFile.read().split('\n'):
            assignment = line.split(':')
            if len(assignment) == 2: 
                assignments[assignment[0]] = str(assignment[1])
    
        assignmentsFile.close()
    
    return assignments

def setStats(stats):
    setAssignments('Stats.txt', stats)

def getStats():    
    stats = getAssignments('Stats.txt', {'high' : 0, 'most' : 0, 'least' : 0})
    
    for stat in stats.keys():
        stats[stat] = int(stats[stat])

    return stats

def setSettings(settings):
    setAssignments('GameSettings.txt', settings)

def getSettings():    
    return getAssignments('GameSettings.txt', {'play_mode' : 'P', 'win_mode' : '0', 'map_size' : 'N', 'drop_type' : '+', 'custom_map_size' : '4x4'})

def capturePresses():
    global event

    if event != ord('q'):
        event = screen.getch() 
    
    return event != ord('q')

def mainMenu():
    global screen, event, settings, stats

    defaults = {'play_mode' : 'P', 'win_mode' : '0', 'map_size' : 'N', 'drop_type' : '+', 'custom_map_size' : '4x4'}
    settings = getSettings()
    stats    = getStats()

    while True:
        screen.clear()
        screen.addstr('-- 2048 / Instructions --\n') 
        screen.addstr('1. Use directional keys on keyboard to make moves. Press "q" to quit.\n')
        screen.addstr('2. Combine equal tiles together to create tiles with 2x the value. Try to get to 2048 to win!\n')
        screen.addstr('3. Press the keys inside the square braces to set up the game according to your tastes.\n\n')
        screen.addstr('+--------------------- Settings ---------------------+\n')
        screen.addstr('| Play Mode..([A]I/[P]layer).....................: %s |\n' % settings['play_mode'] if 'play_mode' in settings else defaults['play_mode'])
        screen.addstr('| Win Mode...(2[0]48/409[6]/81[9]2/[L]imitless)..: %s |\n' % settings['win_mode'] if 'win_mode' in settings else defaults['win_mode'])
        screen.addstr('| Map Size...([C]ustom/[R]andom/[N]ormal)........: %s |\n' % settings['map_size'] if 'map_size' in settings else defaults['map_size'])
        screen.addstr('| Drop Type..([2]/[4]/2[+]4).....................: %s |\n' % settings['drop_type'] if 'drop_type' in settings else defaults['drop_type'])
        screen.addstr('+------- Set To [D]efault (P,0,N,+) Settings? -------+\n\n')
        screen.addstr('Press space anytime to begin playing!')

        mode = ''

        if not capturePresses() or event == ord(' '):
            break
        elif event in [ord('a'), ord('p')]:
            mode = 'play_mode'
        elif event in [ord('0'), ord('6'), ord('9'), ord('l')]:
            mode = 'win_mode'
        elif event in [ord('c'), ord('r'), ord('n')]:
            mode = 'map_size'
        elif event in [ord('2'), ord('4'), ord('+')]:
            mode = 'drop_type'
        elif event == ord('d'):
            settings = dict(defaults)
        
        if mode != '':
            settings[mode] = chr(event).upper()

    setSettings(settings)

def gameLoop():
    global screen, event, stats, moves
    
    seed(getGameSeed())
 
    highScore = stats['high'] 
    gameMap   = initMap()

    while True:
        screen.clear()

        score     = getScore()
        highScore = highScore if highScore > score else score
        screen.addstr('-- 2048 / Highscore: %s, Current Score: %d, Least Moves To Win/Most Moves Ever Made: %d/%d, Move Count: %d --\n\n' % (highScore, score, stats['least'], stats['most'], moves['total']))

        printMap(gameMap)

        if isTheEnd(gameMap) or not capturePresses():
            break
        elif event in buttons.keys():
            prevMap = copyMap(gameMap)
            gameMap = moveMap(buttons[event], gameMap)

            if areNotEqual(prevMap, gameMap):
                gameMap = addNumber(gameMap)
                moves[buttons[event]] += 1
                moves['total'] += 1
                stats['most'] = moves['total'] if moves['total'] > stats['most'] else stats['most']
            else:
                moves['useless'] += 1
    
    stats['high'] = highScore

def endGame():
    global screen, event, stats, moves

    highScore = str(stats['high'])
    digits = len(highScore)

    if not digits % 2:
        digits += 1
        highScore = ' ' + highScore

    half = '-' * (digits / 2)
    full = '-' * digits
    
    screen.clear()
    screen.addstr(' %s--- 2048 / Game Over ---%s \n' % (half, half))
    screen.addstr('+%s------ Game Stats ------%s+\n' % (half, half))
    screen.addstr('| Highscore...........:%s |\n' % printStat(highScore, digits))
    screen.addstr('| Score...............:%s |\n' % printStat(getScore(), digits))
    screen.addstr('| Ups.................:%s |\n' % printStat(moves['up'], digits))
    screen.addstr('| Lefts...............:%s |\n' % printStat(moves['left'], digits))
    screen.addstr('| Downs...............:%s |\n' % printStat(moves['down'], digits))
    screen.addstr('| Rights..............:%s |\n' % printStat(moves['right'], digits))
    screen.addstr('| Total Moves.........:%s |\n' % printStat(moves['total'], digits))
    screen.addstr('| Useless Moves.......:%s |\n' % printStat(moves['useless'], digits))
    screen.addstr('| Most Moves Taken....:%s |\n' % printStat(stats['most'], digits))
    screen.addstr('| Least Moves To Win..:%s |\n' % printStat(stats['least'], digits))
    screen.addstr('+-----------------------%s+\n\n' % full)
    screen.addstr('Press space to try again! Otherwise, hit q to leave.')
    
    while capturePresses():
        if event == ord(' '):
            break

    setStats(stats)

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
