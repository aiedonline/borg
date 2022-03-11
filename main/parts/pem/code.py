import json, os, sys, traceback, socket;

os.environ['SSHC'] = os.environ['ROOT'] + "/.client";
os.environ['SSHS'] = os.environ['ROOT'] + "/.server";

sys.path.insert(0, os.environ['ROOT']);

from threading import Thread;
from api.sock_util import *;

class BorgPem():
    def __init__(self, CONFIG):
        super().__init__(CONFIG, "pem");
    
#    def run(self):
#        while True:
#            try:
#                (clientsocket, address) = self.serversocket.accept();
#                thread = Thread(target = self.trade_pem_server, args = (clientsocket, address, ));
#                thread.start();
#            except KeyboardInterrupt:
#                print( 'Interrupted');
#                sys.exit(0);
#            except:
#                traceback.print_exc();  
#    
#    def trade_pem_server(self, sock, address):
#        address = address[0];
#        # recebimento do PEM
#        expected_size = b""
#        while len(expected_size) < 8:
#            more_size = sock.recv(8 - len(expected_size))
#            if not more_size:
#                raise Exception("Short file length received")
#            expected_size += more_size
#        expected_size = int.from_bytes(expected_size, 'big')
#        packet = b""
#        while len(packet) < expected_size:
#            buffer = sock.recv(expected_size - len(packet))
#            if not buffer:
#                raise Exception("Incomplete file received")
#            packet += buffer
#        with open(os.environ['SSHS'] + "/.ssh/public_" + address + ".pem", 'wb') as f:
#            f.write(packet)
#        #envio de PEM
#        with open( os.environ['SSHS'] + "/.ssh/public_borg.pem", 'rb') as f:
#            raw = f.read();
#        sock.sendall(len(raw).to_bytes(8, 'big'))
#        sock.sendall(raw)

#if __name__ == "__main__":
try:
    print("iniciando ");
    CONFIG = json.loads(open(os.environ['ROOT'] + "/data/server/config.json", "r").read());
    BorgPem(CONFIG);
except KeyboardInterrupt:
    print( 'Interrupted');
    sys.exit(0);
except:
    traceback.print_exc();

