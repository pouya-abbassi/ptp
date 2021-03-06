import rsa
from multiprocessing import cpu_count

class Client():
    def __init__(self, size=2048, pool=cpu_count()):
        try:    #try to use existing key
            with open('client-pubkey.pem', 'rb') as pubfile:
                keydata = pubfile.read()
                self.pubkey = rsa.PublicKey.load_pkcs1(keydata)
            with open('client-privkey.pem', 'rb') as privfile:
                keydata = privfile.read()
                self.privkey = rsa.PrivateKey.load_pkcs1(keydata)
        except: #if not possible, create new pair
            (self.pubkey, self.privkey) = rsa.newkeys(size, poolsize=pool)
            with open('client-pubkey.pem', 'wb') as pubfile:
                pubfile.write(rsa.PublicKey.save_pkcs1(self.pubkey))
                pubfile.close()
            with open('client-privkey.pem', 'wb') as privfile:
                privfile.write(rsa.PrivateKey.save_pkcs1(self.privkey))
                privfile.close()
        try:    #try to use existing server key
            with open('server-pubkey.pem', 'rb') as pubfile:
                keydata = pubfile.read()
                self.other = rsa.PublicKey.load_pkcs1(keydata)
        except: #create server key
            from server import Server
            Server()
            with open('server-pubkey.pem', 'rb') as pubfile:
                keydata = pubfile.read()
                self.other = rsa.PublicKey.load_pkcs1(keydata)
        return None

    def encrypt(self, message):
        '''Encrypt data using other part's RSA public key'''
        message = message.encode('utf8')
        crypto = rsa.encrypt(message, self.other)
        return crypto

    def decrypt(self, crypto):
        '''Decrypt data using our RSA private key'''
        message = rsa.decrypt(crypto, self.privkey)
        return message
