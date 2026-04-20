import socket
import os
import ssl
import threading

import validLoginInfo
import database
import getConfig
import sendEmail
import twoFactorAuth

HEADER = 64

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
LOGIN_MESSAGE = "!LOGIN"
FILE_END_MESSAGE = "!FILE_END"
FILE_SEND_MESSAGE = "!FILE_SEND"
LOGOUT_MESSAGE = "!LOGOUT"
FILE_LIST_MESSAGE = "!FILE_LIST"
LIST_END_MESSAGE = "!LIST_END"
BUFFER_SIZE = 1024



SERVER = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5050
SERVER_ADDR = (SERVER, SERVER_PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDR)

DATABASE = socket.gethostbyname(socket.gethostname())
DATABASE_PORT = 5051
DATABASE_ADDR = (DATABASE, DATABASE_PORT)


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

# sends a file in folder (username) and with name (file_name)
def sendFile(conn, addr, username, file_name):
    directory_path = ".\\documents\\" + username
    file_path = directory_path + "\\" + file_name

    file = open(file_path, "r")

    send(os.path.basename(file_path), conn, addr)

    while True:
        bytes_read = file.read(BUFFER_SIZE)
        if not bytes_read:
            break
        send(bytes_read, conn, addr)

    send(FILE_END_MESSAGE, conn, addr)

    file.close

def deleteFile(username, file_name):
    directory_path = ".\\documents\\" + username
    file_path = directory_path + "\\" + file_name

    if os.path.exists(file_path):
        os.remove(file_path)


# Receive a file and store it in folder (username)
def receiveFile(conn, addr, username):

    file_name = receiveMessage(conn, addr)

    directory_path = ".\\documents\\" + username
    os.makedirs(directory_path, exist_ok=True)

    file_path = directory_path + "\\" + file_name

    file = open(file_path, "w")

    file_bytes = ""

    done = False

    while not done:
        data = receiveMessage(conn, addr)
        if data == FILE_END_MESSAGE:
            done = True
        else:
            file_bytes += data

    file.write(file_bytes)

    file.close()

def sendFileList(conn, addr, username):
    list = []

    directory_path = ".\\documents\\" + username

    if os.path.isdir(directory_path):
        list = os.listdir(directory_path)
    
    for i in list:
        send(i, conn, addr)

    send(LIST_END_MESSAGE, conn, addr)

# chooses what to do based on the message received from the client
def handle_client(conn, addr):
    print(f"New connection! {addr} is connected.")
    connected = True
    username = ""
    logged_in = False
    googleAuthSuccess = False

    while connected:

        print("Receiving messages")

        msg = receiveMessage(conn, addr)

        print(f"{addr}: {msg}")

        match msg:
            case "!DISCONNECT" | None:
                print("Disconnecting")
                connected = False
            case "!LOGIN":
                if not logged_in:
                    print("Login attempt")
                    logged_in, username = login(conn, addr)
                else:
                    print("Error: user is already logged in")
            case "!AUTH":
                if logged_in:
                    print("Authentication attempt")
                    googleAuthSuccess, honeytoken = authenticate(username, conn, addr)
                else:
                    print("Error: need to log in first")
            case "!CANCEL_AUTH":
                if logged_in and not googleAuthSuccess:
                    print("Returning user to login")
                    username = ""
                    logged_in = False
                    googleAuthSuccess = False
                else:
                    print("Error: user shouldn't be in authentication screen")
            case "!REGISTER":
                if not logged_in:
                    print("Register attempt")
                    register(conn, addr)
                else:
                    print("Error: user is already logged in")
            case "!FILE_SEND":
                if logged_in and googleAuthSuccess:
                    print("User " + username + " is sending a file.")
                    receiveFile(conn, addr, username)
                else:
                    print("Error: user is not logged in")
            case "!LOGOUT":
                if logged_in and googleAuthSuccess:
                    print("User " + username + " is logging out.")
                    username = ""
                    logged_in = False
                    googleAuthSuccess = False
                else:
                    print("Error: user is not logged in")
            case "!FILE_LIST":
                if logged_in and googleAuthSuccess:
                    print("User " + username + " is requesting a list of their files.")
                    sendFileList(conn, addr, username)
                else:
                    print("Error: user is not logged in")
            case "!FILE_DOWNLOAD":
                if logged_in and googleAuthSuccess:
                    print("User " + username + " is trying to download a file.")
                    file_name = receiveMessage(conn, addr)
                    sendFile(conn, addr, username, file_name)
                else:
                    print("Error: user is not logged in")
            case "!FILE_DELETE":
                if logged_in and googleAuthSuccess:
                    print("User " + username + " is trying to delete a file.")
                    file_name = receiveMessage(conn, addr)
                    deleteFile(username, file_name)

        # conn.send("Message received".encode(FORMAT))

    conn.close()

