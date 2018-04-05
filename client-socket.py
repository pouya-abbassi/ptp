import socket
from server import Server
from client import Client

client = Client(3072)

HOST = 'localhost'
PORT = 8080
i = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    crypto = client.encrypt('hello ' + str(i))
    s.sendall(crypto)
    data = s.recv(1024*100)
    data = client.decrypt(data)
    print('Recieved:')
    print(data.decode())
    i += 1
