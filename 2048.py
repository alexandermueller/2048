#!/usr/bin/python
# -*- coding: utf-8 -*- 

import time
import curses
from mechanics import *
from fileSaves import *
from ai import makeMove

screen     = curses.initscr()
directions = {'right' : curses.KEY_RIGHT, 'left' : curses.KEY_LEFT, 'down' : curses.KEY_DOWN, 'up' : curses.KEY_UP}
buttons    = {curses.KEY_RIGHT : 'right', curses.KEY_LEFT : 'left', curses.KEY_DOWN : 'down', curses.KEY_UP : 'up'}
moves      = {'left' : 0, 'right' : 0, 'down' : 0, 'up' : 0, 'total' : 0, 'useless' : 0}
drops      = {'2' : ((1, 2),), '4' : ((1, 4),), '+' : ((0.2, 4), (1, 2))}
mods       = {'play_mode'  : {'P' : 'Player', 'A' : 'AI'}, 
              'win_mode'   : {'0' : '2048', '6' : '4096', '9' : '8192', 'L' : '-1'}, 
              'map_size'   : {'N' : '4x4', 'R' : '4x4', 'C' : '8x8'}, 
              'drop_type'  : {'2' : 'Twos Only', '4' : 'Fours Only', '+' : 'Twos And Fours'},
              'game_speed' : {'S' : 0.2, 'M' : 0.01, 'F' : 0},
              'game_type'  : {'O' : 'Original', 'T' : 'AI Tuning'}}
settings   = {}
stats      = {}
movesTable = {}
event      = 0

def printUI(message):
    screen.clear()
    screen.addstr(message)

def getSetting(event, settings):
    for setting in settings:
        options = [ord(option.lower()) for option in (settings[setting]).keys()]
        
        if event in options:
            return setting

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

def capturePresses(aiRunning = False, gameMap = [[0] * 4] * 4):
    global event, directions, movesTable

    stops = [ord('q'), ord('e')]

    if event not in stops:
        if aiRunning:
            event = directions[makeMove(gameMap, movesTable)]
        else: 
            event = screen.getch() 
    
    return event not in stops

def waitForSpace():
    while settings['game_type'] != 'T' and capturePresses():
        if event == ord(' '):
            break

def mainMenu():
    global screen, event, settings, stats, mods

    defaults = {'play_mode' : 'P', 'win_mode' : '0', 'map_size' : 'N', 'drop_type' : '+', 'custom_map_size' : '4x4', 'game_speed' : 'F', 'game_type' : 'O'}
    lowStats = {'high' : 0, 'most' : 0, 'least' : 0, 'largest' : 2}

    settings = getSettings(defaults)
    stats    = getStats(lowStats)
    
    mods['map_size']['R'] = 'x'.join([str(randint(2, 7)), str(randint(2, 7))])

    while True:
        menu  = '+------------------------------------- 2048 / Instructions -------------------------------------+\n'
        menu += '| 1. Use directional keys on keyboard to make moves. Press "q" to quit, "m" for main menu.      |\n'
        menu += '| 2. Combine equal tiles together to create tiles with 2x the value. Try to get to 2048 to win! |\n'
        menu += '| 3. Press the keys inside the square braces to set up the game according to your tastes.       |\n'
        menu += '+-----------------------------------------------------------------------------------------------+\n\n'
        menu += '+---------------------- Settings ----------------------+\n'
        menu += '| Play Mode...([A]I/[P]layer)......................: %s |\n' % settings['play_mode'] if 'play_mode' in settings else defaults['play_mode']
        menu += '| Win Mode....(2[0]48/409[6]/81[9]2/[L]imitless)...: %s |\n' % settings['win_mode'] if 'win_mode' in settings else defaults['win_mode']
        menu += '| Map Size....([C]ustom/[R]andom/[N]ormal).........: %s |\n' % settings['map_size'] if 'map_size' in settings else defaults['map_size']
        menu += '| Drop Type...([2]/[4]/2[+]4)......................: %s |\n' % settings['drop_type'] if 'drop_type' in settings else defaults['drop_type']
        menu += '| Game Speed..([S]low/[M]edium/[F]ast).............: %s |\n' % settings['game_speed'] if 'game_speed' in settings else defaults['game_speed']
        menu += '| Game Type...([O]riginal/AI[T]uning)..............: %s |\n' % settings['game_type'] if 'game_type' in settings else defaults['game_type']
        menu += '+------ Set To [D]efault (P,0,N,+,F,O) Settings? ------+\n\n'
        menu += 'Press space anytime to begin playing!'
        
        printUI(menu)

        setting = ''

        if not capturePresses() or event == ord(' '):
            break
        elif event == ord('d'):
            settings = dict(defaults)
        else:
            setting = getSetting(event, mods)
        
        if setting != '':
            settings[setting] = chr(event).upper()

    setSettings(settings)
    return settings['game_type']

