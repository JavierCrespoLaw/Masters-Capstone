import socket
import ssl
import os

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
LOGIN_MESSAGE = "!LOGIN"
REGISTER_MESSAGE = "!REGISTER"
FILE_END_MESSAGE = "!FILE_END"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# sends a message to the server using the client socket
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    # print(client.recv(2048).decode(FORMAT))

# Receives a message from the client socket
def receiveMessage():
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        return msg
    return None

def sendFile(file_name):
    file = open(file_name, "rb")
    file_size = os.path.getsize(file_name)

    client.send(os.path.basename(file_name).encode(FORMAT))
    client.send(str(file_size).encode(FORMAT))

    data = file.read()
    client.sendall(data)
    client.send(FILE_END_MESSAGE)

    file.close