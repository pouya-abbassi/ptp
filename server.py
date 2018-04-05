import rsa
from multiprocessing import cpu_count

class Server():
    def __init__(self, size=2048, pool=cpu_count()):
        try:    #try to use existing key
            with open('server-pubkey.pem', 'rb') as pubfile:
                keydata = pubfile.read()
                self.pubkey = rsa.PublicKey.load_pkcs1(keydata)
            with open('server-privkey.pem', 'rb') as privfile:
                keydata = privfile.read()
                self.privkey = rsa.PrivateKey.load_pkcs1(keydata)
        except: #if not possible, create new pair
            (self.pubkey, self.privkey) = rsa.newkeys(size, poolsize=pool)
            with open('server-pubkey.pem', 'wb') as pubfile:
                pubfile.write(rsa.PublicKey.save_pkcs1(self.pubkey))
                pubfile.close()
            with open('server-privkey.pem', 'wb') as privfile:
                privfile.write(rsa.PrivateKey.save_pkcs1(self.privkey))
                privfile.close()
        try:    #try to use existing server key
            with open('client-pubkey.pem', 'rb') as pubfile:
                keydata = pubfile.read()
                self.other = rsa.PublicKey.load_pkcs1(keydata)
        except: #create new server key
            from client import Client
            Client()
            with open('client-pubkey.pem', 'rb') as pubfile:
                keydata = pubfile.read()
                self.other = rsa.PublicKey.load_pkcs1(keydata)
        return None

    def encrypt(self, message):
        '''Encrypt data using other part's RSA public key'''
        message = message
        crypto = rsa.encrypt(message, self.other)
        return crypto

    def decrypt(self, crypto):
        '''Decrypt data using our RSA private key'''
        message = rsa.decrypt(crypto, self.privkey)
        return message