def gameLoop(gameCount):
    global screen, event, settings, stats, moves, mods, drops
    
    seed(resetGameSeed())
    
    highScore = stats['high'] 
    (x, y)    = mods['map_size'][settings['map_size']].split('x')
    
    setDimensions(int(x), int(y))
    
    gameMap = initMap(drops[settings['drop_type']])
    moves   = {'left' : 0, 'right' : 0, 'down' : 0, 'up' : 0, 'total' : 0, 'useless' : 0}
    timeout = mods['game_speed'][settings['game_speed']]
    
    resetScore()
    resetLargest()

    while True: 
        screen.refresh()
        time.sleep(timeout)

        score     = getScore()
        highScore = max(highScore, score)
        
        chosen  = [mods[mode][settings[mode]] for mode in ['play_mode', 'win_mode', 'map_size', 'drop_type', 'game_type']]    
        topRow  = [highScore, stats['largest'], stats['least'], stats['most']]
        title   = ' / '.join(chosen)
        divider = '+----------------%s-+-----------------%s-+---------------------%s-%s-+' % tuple(['-' * len(str(stat)) for stat in topRow])
        filler  = '-' * ((len(divider) - len(title) - 4) / 2)

        header  = ' %s %s %s\n' % (filler, title, filler)
        header += '%s\n' % divider
        header += '| Highscore....: %d | Record Largest: %s | Least/Most Moves..: %s/%s |\n' % tuple(topRow)
        
        if settings['game_type'] == 'O':
            header += '| Current Score: %s | Game Largest..: %s | Current Move Count: %s %s |\n' % (printStat(score, len(str(topRow[0]))), printStat(getLargest(), len(str(topRow[1]))), ' ' * len(str(topRow[2])), printStat(moves['total'], len(str(topRow[3]))))
        else:
            header += '| Current Score: %s | Game Largest..: %s | Current Game Count: %s %s |\n' % (printStat(score, len(str(topRow[0]))), printStat(getLargest(), len(str(topRow[1]))), ' ' * len(str(topRow[2])), printStat(gameCount, len(str(topRow[3]))))

        header += '%s\n\n' % divider

        printUI(header)
        printMap(gameMap)

        if hasWon(mods['win_mode'][settings['win_mode']]):
            screen.addstr("\nCongrats! You are a winner! Press space to continue.")
            stats['least'] = min(moves['total'], stats['least']) if stats['least'] else moves['total']
            waitForSpace()  
            break
        if isTheEnd(gameMap) or not capturePresses(settings['play_mode'] == 'A', gameMap):
            screen.addstr("\nDarn, better luck next time! Press space to continue.")
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

    if not (digits % 2):
        digits += 1
        highScore = ' ' + highScore

    half = '-' * (digits / 2)
    full = '-' * digits

    statistics  = ' %s--- 2048 / Game Over ---%s \n' % (half, half)
    statistics += '+%s------ Game Stats ------%s+\n' % (half, half)
    statistics += '| Record Largest......:%s |\n' % printStat(stats['largest'], digits)
    statistics += '| Game Largest........:%s |\n' % printStat(getLargest(), digits)
    statistics += '| Highscore...........:%s |\n' % printStat(highScore, digits)
    statistics += '| Score...............:%s |\n' % printStat(getScore(), digits)
    statistics += '| Ups.................:%s |\n' % printStat(moves['up'], digits)
    statistics += '| Lefts...............:%s |\n' % printStat(moves['left'], digits)
    statistics += '| Downs...............:%s |\n' % printStat(moves['down'], digits)
    statistics += '| Rights..............:%s |\n' % printStat(moves['right'], digits)
    statistics += '| Total Moves.........:%s |\n' % printStat(moves['total'], digits)
    statistics += '| Useless Moves.......:%s |\n' % printStat(moves['useless'], digits)
    statistics += '| Most Moves Taken....:%s |\n' % printStat(stats['most'], digits)
    statistics += '| Least Moves To Win..:%s |\n' % printStat(stats['least'], digits)
    statistics += '+-----------------------%s+\n\n' % full
    statistics += 'Press space to try again! Otherwise, hit q to leave.'
    
    isNewHighScore = stats['high'] < getScore()

    printUI(statistics)
    waitForSpace()
    setStats(stats)
    
    return isNewHighScore

def main(stdscr):
    global screen, event, movesTable
    screen = stdscr
    
    curses.noecho() 
    
    if hasattr(curses, 'curs_set'):
        try:
            curses.curs_set(0)  # make the cursor invisible
        except:
            pass
    
    screen.keypad(1) 

    gameType = 'O'

    while event != ord('q'):
        event        = 0
        gameType     = mainMenu()
        gameSessions = 1000 if gameType == 'T' else 1
        movesTable   = getHashTable(movesTable) if gameType == 'T' else movesTable

        for i in xrange(0, gameSessions):
            gameLoop(i)
            isNewHighScore = endGame()
    
            # if isNewHighScore and gameType == 'T':


        if gameType == 'T': 
            setHashTable(movesTable)

    curses.endwin()

curses.wrapper(main)
