#!/usr/bin/python
# -*- coding: utf-8 -*- 

import curses
import os.path
from mechanics import *
from ai import makeMove

screen     = curses.initscr()
directions = {'right' : curses.KEY_RIGHT, 'left' : curses.KEY_LEFT, 'down' : curses.KEY_DOWN, 'up' : curses.KEY_UP}
buttons    = {curses.KEY_RIGHT : 'right', curses.KEY_LEFT : 'left', curses.KEY_DOWN : 'down', curses.KEY_UP : 'up'}
moves      = {'left' : 0, 'right' : 0, 'down' : 0, 'up' : 0, 'total' : 0, 'useless' : 0}
drops      = {'2' : ((1, 2),), '4' : ((1, 4),), '+' : ((0.2, 4), (1, 2))}
mods       = {'play_mode' : {'P' : 'Player', 'A' : 'AI'}, 
              'win_mode'  : {'0' : '2048', '6' : '4096', '9' : '8192', 'L' : '-1'}, 
              'map_size'  : {'N' : '4x4', 'R' : '4x4'}, 
              'drop_type' : {'2' : 'Twos Only', '4' : 'Fours Only', '+' : 'Twos And Fours'}}
settings   = {}
stats      = {}
event      = 0

def printStat(stat, maxLen):
    stat = str(stat)
    return ' ' * (maxLen - len(stat)) + stat

def printMap(gameMap):
    global mods, stats
    
    largest   = getLargest()
    maxNumLen = len(str(largest))
    divider   = '+-%s-+\n' % ('-+-'.join(['-' * maxNumLen] * int(mods['map_size'][settings['map_size']][0]))) 
    title     = '%s' % mods['win_mode'][settings['win_mode']]
    filler    = ' ' * ((len(divider) - len(title) - 2) / 2)

    screen.addstr('%s-%s-%s\n' % (filler, title, filler))

    for row in gameMap:
        screen.addstr(divider)
        screen.addstr('| %s |\n' % (' | '.join([printStat(num, maxNumLen) for num in row])))

    screen.addstr(divider)

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
    stats = getAssignments('Stats.txt', {'high' : 0, 'most' : 0, 'least' : 0, 'largest' : 2})
    
    for stat in stats.keys():
        stats[stat] = int(stats[stat])

    return stats

def setSettings(settings):
    setAssignments('GameSettings.txt', settings)

def getSettings():    
    return getAssignments('GameSettings.txt', {'play_mode' : 'P', 'win_mode' : '0', 'map_size' : 'N', 'drop_type' : '+', 'custom_map_size' : '4x4'})

def capturePresses(aiRunning = False, gameMap = [[0] * 4] * 4):
    global event, directions

    if aiRunning:
        event = directions[makeMove(gameMap)]
    elif event != ord('q'):
        event = screen.getch() 
    
    return event != ord('q')

def waitForSpace():
    while capturePresses():
        if event == ord(' '):
            break

def mainMenu():
    global screen, event, settings, stats, mods

    defaults = {'play_mode' : 'P', 'win_mode' : '0', 'map_size' : 'N', 'drop_type' : '+', 'custom_map_size' : '4x4'}
    settings = getSettings()
    stats    = getStats()
    
    mods['map_size']['R'] = 'x'.join([str(randint(2, 7)), str(randint(2, 7))])

    while True:
        screen.clear()
        screen.addstr('+------------------------------------- 2048 / Instructions -------------------------------------+\n') 
        screen.addstr('| 1. Use directional keys on keyboard to make moves. Press "q" to quit.                         |\n')
        screen.addstr('| 2. Combine equal tiles together to create tiles with 2x the value. Try to get to 2048 to win! |\n')
        screen.addstr('| 3. Press the keys inside the square braces to set up the game according to your tastes.       |\n')
        screen.addstr('+-----------------------------------------------------------------------------------------------+\n\n') 
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

        # if settings['map_size'] == 'C':

    setSettings(settings)

def gameLoop():
    global screen, event, settings, stats, moves, mods, drops
    
    seed(getGameSeed())
    
    highScore = stats['high'] 
    (x, y)    = mods['map_size'][settings['map_size']].split('x')
    
    setDimensions(int(x), int(y))
    
    gameMap   = initMap(drops[settings['drop_type']])
    moves     = {'left' : 0, 'right' : 0, 'down' : 0, 'up' : 0, 'total' : 0, 'useless' : 0}
    
    resetScore()
    resetLargest()

    while True:
        screen.clear()

        score     = getScore()
        highScore = max(highScore, score)
        
        chosen    = [mods[mode][settings[mode]] for mode in ['play_mode', 'win_mode', 'map_size', 'drop_type']]    
        topRow    = [highScore, stats['largest'], stats['least'], stats['most']]
        title     = ' / '.join(chosen)
        divider   = '+----------------%s-+-----------------%s-+---------------------%s-%s-+' % tuple(['-' * len(str(stat)) for stat in topRow])
        filler    = '-' * ((len(divider) - len(title) - 4) / 2)

        screen.addstr(' %s %s %s\n' % (filler, title, filler))
        screen.addstr('%s\n' % divider)
        screen.addstr('| Highscore....: %d | Record Largest: %s | Least/Most Moves..: %s/%s |\n' % tuple(topRow))
        screen.addstr('| Current Score: %s | Game Largest..: %s | Current Move Count: %s %s |\n' % (printStat(score, len(str(topRow[0]))), printStat(getLargest(), len(str(topRow[1]))), ' ' * len(str(topRow[2])), printStat(moves['total'], len(str(topRow[3])))))
        screen.addstr('%s\n\n' % divider)
        
        printMap(gameMap) 

        if hasWon(mods['win_mode'][settings['win_mode']]):
            screen.addstr("\nCongrats! You are a winner! Press Space To Continue.")
            stats['least'] = min(moves['total'], stats['least']) if stats['least'] else moves['total']
            waitForSpace()  
            break
        if isTheEnd(gameMap) or not capturePresses(settings['play_mode'] == 'A', gameMap):
            screen.addstr("\nDarn, better luck next time! Press Space To Continue.")
            waitForSpace()
            break
        elif event in buttons.keys():
            prevMap = copyMap(gameMap)
            gameMap = moveMap(buttons[event], gameMap)

            if areNotEqual(prevMap, gameMap):
                gameMap = addNumber(gameMap, drops[settings['drop_type']])
                moves[buttons[event]] += 1
                moves['total'] += 1
                stats['most'] = max(moves['total'], stats['most'])
                stats['largest'] = max(getLargest(), stats['largest'])
            else:
                moves['useless'] += 1

    stats['high'] = highScore

def endGame():
    global screen, event, stats, moves

    highScore = str(stats['high'])
    digits = max(len(highScore), len(str(getLargest())))

    if not digits % 2:
        digits += 1
        highScore = ' ' + highScore

    half = '-' * (digits / 2)
    full = '-' * digits
    
    screen.clear()
    screen.addstr(' %s--- 2048 / Game Over ---%s \n' % (half, half))
    screen.addstr('+%s------ Game Stats ------%s+\n' % (half, half))
    screen.addstr('| Record Largest......:%s |\n' % printStat(stats['largest'], digits))
    screen.addstr('| Game Largest........:%s |\n' % printStat(getLargest(), digits))
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
    
    waitForSpace()

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
