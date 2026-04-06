import socket
import os
import ssl
import threading

import validLoginInfo
import database

HEADER = 64
PORT = 5050
# SERVER = "192.168.220.165"


SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
LOGIN_MESSAGE = "!LOGIN"
FILE_END_MESSAGE = b"!FILE_END"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)



# Send a message (msg) to the connection (conn)
# sends the message length first and then the message itself
def send(msg, conn, addr):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

# receives a message from the connection (conn)
# gets the message length first, and then 
def receiveMessage(conn, addr):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        return msg
    return None

#def sendFile(conn, addr, filePath):
#    file = open(filePath, "rb")
#    file_size = os.path.getsize(filePath)
#    file_name = os.path.basename(filePath)

#    conn.send(file_name.encode(FORMAT))
#    conn.send((str(file_size)).encode(FORMAT))

#    data = file.read()
#    conn.sendall(data)

def receiveFile(conn, addr, filePath):
    file_name = conn.recv(1024).decode(FORMAT)
    file_size = conn.recv(1024).decode(FORMAT)

    file = open(file_name, "wb")

    file_bytes = b""

    done = False

    while not done:
        data = conn.recv(1024)
        if file_bytes[-9:] == FILE_END_MESSAGE:
            done = True
        else:
            file_bytes += data

    file.write(file_bytes)

    file.close()



# chooses what to do based on the message received from the client
def handle_client(conn, addr):
    print(f"New connection! {addr} is connected.")
    connected = True
    email = ""
    logged_in = False

    while connected:

        print("Receiving messages")

        msg = receiveMessage(conn, addr)

        print(f"{addr}: {msg}")

        match msg:
            case "!DISCONNECT" | None:
                print("Disconnecting")
                connected = False
            case "!LOGIN":
                print("Login attempt")
                logged_in, email = login(conn, addr)
            case "!REGISTER":
                print("Register attempt")
                register(conn, addr)

        # conn.send("Message received".encode(FORMAT))

    conn.close()

# checks to see if the user's login attempt is valid
def login(conn, addr):
    email = receiveMessage(conn, addr)
    password = receiveMessage(conn, addr)
    print(f"Login attempt detected with username {email} and password {password}")
    # emailValid = validLoginInfo.checkValidEmail(email)
    # passwordValid = validLoginInfo.checkValidPassword(password)
    loginValid = database.existsInDatabase(email, password)
    if loginValid:
        print(f"Email and password are valid!")
        # database.saveToDatabase(email, password)
        send("!SUCCESS", conn, addr)
    else:
        print(f"Email and password are not valid!")
        send("!FAILURE", conn, addr)

    return loginValid, email

def register(conn, addr):
    email = receiveMessage(conn, addr)
    password = receiveMessage(conn, addr)
    print(f"Register attempt detected with username {email} and password {password}")
    print(f"Type of email: {type(email)}")
    emailInDatabase = database.emailInDatabase(str(email))
    if not emailInDatabase:
        print(f"Registration successful!")
        database.saveToDatabase(str(email), str(password))
        send("!SUCCESS", conn, addr)
    else:
        print(f"Email already in use")
        send("!FAILURE", conn, addr)

def start_server():
    server.listen()
    print("Server is listening on: " + SERVER)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print(f"Number of connections: {(threading.active_count() - 1)}")

print("Starting server: ")
start_server()

