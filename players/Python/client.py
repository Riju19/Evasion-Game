import socket
import random
import sys
import time
import random

host = "localhost"
port = int(sys.argv[1])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

hunter = False
stream = ""
while True:
    while True:
        stream = stream + sock.recv(4096)
        lines = stream.split("\n")
        if len(lines) > 1:
            line = lines[-2]
            stream = lines[-1]
            break
        else:
            continue

    print "received: " + line

    val = .01
    time.sleep(val)

    tosend = None

    if line == "done":
        break
    elif line == "hunter":
        hunter = True
    elif line == "prey":
        hunter = False
    elif line == "sendname":
        tosend = "random_player_" + str(port) #Put team name here
    else:
        data = line.split(" ")
        if hunter:
            """
            TODO - Place Hunter code here

            The line read from server contains:
                playerTimeLeft
                gameNum - 0/1
                tickNum
                maxWalls
                WallPlacementDelay
                Board Size x
                Board size y
                currentWallTimer
                hunter x pos
                hunter y pos
                hunter x vel
                hunter y vel
                prey x pos
                prey y pos
                numWalls
                WallInfo1, WallInfo2 ...

            To return:
                gameNum
                tickNum
                WallsToAdd - 0,1,2,3,4
                Indices of walls to be deleted, based on the game state sent by server
            """
            wall = "0"
            tosend = data[1] + " " + data[2] + " " + wall
        else:
            """
            TODO - Place Prey code here

            The line read from server contains:
                playerTimeLeft
                gameNum - 0/1
                tickNum
                maxWalls
                WallPlacementDelay
                Board Size x
                Board size y
                currentWallTimer
                hunter x pos
                hunter y pos
                hunter x vel
                hunter y vel
                prey x pos
                prey y pos
                numWalls
                WallInfo1, WallInfo2 ...


            To return:
                gameNum
                tickNum
                prey x movement
                prey y movement
            """
            x = random.randint(-1,1)
            y = random.randint(-1,1)
            tosend = data[1] + " " + data[2] + " " + str(x) + " " + str(y)

    if tosend is not None:
        print "sending: " + tosend
        sock.sendall(tosend + "\n")