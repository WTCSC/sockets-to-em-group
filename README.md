# Socket Tic-Tac-Toe

This project is a simple two-player Tic-Tac-Toe game written in Python using socket programming. One player runs the server and the other connects as a client. 

## Requirements

- A linux machine
- Privlleges to open and connect to sockets
- Linux 3.0 or higher
- *Socket* and *Random* modules installed

## Files

- **server.py** - Hosts the game and waits for a client to connect
- **client.py** - Connects to the server and plays the game

## How to Run

### Clone the git repository

    git clone https://github.com/WTCSC/sockets-to-em-group

Then navigate into that directory

### Start the Server

    python server.py

Choose a port number between 1024 and 65535.

### Start the Client

    python client.py

Enter the server IP address (or localhost) and the same port number used by the server.

## How to Play

- Enter moves using coordinates like a2 or c3
- The board updates after each move
- The game ends when someone wins or the board is full

## Licensing and Configuration

There is none