# checks to see if the user's login attempt is valid
def login(conn, addr):
    username = receiveMessage(conn, addr)
    password = receiveMessage(conn, addr)
    print(f"Login attempt detected with username {username} and password {password}")
    loginValid = database.existsInDatabase(username, password)
    if loginValid:
        print(f"Username and password are valid!")
        send("!SUCCESS", conn, addr)
    else:
        print(f"Username and password are not valid!")
        send("!FAILURE", conn, addr)

    return loginValid, username

def authenticate(username, conn, addr):
    userOTP = receiveMessage(conn, addr)
    code1, code2, code3 = database.getCodesFromDatabase(username)
    authNum = int(database.getAuthNumFromDatabase(username))
    result = twoFactorAuth.verifyCodes(code1, code2, code3, userOTP, authNum)
    authSuccess = False
    honeytoken = False
    match result:
        case "SUCCESS":
            print("Authentication Successfull!")
            send("!SUCCESS", conn, addr)
            authSuccess = True
        case "FAILURE":
            print("Authentication failed!")
            send("!FAILURE", conn, addr)
        case "HONEYTOKEN":
            print("Honeytoken triggered!")
            send("!HONEYTOKEN", conn, addr)
            honeytoken = True

    return authSuccess, honeytoken


def register(conn, addr):
    username = receiveMessage(conn, addr)
    email = receiveMessage(conn, addr)
    password = receiveMessage(conn, addr)
    authenticationNumber = receiveMessage(conn, addr)
    print(f"Register attempt detected with username {username}, email {email}, password {password}, and authentication number {authenticationNumber}")
    usernameInDatabase = database.usernameInDatabase(str(username))
    emailInDatabase = database.emailInDatabase(str(email))
    if not emailInDatabase and not usernameInDatabase:
        print(f"Registration successful!")
        database.saveToUserDatabase(str(username), str(email), str(password))
        database.saveToAuthenticationNumbersDatabase(str(username), int(authenticationNumber))
        twoFactorAuthenticationSetup(str(username), str(email))
        send("!SUCCESS", conn, addr)
    else:
        print(f"Username or Email already in use")
        send("!FAILURE", conn, addr)

def twoFactorAuthenticationSetup(username, email):
    code1, code2, code3 = twoFactorAuth.generateCodes()
    database.saveToCodesDatabase(username, code1, code2, code3)
    sendEmail.emailQRCodes(username, getConfig.getEmailServer(), getConfig.getPasswordServer(), email, code1, code2, code3)


def start_server():
    server.listen()
    print("Server is listening on: " + SERVER)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print(f"Number of connections: {(threading.active_count() - 1)}")

def start():
    if getConfig.loadEnvValues() == False:
        print("Error: Unable to get config values. ")
        return
    database.createDatabases()
    print("Starting server: ")
    start_server()


def main():
    getConfig.loadEnvValues()
    code1, code2, code3 = database.getCodesFromDatabase("testUser")
    # sendEmail.emailQRCodes("testUser", getConfig.getEmailServer(), getConfig.getPasswordServer(), "crespoj1@sunypoly.edu", code1, code2, code3)
    print(twoFactorAuth.verifyCodes(code1, code2, code3, "748273", 3))


if __name__ == "__main__":
    main()
