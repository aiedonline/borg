import hashlib, subprocess, json, time, signal, os, sys;
from threading import Thread;

class Process():
    def __init__(self, path, time_to_life=0, interpreter="python3", required=[]):
        self.path = path;
        self.time_to_life = time_to_life;
        self.interpreter = interpreter;
        self.process_children = None;
        self.out = None; self.err = None;
        self.status_code = None;
        #for dependence in required:
        #    self.__install_dependence(dependence);
    
    def __kill_time_to_life(self):
        if self.time_to_life > 0:
            time.sleep(self.time_to_life);
            self.close();
    
    def start(self, data_in={}):
        process_key = hashlib.md5(self.path.encode()).hexdigest();
        thread = Thread(target = self.__kill_time_to_life, args = ());
        #self.process_children = subprocess.Popen(args=[self.interpreter, self.path],  stdout=subprocess.PIPE, stdin=subprocess.PIPE);
        self.process_children = subprocess.Popen(args=[self.interpreter, self.path], stdin=subprocess.PIPE);
        thread.start();
        p_out = self.process_children.communicate(input=(json.dumps( data_in ) + "\n").encode('utf-8'));
        if p_out[0] != None:
            self.out = str(p_out[0], 'utf-8');
        if p_out[1] != None:
            self.err = str(p_out[1], 'utf-8');
        if self.process_children != None:
            self.status_code = self.process_children.returncode;
            #if self.process_children.returncode != 0:
            #    print(self.out, "\033[91m", self.err, "\033[0m");
            #if p_out[1].strip() :
            #    err.write(self.err);
            #    err.close();
            #if p_out[0].strip() :
            #    out.write(self.out);
            #    out.close();
    def close(self):
        self.process_children.kill();
        try:
            os.kill(self.process_children.pid, signal.SIGINT);
            self.process_children = None;
        except:
            stderr = 1;
    
    def __install_dependence(self, dependence):
        sub = subprocess.run([self.interpreter, os.environ['ROOT'] + "/main/api/process_module_exists.py", dependence['name']]);
        print(sub.returncode);
        if sub.returncode != 0:
            print("[*] Install: ",  dependence['install']);
            subprocess.run([self.interpreter, "-m", "pip", "install", dependence['install']]);



