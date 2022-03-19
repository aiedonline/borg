#!/usr/bin/python3
# /opt/borg/api/blowfishhelper.py
# Parte do código do projeto BORG

import base64;

from Crypto.Cipher import Blowfish
from struct import pack
from Crypto.Random import get_random_bytes;
from base64 import b64encode, b64decode;

class BlowfishHelper():
    def __init__(self, key=None):
        if key == None:
            key = get_random_bytes(32);
        self.key = key;
        self.bs = Blowfish.block_size;
    def encrypt(self, message):
        message = message.encode("utf-8");
        cipher = Blowfish.new(self.key, Blowfish.MODE_CBC);
        plen = self.bs - len(message) % self.bs;
        padding = [plen]*plen;
        padding = pack('b'*plen, *padding);
        msg = cipher.iv + cipher.encrypt(message + padding);
        return base64.b64encode( msg ).decode('utf-8');

    def decrypt(self, message):
        ciphertext = base64.b64decode( message );
        iv = ciphertext[:self.bs];
        ciphertext = ciphertext[self.bs:];
        cipher = Blowfish.new(self.key, Blowfish.MODE_CBC, iv);
        msg = cipher.decrypt(ciphertext)

        last_byte = msg[-1]
        msg = msg[:- (last_byte if type(last_byte) is int else ord(last_byte))]
        return msg.decode("utf-8");

#if __name__ == "__main__":
#    b = BlowfishHelper();
#    text = "Acesse o canal aiedonline no Youtube!!!"
#    encrypted = b.encrypt(text);
#    decrypted = b.decrypt(encrypted);
#    print("Texto:     ", text);
#    print("Encripted: ", encrypted);
#    print("Decripted: ", decrypted);
