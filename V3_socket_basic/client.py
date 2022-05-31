import socket


# Define our socket object, INET corresponds IvP4 and Stream corresponds TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Instead of binding client wants to connect to the server
s.connect((socket.gethostname(), 8000))

full_msg = ''
while True:
    # Message we receive from server
    msg = s.recv(8) # size of chunk data we want to receive at the time
    if len(msg) <= 0:
        break
    full_msg += msg.decode("utf-8")
print(full_msg)
