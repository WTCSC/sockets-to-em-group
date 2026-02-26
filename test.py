b = [["-", "-", "-"],["-", "-", "-"],["-", "-", "-"]]

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
def message_reciever()
def board_editor(b, arg, player):
    arg1_ascii = ord(arg.lower()[1])
    arg2_value = int(arg[1]) - 1

board_printer(b)