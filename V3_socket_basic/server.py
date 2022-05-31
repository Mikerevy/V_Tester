import socket


# socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Hold together -> bind
s.bind((socket.gethostname(), 8000))  # gethostname() - localhost, the port 8000
s.listen(5) # 5 - queue


while True:
    # Anybody connects returns client socket and IP address
    clientsocket, address = s.accept() # client socket is an object
    print(f"Connection from {address} has been established!")

    msg = bytes("Welcome to the server!", "utf-8")

    # Send information to the client socket
    clientsocket.send(msg)
    clientsocket.close()
