import random
import socket
import sys
import time

host = "localhost"
port = int(sys.argv[1])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

hunter = False
stream = ""
while True:
    line = ""
    while True:
        recv = sock.recv(4096)
        stream = stream + recv.decode()
        lines = stream.split("\n")
        if len(lines) > 1:
            line = lines[-2]
            stream = lines[-1]
            break
        else:
            continue

    print("received: " + line)

    val = .01
    time.sleep(val)

    to_send = None

    if line == "done":
        break
    elif line == "hunter":
        hunter = True
    elif line == "prey":
        hunter = False
    elif line == "sendname":
        to_send = "random_player_" + str(port)
    else:
        data = line.split(" ")
        if hunter:
            x = random.randint(0,50)
            wall = "0"
            if x == 0:
                wall = "1"
            elif x == 1:
                wall = "2"
            elif x == 2:
                wall = "3"
            elif x == 3:
                wall = "4"
            if random.randint(0,80) == 0:
                wall = "0 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20"
            to_send = data[1] + " " + data[2] + " " + wall
        else:
            x = random.randint(-1,1)
            y = random.randint(-1,1)
            to_send = data[1] + " " + data[2] + " " + str(x) + " " + str(y)

    if to_send is not None:
        print("sending: " + to_send)
        sock.sendall((to_send + "\n").encode())
