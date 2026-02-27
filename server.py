import socket, random

def exit1():  # close sockets and quit
    client.close()
    server.close()
    exit()

def board_editor(b, arg, player):  # try to place a piece
    try:
        col = ord(arg.lower().strip()[0]) - 97  # letter -> index
        row = int(arg[1]) - 1  # number -> index
        if b[row][col] == "-":  # empty spot?
            b[row][col] = player
            print(f"A {player} was placed on {arg}")
        else:
            print(f"Tried to place a {player} on {arg} but the space was full!")
        return b
    except:  # invalid input
        return False

def board_printer(b):  # print the board
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

def check_winner(board, player):  # see if player won
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):  # rows
            return True
        if all(board[j][i] == player for j in range(3)):  # cols
            return True
    if all(board[i][i] == player for i in range(3)):  # diag
        return True
    if all(board[i][2-i] == player for i in range(3)):  # other diag
        return True
    return False

def check_draw(board):  # no empty spots = draw
    return all(cell != "-" for row in board for cell in row)


print("\n"*99)  # clear screen
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = input("What port would you like to bind too? ")
try:
    port = int(port)
    if port < 1024 or port > 65535:  # check valid range
        print("invalid port number")
        exit1()
    server.bind(("0.0.0.0", port))
except ValueError:  # not a number
    print("invalid port number")
    exit1()
except:
    print("something went wrong, try again later")
    exit1()

server.listen(1)  # start listening
print("Waiting for connection")

client, addr = server.accept()  # wait for client
print(f"Connected to {addr}")

game_board = [["-", "-", "-"],["-", "-", "-"],["-", "-", "-"]]
player = "X"

print("\n"*99)
print("Flip a coin to go first")
Decision = input("Would you like Heads or Tails? (1 or 2)? ")
client.send(Decision.encode())
if Decision.strip() == str(random.randint(1,2)):  # you won coin
    print(f"Congratulations, it was {'Heads' if Decision == '1' else 'Tails'}, you go for first")
    client.send("T".encode())
    turn = 1
else:  # opponent won coin
    print(f"Sorry, the coin was {'Tails' if Decision == '1' else 'Heads'} your opponent goes first")
    client.send("F".encode())
    turn = 0
print("You play as X")

while True:
    board_printer(game_board)
    if turn == 1:  # your turn
        move = input("What space would you like to place (ex: a2)? ")
        while True:  # repeat until valid
            returnval = board_editor(game_board, move, "X")
            if returnval != False:
                game_board = returnval[:]
                break
            else:
                move = input("Bad move, Try again! (ex: a2)")
        board_printer(game_board)
        client.send(move.encode())
        if check_winner(game_board, "X"):
            print("Nice, You win!")
            exit1()
        turn = 0
    if check_draw(game_board):  # tie check
        print("Cats game!")
        exit1()
    if turn == 0:  # opponent's turn
        print ("Waiting on opponent")
        msg = client.recv(1024).decode()
        if not msg:
            break
        game_board = board_editor(game_board, msg, "O")
        board_printer(game_board)
        if check_winner(game_board, "O"):
            print("Sorry, You lose!")
            exit1()
        turn = 1
    if check_draw(game_board):
        print("Cats game!")
        exit1()


client.close()  # cleanup
server.close()