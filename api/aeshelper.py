import os, uuid, random, base64;
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes;

class AesHelper:
    def __init__(self, key=None, iv=None):
        if key == None:
            self.key = os.urandom(32);
        if iv == None:
            self.iv = os.urandom(16);
        self.cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv));
    def encrypt(self, mensagem):
        mensagem = base64.b64encode(mensagem.encode()).decode();
        for i in range( 16 - (len(mensagem)  % 16) ):
            mensagem += " ";
        encryptor = self.cipher.encryptor();
        return encryptor.update(mensagem.encode("utf-8")) + encryptor.finalize();
    def decrypt(self, message):
        decryptor = self.cipher.decryptor();
        return  base64.b64decode( (decryptor.update(message) + decryptor.finalize()) ).decode("utf-8").strip();

#ae = AesHelper();
#criptografado = ae.encrypt("Botafogo campeão, aeee textoooorrr");
#print(criptografado);
#print(ae.decrypt(criptografado));

