# -*- coding: utf-8 -*-
import socket, signal, json, os, time, datetime, traceback, sys, inspect, unicodedata, miniupnpc, hashlib, uuid, importlib, importlib.util, subprocess;
import time;

sys.path.insert(0, os.environ['ROOT']);

from api.process import *;
from main.server_part import *;

class BorgServer():
    def __init__ (self):
        self.CONFIG = json.loads(open(os.environ['ROOT'] + "/data/server/config.json", "r").read());

    def __load_part(self, path):
        p = Part(path);
        p.start();
    
    def run(self):
        lista = os.listdir(os.environ['ROOT'] + "/main/parts/");
        for elemento in lista:
            try:
                if os.path.isdir(os.environ['ROOT'] + "/main/parts/" + elemento):
                    p = Part(os.environ['ROOT'] + "/main/parts/"+ elemento);
            except KeyboardInterrupt:
                print( 'Interrupted');
                sys.exit(0);
            except:
                traceback.print_exc();
                exit(1);    


#if __name__ =="__main__":
b = BorgServer();
b.run();




