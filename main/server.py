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








#CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#ROOT = os.path.dirname(CURRENTDIR);
#sys.path.insert(0,ROOT);

#from threading import stack_size
#stack_size(32*1024)

#from threading import Thread
#from api.iplist import *;
#from api.localjson import *;
#from api.log import *;

#class BorgServer(Thread):
#    def __init__ (self, ROOT, MACHINE):
#        Thread.__init__(self);
#        self.process_child = {};
#        self.ROOT = ROOT;
#        self.MACHINE = MACHINE;
#        self.CONFIG = json.loads(open(ROOT + "/data/server/config.json", "r").read());
#        #self.MODULES = LocalJson(ROOT + "/data/modules.json");
#        if self.CONFIG.get("uuid") == None:
#            self.CONFIG['uuid'] = str(uuid.uuid4())[:8];
#            f = open(ROOT + "/data/server/config.json", "w");
#            f.write(json.dumps(self.CONFIG));
#            f.close();
#    
#    #def sair_seguro(self, *args):
#    #    self.MODULES.setAll("active", False);
#        
#    def porprocesso(self, key, script):
#        CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
#        if os.path.exists(CURRENTDIR + "/parts/"+ key +"/code.py") == False:
#            print("Não possui code.py em:", key);
#            return;
#        if os.path.exists(CURRENTDIR + "/parts/"+ key +"/config.json") == False:
#            print("Não possui um config.json em ", key);
#            return;
#        
#        modulo = LocalJson(CURRENTDIR + "/parts/"+ key +"/config.json");
#        while True:
#            try:
#                if modulo.get("active") == False:
#                    time.sleep(30);
#                    continue;
#                #if self.MODULES.has(key) == False:
#                #    print("A key não existe como módulo: ", key ,".");
#                #    time.sleep(30);
#                #    continue;
#                print('\033[92m', "Processo: ", modulo.get("port"), '\033[0m', script);
#                if os.path.exists("/tmp/"+ key +"_stdout.txt") == True:
#                    os.unlink("/tmp/"+ key +"_stdout.txt");
#                if os.path.exists("/tmp/"+ key +"_stderr.txt") == True:
#                    os.unlink("/tmp/"+ key +"_stderr.txt");
#                print("antes de brir arquivos");
#                with open("/tmp/"+ key +"_stdout.txt","wb") as out, open("/tmp/"+ key +"_stderr.txt","wb") as err:
#                    p = subprocess.Popen(args=["python3", script], stdout=out, stdin=subprocess.PIPE, stderr=err);
#                    #self.MODULES.set(key + ".active", True);
#                    if self.process_child.get(key) == None:
#                        self.process_child[key] = {};
#                    self.process_child[key]['process'] = p;
#                    self.process_child[key]['hash'] = hashlib.md5(open(script).read().encode()).hexdigest();
#                    self.process_child[key]['path'] = script;
#                    #Log.send("Iniciando: " + script, "INFO");
#                    p.communicate();
#                print('\033[1m', "Parou em: ", key, '\033[0m' ,":\n" ,  '\033[93m' + open("/tmp/"+ key +"_stdout.txt").read() + '\033[0m' + "\n" + '\033[91m' + open("/tmp/"+ key +"_stderr.txt").read() + '\033[0m');
#                self.process_child[key]['process'] = None;
#                #os._exit(1);
#            except KeyboardInterrupt:
#                print( 'Interrupted');
#                sys.exit(0);
#            except:
#                traceback.print_exc();
#                Log.send(traceback.format_exc());
#                
#            time.sleep(5);
#    def thread_monitora_mudanca(self):
#        time.sleep(60);
#        while True:
#            try:
#                keys = self.process_child.keys() ;
#                for key in  keys:
#                    value = self.process_child[key];
#                    if value['process'] != None and value['hash'] != None and value['path'] != None :
#                        modulo = LocalJson(ROOT + "/main/parts/"+ key +"/config.json");
#                        if modulo.get("active") == False:
#                            value['process'].terminate();
#                        if value['hash'] != hashlib.md5(open(value['path']).read().encode()).hexdigest():
#                            time.sleep(180);
#                            Log.send("Parando: " + key, "INFO");
#                            value['process'].terminate();
#            except KeyboardInterrupt:
#                print( 'Interrupted');
#                sys.exit(0);
#            except:
#                Log.send(traceback.format_exc());
#                traceback.print_exc();
#            time.sleep(60);
#    def run(self):
#        CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#        lista = os.listdir(CURRENTDIR + "/parts/");
#        for elemento in lista:
#            try:
#                if os.path.isdir(CURRENTDIR + "/parts/" + elemento):
#                    thread = Thread(target = self.porprocesso, args = (elemento, CURRENTDIR + "/parts/" + elemento + "/code.py" , ));
#                    thread.start();
#            except KeyboardInterrupt:
#                print( 'Interrupted');
#                sys.exit(0);
#            except:
#                Log.send(traceback.format_exc());
#                traceback.print_exc();
#                exit(1);
#        # TREAD QUE MONITORA
        
#        thread5 = Thread(target = self.thread_monitora_mudanca, args = ());
#        thread5.start();
#    def __del__(self):
#        print('finalizando....');
#  
    

    
    
    

    

