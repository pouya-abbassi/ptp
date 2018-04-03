from server import Server
from client import Client

def mosi(message):
    '''mosi: Master Out Slave In
    Name came from electronic SPI interface'''
    crypto = server.encrypt(message)
    message = client.decrypt(crypto)
    return crypto, message

def miso(message):
    '''miso: Master In Slave Out
    Name came from electronic SPI interface'''
    crypto = client.encrypt(message)
    message = server.decrypt(crypto)
    return crypto, message

server = Server(3072)
client = Client(3072)

print(mosi('hello'))
print(miso('hello'))
