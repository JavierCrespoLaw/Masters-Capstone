import socket

DATABASE = socket.gethostbyname(socket.gethostname())
DATABASE_PORT = 5051
DATABASE_ADDR = (DATABASE, DATABASE_PORT)

database = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
database.connect(DATABASE_ADDR)



