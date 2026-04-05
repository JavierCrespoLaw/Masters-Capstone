import socket
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

# chooses what to do based on the message received from the client
def handle_client(conn, addr):
    print(f"New connection! {addr} is connected.")
    connected = True
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
                login(conn, addr)

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

def start():
    server.listen()
    print("Server is listening on: " + SERVER)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print(f"Number of connections: {(threading.active_count() - 1)}")

print("Starting server: ")
start()
    