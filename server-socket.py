import socket
from server import Server

server = Server(3072)

HOST = ''
PORT = 8080
i = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
while True:
    data = conn.recv(1024*100)
    if not data: break
    data = server.decrypt(data)
    crypto = server.encrypt(data)
    conn.sendall(crypto)
    i += 1
