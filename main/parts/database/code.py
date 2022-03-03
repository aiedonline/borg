import json, os, sys, traceback, socket;

os.environ['ROOT'] = "/home/well/projects/borg/";
os.environ['SSHC'] = os.environ['ROOT'] + "/.client";
os.environ['SSHS'] = os.environ['ROOT'] + "/.server";

sys.path.insert(0, os.environ['ROOT']);

from threading import Thread;
from api.sock_util import *;

class BorgDatabase():
    def __init__(self, CONFIG):
        self.CONFIG = CONFIG;
        self.LOCAL = json.loads(open(os.environ['ROOT'] + "/main/parts/database/config.json").read());
        print("...::: Módulo DATABASE :::....:" , self.CONFIG['port'] + self.LOCAL["port"]);
        try:
            self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            self.serversocket.bind(('0.0.0.0', self.CONFIG['port'] + self.LOCAL["port"]));
            self.serversocket.listen(1500);
            self.run();
        except KeyboardInterrupt:
            print( 'Interrupted');
            sys.exit(0);
        except:
            traceback.print_exc();
            sys.stdout.write("Falha ao abrir portas.")
            os._exit(1);
    
    def run(self):
        while True:
            try:
                (clientsocket, address) = self.serversocket.accept();
                Thread(target=self.dispacher, args=(clientsocket, address[0], )).start();
            except KeyboardInterrupt:
                print( 'Interrupted');
                sys.exit(0);
            except:
                traceback.print_exc();
    def dispacher(self, clientsocket, address):
        # ('6', '000', '000', '00AAA', '000', '10000000', '0000000', '00000000000000')
        server_data = borg_wait(clientsocket, address);
        class_method = getattr(self, "dispacher_" + server_data[3]);
        result = class_method(clientsocket, address );
    #def dispacher_HELLO(self, clientsocket, address):
    #    protocol = "HELLO"; version = "000";
    #    borg_response(clientsocket, address, protocol, version, "OLá amigo");
    
try:
    CONFIG = json.loads(open(os.environ['ROOT'] + "/data/server/config.json", "r").read());
    BorgDatabase(CONFIG);
except KeyboardInterrupt:
    print( 'Interrupted');
    sys.exit(0);
except:
    traceback.print_exc();
