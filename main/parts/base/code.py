import json, os, sys, traceback, socket;

os.environ['SSHC'] = os.environ['ROOT'] + "/.client";
os.environ['SSHS'] = os.environ['ROOT'] + "/.server";

sys.path.insert(0, os.environ['ROOT']);

from threading import Thread;
from api.sock_util import *;
from main.parts.service import *;

class BorgBase(Service):
    def __init__(self, CONFIG):
        self.CONFIG = CONFIG;
        self.LOCAL = json.loads(open(os.environ['ROOT'] + "/main/parts/base/config.json").read());
        print("...::: Módulo BASE :::....:" , self.CONFIG['port'] + self.LOCAL["port"]);
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
    
    def dispacher_HELLO(self, clientsocket, address):
        protocol = "HELLO"; version = "111";
        borg_response(clientsocket, address, protocol, version, "OLAAMIGO");
        
    
try:
    CONFIG = json.loads(open(os.environ['ROOT'] + "/data/server/config.json", "r").read());
    BorgBase(CONFIG);
except KeyboardInterrupt:
    print( 'Interrupted');
    sys.exit(0);
except:
    traceback.print_exc();




#import time, os, socket, traceback, json, sys, inspect;
#import subprocess

#CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENTDIR)));
#sys.path.insert(0,ROOT);

#from threading import stack_size
##stack_size(64*1024)

#from api.socketUtil_base import *;
#from api.localjson import *;
#from api.log import *;
#from main.parts.processbase import *;
#from threading import Thread

#PORT_NUMBER = 3;
#
#class BorgBase(ProcessBase):
#    def __init__(self, CONFIG):
#        super().__init__();
#        print("...::: Módulo BASE :::....");
#        self.CONFIG = CONFIG;
#        self.request_count = 0;
#        self.LOCAL = json.loads(open(CURRENTDIR + "/config.json").read());
#        self.concorrentes = 0;
#        # info
#        #self.INFO = LocalJson(CURRENTDIR + "/info.json", interval_save=60, interval_load=60); self.INFO.set("start", datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'));
#        try:
#            self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
#            self.serversocket.bind(('0.0.0.0', self.CONFIG['port'] + self.LOCAL.get("port")));
#            self.serversocket.listen(1500);
#        except KeyboardInterrupt:
#            print( 'Interrupted');
#            sys.exit(0);
#        except:
#            Log.send(traceback.format_exc());
#            traceback.print_exc();
#            sys.stdout.write("Falha ao abrir portas.")
#            os._exit(1);
#    
#    def run(self):
#        while True:
#            try:
#                (clientsocket, address) = self.serversocket.accept();
#                thread = Thread(target = self.dispacher, args = (clientsocket, ));
#                thread.start();
#            except KeyboardInterrupt:
#                print( 'Interrupted');
#                sys.exit(0);
#            except:
#                Log.send(traceback.format_exc());
#                traceback.print_exc();   
#    def dispacher(self, clientsocket):
#        (protocol, version, length, body, uuid) = readSocket(clientsocket, "S");
#        print(protocol);
#        self.request_count = self.request_count + 1;
#        self.concorrentes += 1;
#        try:
#            if protocol != None:
#                #self.INFO.incrase(protocol);
#                #self.INFO.incrase(uuid);
#                    
#                if protocol == 'HELLO':
#                    self.thread_hello(clientsocket,version, length, body, uuid);
#                    #thread = Thread(target = self.thread_hello, args = (clientsocket,version, length, body, uuid, ));
#                    #thread.start();
#                elif protocol == 'INFON':
#                    self.thread_nos(clientsocket,version, length, body, uuid);
#                    #thread = Thread(target = self.thread_nos, args = (clientsocket,version, length, body, uuid, ));
#                    #thread.start();                   
#        except KeyboardInterrupt:
#            print( 'Interrupted');
#            sys.exit(0);
#        except:
#            Log.send(traceback.format_exc());
#            traceback.print_exc();
#    
#    def thread_hello(self, clientsocket, version, length, body, uuid_outro, ):
#        try:
#            writeSocket(clientsocket, "HELLO", "1", open(ROOT + "/data/machines.json").read(), uuid=self.CONFIG['uuid']);
#        except KeyboardInterrupt:
#            print('Interrupted');
#            sys.exit(0);
#        except:
#            Log.send(traceback.format_exc());
#            traceback.print_exc();#
#
#    def thread_nos(self, clientsocket, version, length, body, uuid_outro, ):
#        try:
#            buffer = json.loads(open(ROOT + "/data/machines.json").read());
#            for elemento in buffer['elements']:
#                elemento["ip"] = "0.0.0.0";
#            writeSocket(clientsocket, "INFON", "1", json.dumps(buffer), uuid=self.CONFIG['uuid']);
#        except KeyboardInterrupt:
#            print( 'Interrupted');
#            sys.exit(0);
#        except:
#            Log.send(traceback.format_exc());
#            traceback.print_exc();
#    def __del__(self):
#        self.serversocket.close();
#try:
#    CONFIG = json.loads(open(ROOT + "/data/server/config.json", "r").read());
#    print("CONFIG: ", CONFIG);
#    codigo = BorgBase(CONFIG);
#    codigo.run();
#except KeyboardInterrupt:
#    print( 'Interrupted');
#    sys.exit(0);
#except:
#    Log.send(traceback.format_exc());
#    traceback.print_exc();

