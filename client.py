import socket
def board_printer(b):
    print(f"""
          A     B     B     
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
def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2-i] == player for i in range(3)):
        return True
    return False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("\n"*99)

ip = input("What ip would you like to connect to (or localhost)? ")
port = input(f"What port on ip: {ip}? ")

try:
    client.connect((ip, int(port)))
    print("Connected to server")
except:
    print("Something went wrong, try again later")
    exit()

game_board = [["-", "-", "-"],["-", "-", "-"],["-", "-", "-"]]

print("\n"*99)
print("Opponent is flipping a coin to go first")
Decision = client.recv(1024).decode()
result = client.recv(1024).decode()
print(f"Your oponent chose {'Heads' if Decision == '1' else 'Tails'} {'but was wrong, You go first!' if bool(result) else 'and was right, They go first!'}")
while True:
    if bool(result):
        board_printer(game_board)
        while True:
            choice = input("What space would you like to enter?")

    msg = input("Enter message: ")
    if not msg:
        break
    client.send(msg.encode())
    response = client.recv(1024).decode()
    print(f"Server says: {response}")

client.close()
