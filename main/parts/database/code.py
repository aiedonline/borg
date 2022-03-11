import json, os, sys, traceback, socket;

os.environ['ROOT'] = "/home/well/projects/borg/";
os.environ['SSHC'] = os.environ['ROOT'] + "/.client";
os.environ['SSHS'] = os.environ['ROOT'] + "/.server";

sys.path.insert(0, os.environ['ROOT']);

from threading import Thread;
from api.sock_util import *;

class BorgDatabase():
    def __init__(self, CONFIG):
        super().__init__(CONFIG, "database");
    
try:
    CONFIG = json.loads(open(os.environ['ROOT'] + "/data/server/config.json", "r").read());
    BorgDatabase(CONFIG);
except KeyboardInterrupt:
    print( 'Interrupted');
    sys.exit(0);
except:
    traceback.print_exc();
