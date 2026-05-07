import socket
import ssl
import os
import getConfig

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "!DISCONNECT"
LOGIN_MESSAGE = "!LOGIN"
REGISTER_MESSAGE = "!REGISTER"
RESET_PASSWORD_MESSAGE = "!RESET_PASS"
FILE_END_MESSAGE = "!FILE_END"
FILE_SEND_MESSAGE = "!FILE_SEND"
FILE_DOWNLOAD_MESSAGE = "!FILE_DOWNLOAD"
FILE_DELETE_MESSAGE = "!FILE_DELETE"
LOGOUT_MESSAGE = "!LOGOUT"
FILE_LIST_MESSAGE = "!FILE_LIST"
LIST_END_MESSAGE = "!LIST_END"

getConfig.loadEnvValues()
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
BUFFER_SIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((getConfig.getIPAddress(), 5050))

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

# Sends a set of bytes to the server using the client socket
def sendBytes(bytes):
    message = bytes
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

# Receives a set of bytes from the client socket
def receiveBytes():
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        bytes = client.recv(msg_length)
        return bytes
    return None

# Sends the contents of a file to the server.
# Reads the file in bytes mode, sends them to the server one at a time, and then sends a set of bytes signaling the end of the file.
def sendFile(file_path):

    send(FILE_SEND_MESSAGE)

    file = open(file_path, "rb")

    send(os.path.basename(file_path))

    while True:
        bytes_read = file.read(BUFFER_SIZE)
        if not bytes_read:
            break
        sendBytes(bytes_read)

    sendBytes(FILE_END_MESSAGE.encode(FORMAT))

    file.close

# Receives a file from the server
# Continually read bytes coming from the server until the file end message is received
# Once all bytes have been received, writes the bytes to a file
def receiveFile():
    file_name = receiveMessage()

    directory_path = ".\\localfiles"
    os.makedirs(directory_path, exist_ok=True)

    file_path = directory_path + "\\" + file_name

    file = open(file_path, "wb")

    file_bytes = b""

    done = False

    while not done:
        data = receiveBytes()
        if data == FILE_END_MESSAGE.encode(FORMAT):
            done = True
        else:
            file_bytes += data

    file.write(file_bytes)

    file.close()

# Receive a list of values from the server
# Adds values to a list until the list end message is received
# Returns the list once all values have been obtained
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