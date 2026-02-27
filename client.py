import socket

def exit1():  # close socket and quit
    client.close()
    exit()

def board_editor(b, arg, player):  # try to place a piece
    try:
        col = ord(arg.lower().strip()[0]) - 97  # letter -> col
        row = int(arg[1]) - 1  # number -> row
        if b[row][col] == "-":  # empty?
            b[row][col] = player
            print(f"A {player} was placed on {arg}")
        else:
            print(f"Tried to place a {player} on {arg} but the space was full!")
        return b
    except:  # invalid input
        return False

def board_printer(b):  # show board
    print(f"""
          A     B     C     
             |     |     
       1  {b[0][0]}  |  {b[0][1]}  |  {b[0][2]}  
        _____|_____|_____
             |     |     
       2  {b[1][0]}  |  {b[1][1]}  |  {b[1][2]}  
        _____|_____|_____
             |     |     
       3  {b[2][0]}  |  {b[2][1]}  |  {b[2][2]}  
             |     |     
    """)
    print("--------------------------------------------")

def check_winner(board, player):  # did player win?
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):  # row
            return True
        if all(board[j][i] == player for j in range(3)):  # col
            return True
    if all(board[i][i] == player for i in range(3)):  # diag
        return True
    if all(board[i][2-i] == player for i in range(3)):  # other diag
        return True
    return False

def check_draw(board):  # full board?
    return all(cell != "-" for row in board for cell in row)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("\n"*99)  # clear screen

ip = input("What ip would you like to connect to (or localhost)? ")
port = input(f"What port on ip: {ip}? ")

try:
    client.connect((ip, int(port)))  # connect to server
    print("Connected to server")
except:  # anything goes wrong
    print("Something went wrong, try again later")
    exit()

game_board = [["-", "-", "-"],["-", "-", "-"],["-", "-", "-"]]
player = "O"

print("\n"*99)
print("Opponent is flipping a coin to go first")
Decision = client.recv(1024).decode()  # their coin choice
result = client.recv(1024).decode()  # did they win?
print(f"Your opponent chose {'Heads' if Decision == '1' else 'Tails'} {'but was wrong, You go first!' if result == 'F' else 'and was right, They go first!'}")
print("You play as O")
turn = 1 if result == "F" else 0  # decide first turn

while True:
    board_printer(game_board)
    if turn == 1:  # your turn
        move = input("What space would you like to place (ex: a2)? ")
        while True:  # repeat until valid
            returnval = board_editor(game_board, move, "O")
            if returnval != False:
                game_board = returnval[:]
                break
            else:
                move = input("Bad move, Try again! (ex: a2)")
        board_printer(game_board)
        client.send(move.encode())
        if check_winner(game_board, "O"):
            print("Nice, You win!")
            exit1()
        turn = 0
    if check_draw(game_board):  # tie?
        print("Cats game!")
        exit1()
    if turn == 0:  # opponent turn
        print ("Waiting on opponent")
        msg = client.recv(1024).decode()
        if not msg:  # server disconnected
            break
        game_board = board_editor(game_board, msg, "X")
        board_printer(game_board)
        if check_winner(game_board, "X"):
            print("Sorry, You lose!")
            exit1()
        turn = 1
    if check_draw(game_board):  # tie again
        print("Cats game!")
        exit1()

client.close()  # cleanup