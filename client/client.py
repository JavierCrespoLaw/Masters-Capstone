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
FILE_SEND_MESSAGE = "!FILE_SEND"
FILE_DOWNLOAD_MESSAGE = "!FILE_DOWNLOAD"
FILE_DELETE_MESSAGE = "!FILE_DELETE"
LOGOUT_MESSAGE = "!LOGOUT"
FILE_LIST_MESSAGE = "!FILE_LIST"
LIST_END_MESSAGE = "!LIST_END"

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
BUFFER_SIZE = 1024

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

def sendFile(file_path):

    send(FILE_SEND_MESSAGE)

    file = open(file_path, "r")
    # file_size = os.path.getsize(file_path)

    send(os.path.basename(file_path))
    # client.send(str(file_size).encode(FORMAT))

    while True:
        bytes_read = file.read(BUFFER_SIZE)
        if not bytes_read:
            break
        send(bytes_read)

    send(FILE_END_MESSAGE)

    file.close

def receiveFile():
    file_name = receiveMessage()

    directory_path = ".\\localfiles"
    os.makedirs(directory_path, exist_ok=True)

    file_path = directory_path + "\\" + file_name

    file = open(file_path, "w")

    file_bytes = ""

    done = False

    while not done:
        data = receiveMessage()
        if data == FILE_END_MESSAGE:
            done = True
        else:
            file_bytes += data

    file.write(file_bytes)

    file.close()

def receiveList():
    list = []
    receiving = True
    while receiving:
        message = receiveMessage()
        if message == LIST_END_MESSAGE:
            receiving = False
        else:
            list.append(message)

    return list