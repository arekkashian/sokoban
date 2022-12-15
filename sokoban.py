#need to reset screen better between stages, sometimes graphics from old stage can appear if new stage is smaller, ie the spaces that are not redrawn stay teh same

import curses
from random import randint

sequence1 = ("map1.txt", "map2.txt", "map3.txt", "map4.txt")
sequence2 = ("map5.txt", "map6.txt", "map7.txt", "map8.txt")


stage = 0
quitFlag = False

screen = curses.initscr()

curses.cbreak()
curses.curs_set(0)
curses.noecho()

screen.nodelay(False)

while True:

    map = {}
    graphic = {}
    boulders = set()
    holes = set()

    s = randint(0,1)

    if quitFlag:
        break

    if s == 0:
        with open(sequence1[stage]) as f:
            lines = f.readlines()
    else:
        with open(sequence2[stage]) as f:
            lines = f.readlines()


#0 is hole, 1 is empty, 2 is boulder, 3 is wall
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            graphic[(x,y)] = lines[y][x]
            if lines[y][x] == '|' or lines[y][x] == '-' or lines[y][x] == ' ':
                map[(x,y)] = 3
                graphic[(x,y)] = lines[y][x]
            if lines[y][x] == '+':
                map[(x,y)] = 1
                graphic[(x,y)] = lines[y][x]
            if lines[y][x] == '<':
                map[(x,y)] = 1
                graphic[(x,y)] = lines[y][x]
                goal = (x,y)
            if lines[y][x] == '.':
                map[(x,y)] = 1
                graphic[(x,y)] = lines[y][x]
            if lines[y][x] == '0':
                map[(x,y)] = 1
                graphic[(x,y)] = '.'
                boulders.add((x,y))
            if lines[y][x] == '@':
                map[(x,y)] = 1
                graphic[(x,y)] = '>'
                player = (x,y)
            if lines[y][x] == '^':
                map[(x,y)] = 1
                graphic[(x,y)] = '.'
                holes.add((x,y))


    for key in map.keys():
        if player == key:
            screen.addstr(key[1], key[0], '@')
        elif key in boulders:
            screen.addstr(key[1], key[0], '0')
        elif key in holes:
            screen.addstr(key[1], key[0], '^')
        else:
            screen.addstr(key[1], key[0], str(graphic[key]))

    screen.refresh()


    while True:
        c = screen.getch()

        if c == ord('q'):
            quitFlag = True
            break
        if c == ord('j'):
            if (player[0], player[1]+1) in boulders:
                if (player[0], player[1]+2) in holes:
                    boulders.remove((player[0], player[1]+1))
                    holes.remove((player[0], player[1]+2))
                    player = (player[0], player[1]+1)
                elif map[(player[0], player[1]+2)] == 1 and (player[0], player[1]+2) not in boulders:
                    boulders.remove((player[0], player[1]+1))
                    boulders.add((player[0], player[1]+2))
                    player = (player[0], player[1]+1)
            elif map[(player[0], player[1]+1)] == 1 and (player[0], player[1]+1) not in holes:
                player = (player[0], player[1]+1)

        if c == ord('k'):
            if (player[0], player[1]-1) in boulders:
                if (player[0], player[1]-2) in holes:
                    boulders.remove((player[0], player[1]-1))
                    holes.remove((player[0], player[1]-2))
                    player = (player[0], player[1]-1)
                elif map[(player[0], player[1]-2)] == 1 and (player[0], player[1]-2) not in boulders:
                    boulders.remove((player[0], player[1]-1))
                    boulders.add((player[0], player[1]-2))
                    player = (player[0], player[1]-1)
            elif map[(player[0], player[1]-1)] == 1 and (player[0], player[1]-1) not in holes:
                player = (player[0], player[1]-1)

        if c == ord('h'):
            if (player[0]-1, player[1]) in boulders:
                if (player[0]-2, player[1]) in holes:
                    boulders.remove((player[0]-1, player[1]))
                    holes.remove((player[0]-2, player[1]))
                    player = (player[0]-1, player[1])
                elif map[(player[0]-2, player[1])] == 1 and (player[0]-2, player[1]) not in boulders:
                    boulders.remove((player[0]-1, player[1]))
                    boulders.add((player[0]-2, player[1]))
                    player = (player[0]-1, player[1])
            elif map[(player[0]-1, player[1])] == 1 and (player[0]-1, player[1]) not in holes:
                player = (player[0]-1, player[1])
            
        if c == ord('l'):
            if (player[0]+1, player[1]) in boulders:
                if (player[0]+2, player[1]) in holes:
                    boulders.remove((player[0]+1, player[1]))
                    holes.remove((player[0]+2, player[1]))
                    player = (player[0]+1, player[1])
                elif map[(player[0]+2, player[1])] == 1 and (player[0]+2, player[1]) not in boulders:
                    boulders.remove((player[0]+1, player[1]))
                    boulders.add((player[0]+2, player[1]))
                    player = (player[0]+1, player[1])
            elif map[(player[0]+1, player[1])] == 1 and (player[0]+1, player[1]) not in holes:
                player = (player[0]+1, player[1])
            

        if c == ord('y'):
            if map[(player[0]-1, player[1]-1)] == 1 and ((map[(player[0]-1, player[1])] == 1 and (player[0]-1, player[1]) not in boulders) or (map[(player[0], player[1]-1)] == 1 and (player[0], player[1]-1) not in boulders)):
                if (player[0]-1, player[1]-1) not in boulders:
                    player = (player[0]-1, player[1]-1)
            
        if c == ord('u'):
            if map[(player[0]+1, player[1]-1)] == 1 and ((map[(player[0]+1, player[1])] == 1 and (player[0]+1, player[1]) not in boulders) or (map[(player[0], player[1]-1)] == 1 and (player[0], player[1]-1) not in boulders)):
                if (player[0]+1, player[1]-1) not in boulders:
                    player = (player[0]+1, player[1]-1)
            
        if c == ord('b'):
            if map[(player[0]-1, player[1]+1)] == 1 and ((map[(player[0]-1, player[1])] == 1 and (player[0]-1, player[1]) not in boulders) or (map[(player[0], player[1]+1)] == 1 and (player[0], player[1]+1) not in boulders)):
                if (player[0]-1, player[1]+1) not in boulders:
                    player = (player[0]-1, player[1]+1)
            
        if c == ord('n'):
            if map[(player[0]+1, player[1]+1)] == 1 and ((map[(player[0]+1, player[1])] == 1 and (player[0]+1, player[1]) not in boulders) or (map[(player[0], player[1]+1)] == 1 and (player[0], player[1]+1) not in boulders)):
                if (player[0]+1, player[1]+1) not in boulders:
                    player = (player[0]+1, player[1]+1)

        if player == goal:
            stage = stage + 1
            break
            
        for key in map.keys():
            if player == key:
                screen.addstr(key[1], key[0], '@')
            elif key in boulders:
                screen.addstr(key[1], key[0], '0')
            elif key in holes:
                screen.addstr(key[1], key[0], '^')
            else:
                screen.addstr(key[1], key[0], str(graphic[key]))

        screen.refresh()

curses.endwin()