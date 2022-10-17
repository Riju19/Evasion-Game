# Evasion

This is the implementation of the architecture for the [evasion game](http://cs.nyu.edu/courses/fall17/CSCI-GA.2965-001/evasion.html). Any questions, requests, or bug reporting, please contact us at riju.khatri@nyu.edu or niharika.sinha@nyu.edu

# Requirements

* Java 8 SDK
* Apache Maven
* Node.js (optional, client-side, for display) Tested on v5.5.0

# Clone and build

(on energon2)

```
git clone git@github.com:etytan/evasion.git
cd evasion
module load java-1.8
mvn clean package
```

(locally)
```
git clone git@github.com:etytan/evasion.git
cd evasion
mvn clean package
```


# Run

(on energon2)

```
module load java-1.8
java -jar ./target/evasion-1.0-SNAPSHOT.jar [player 1 port] [player 2 port] [max walls] [wall placement delay] ([display host] [display port])
```

(locally)

```
java -jar ./target/evasion-1.0-SNAPSHOT.jar [player 1 port] [player 2 port] [max walls] [wall placement delay] ([display host] [display port])
```

As an example if running with display using random players:

```
java -jar ./target/evasion-1.0-SNAPSHOT.jar 9000 9001 100 10 127.0.0.1 8999
node web.js 8999 8998
python ./players/random_player.py 9000
python ./players/random_player.py 9001
```
The display will be shown in your web browser here: http://127.0.0.1:8998/

# Details

Players should connect on the ports specified as arguments to the jar after it has started executing. Each message sent in either direction (to client or to server) should/will end with a newline.

Upon connecting, players will be prompted with `sendname`; they should respond with their team name. The game won't start until both players have done so.

Multiple games will be played during a single session. At the start of each game, the player will receive the message `hunter` or `prey`, which identifies their role in the upcoming match. Players should not respond to this message.

Immediately after that, the game will commence and the server will begin sending messages containing the full game state at each iteration to each player. These messages look like:

```
[playerTimeLeft] [gameNum] [tickNum] [maxWalls] [wallPlacementDelay] [boardsizeX] [boardsizeY] [currentWallTimer] [hunterXPos] [hunterYPos] [hunterXVel] [hunterYVel] [preyXPos] [preyYPos] [numWalls] {wall1 info} {wall2 info} ... 
```

Each "{wall info}" above is just a set of numbers describing a wall on the playing field. There will be `[numWalls]` such sets.

A horizontal wall is identified by: `0 [y] [x1] [x2]` where `y` is its y location, `x1` is the x location of its left-most pixel (i.e. smaller x value), and `x2` is the x location of its right-most pixel (i.e. larger x value). 

A vertical wall is identified by: `1 [x] [y1] [y2]` where `x` is its x location, `y1` is the y location of its bottom-most pixel (i.e. smaller y value), and `y2` is the y location of its top-most pixel (i.e. larger y value).

The order of the `{wall info}` sets is relevent; when the hunter references a wall to delete it should do so using the wall's place in this list, starting at 0.

Note that both players get the same game state information each tick, EXCEPT for playerTimeLeft which is specific to the given player (and given in milliseconds). (Players are not permitted to know how close their opponents are to exhausting their time limits.)

# Board

The grid is of size 300 x 300, where point (0,0) lies on the top left corner. The direction x moves positively from left to right, and y moves positively from top to bottom. The hunter starts at position (0,0) and the prey begins at (230,200).
# Hunter

In response to each received game state message, the hunter should send the following:

```
[gameNum] [tickNum] [wall type to add] [wall index to delete] [wall index to delete] [wall index to delete] ...
```

`[gameNum]` and `[tickNum]` should be relayed directly back to the server based on which game state message this action is in response to. 

`[wall type to add]` should be 0 for no wall, 1 for horizontal wall, 2 for vertical wall. There is no penalty for asking for a wall that can't be built for whatever reason.

Each `[wall index to delete]` specifies a wall to be deleted, based on its position (starting at 0) in the game state message. There can be any number of these, or none. Asking to delete a wall index that doesn't exist has no effect.

The hunter bounce behavior is as follows (* = wall or arena boundary, arrow = hunter moving in the direction it points):

```
First the pixels adjacent to both the hunter and the one being hit are considered...

+-+-+    +-+-+
|*| |    |*|↗|
+-+-+ -> +-+-+
|*|↖|    |*| |  
+-+-+    +-+-+   (1)

+-+-+    +-+-+
|*|*|    |*|*|
+-+-+ -> +-+-+
| |↖|    |↙| |
+-+-+    +-+-+   (2)

+-+-+    +-+-+
|*|*|    |*|*|
+-+-+ -> +-+-+
|*|↖|    |*|↘|
+-+-+    +-+-+   (3)


+-+-+
|*| |
+-+-+  = search is expanded, now including the other pixels adjacent to the one being hit...
| |↖|
+-+-+


  +-+        +-+
  | |        | |
+-+-+-+    +-+-+-+
|*|*| | -> |*|*| |
+-+-+-+    +-+-+-+
  | |↖|      |↙| |
  +-+-+      +-+-+   (4)

  +-+        +-+
  |*|        |*|
+-+-+-+    +-+-+-+
| |*| | -> | |*|↗|
+-+-+-+    +-+-+-+
  | |↖|      | | |
  +-+-+      +-+-+   (5)

  +-+        +-+
  |*|        |*|
+-+-+-+    +-+-+-+
|*|*| | -> |*|*| |
+-+-+-+    +-+-+-+
  | |↖|      | |↘|
  +-+-+      +-+-+   (6)

  +-+        +-+
  | |        | |
+-+-+-+    +-+-+-+
| |*| | -> | |*| |
+-+-+-+    +-+-+-+
  | |↖|      | |↘|
  +-+-+      +-+-+   (7)
```

(The same calculations are mirrored about the relevant axes for the other three directions in which the hunter can be traveling.)

# Prey

In response to each received game state message, the prey should send the following:

```
[gameNum] [tickNum] [x movement] [y movement]
```

`[gameNum]` and `[tickNum]` should be relayed directly back to the server based on which game state message this action is in response to. 

The x and y movement specifies the direction in which the prey wishes to travel. This should be 1, 0, or -1 for each -- if values lie outside this range, only their sign will be considered as the direction. For instance, (300,-300) will be considered as (1,-1) . On ticks in which the prey can't move (`tickNum % 2 == 0`), these fields will have no effect, but placeholder values should still be sent.

Prey movement here only determines its direction, since it can move only 1 unit in any direction. 
# Capture

As noted in the class site game overview, the game is over when the Euclidean distance between hunter and prey is within four, and there is no wall between them.

# Display

To enable the display, on your local machine, first run `node web.js [display port] [local webserver port]`, and go to `localhost:[local webserver port]` in your browser. You'll be accessing the port given by `[local webserver port]` locally, but if using energon you'll need a connection from energon to your local port given by `[display port]`, so router/firewall port forwarding for that port might be required. The `[display port]` is where the application sends the data to node.js. The `[local webserver port]` is where node.js sends the data to browser.

Now run the main java jar (on energon2 or locally), supplying the display host and display port parameters as listed in the run instructions above. If running locally, host should be "localhost". If running on energon, it should be the ip address of your local machine. (You can try using 'python display/getLocalIp.py' but if that fails any "what is my ip" web service should suffice.) The display port should match what you supplied to the node server.

From this point everything should just work. You should not need to reset your browser tab or the node server -- not even in between restarts of the java jar.



# Other notes

Each player has two minutes of "thinking" time, which can be distributed across ticks as they see fit. If a player's total elapsed time reaches zero on any turn, the game is over. If the prey times out, the score for the current game is recorded as the current tick number. If the hunter times out, the score for the current game is recorded as (effectively) infinity. (Note: this is basically the opposite of what was described in class -- the realtime, 1/60th of a second per tick, server-ignoring-old-moves system has been scrapped.)

The current game is over when the server sends the message `hunter` or `prey`, meaning a new game is about to start, or `done`, meaning the session is over and the player should disconnect.

# Player code

Sample player code can be found in the "players" directory (random_player.py).

To run: `python random_player.py [port on which to connect]`

# Acknowledgements

Original implementation provided by https://github.com/danielrotar/evasion
