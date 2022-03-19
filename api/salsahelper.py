#!/usr/bin/python3
# /opt/borg/api/salsahelper.py
# Parte do código do projeto BORG

import base64;

from Crypto.Cipher import Salsa20;
from Crypto.Random import get_random_bytes;

class SalsaHelper():
    def __init__(self, key=None):
        if key == None:
            self.key = get_random_bytes(32);
        else:
            self.key = key;
    def encrypt(self, message):
        cipher = Salsa20.new(key=self.key);
        msg = cipher.nonce + cipher.encrypt(message.encode("utf-8"));
        return base64.b64encode( msg ).decode("utf-8");
    
    def decrypt(self, message):
        msg = base64.b64decode(message.encode("utf-8"));
        msg_nonce = msg[:8];
        ciphertext = msg[8:];
        cipher = Salsa20.new(key=self.key, nonce=msg_nonce);
        return cipher.decrypt(ciphertext).decode("utf-8");

#if __name__ == "__main__":
#    s = SalsaHelper();
#    text = "AIED é muito bom, o melhor canal!!!";
#    encrypted = s.encrypt(text);
#    decrypted = s.decrypt(encrypted);
#    print("Text:      ", text     );
#    print("Encrypted: ", encrypted);
#    print("Decrypted: ", decrypted);
