import json, os, sys, traceback, socket;

os.environ['SSHC'] = os.environ['ROOT'] + "/.client";
os.environ['SSHS'] = os.environ['ROOT'] + "/.server";

sys.path.insert(0, os.environ['ROOT']);

from threading import Thread;
from api.sock_util import *;
from main.parts.service import *;

class BorgBase(Service):
    def __init__(self, CONFIG):
        super().__init__(CONFIG, "base");
    
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
