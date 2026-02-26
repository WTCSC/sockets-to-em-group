import socket, random
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
print("\n"*99)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = input("What port would you like to binnd too? ")
try:
    port = int(port)
    if port < 1024 or port > 65535:
        print("invalid port number")
        exit()
    server.bind(("0.0.0.0", port))
except ValueError:
    print("invalid port number")
    exit()
except:
    print("something went wrong, try again later")

server.listen(1)
print("Waiting for connection")

client, addr = server.accept()
print(f"Connected to {addr}")

game_board = [["-", "-", "-"],["-", "-", "-"],["-", "-", "-"]]

print("\n"*99)
print("Flip a coin to go first")
Decision = input("Would you like Heads or Tails? (1 or 2)? ")
client.send(Decision.encode())
if Decision.strip() == str(random.randint(1,2)):
    print(f"Congradulations, it was {'Heads' if Decision == '1' else 'Tails'} you go for first")
    client.send("True".encode())
else:
    print(f"Sorry, the coin was {'Tails' if Decision == '1' else 'Heads'} your opponent goes first")
    client.send("False".encode())

while True:
    msg = client.recv(1024).decode()
    if not msg:
        break
    message = input("What to say? ")
    client.send(f"Server received: {message}".encode())

client.close()
server.close()