from ast import arg
import os, sys, time, uuid;
from threading import Thread

os.environ['ROOT'] = "/opt/borg"; #os.path.abspath("./");
os.environ['SSHC'] = os.environ['ROOT'] + "/.client";
os.environ['SSHS'] = os.environ['ROOT'] + "/.server";

ROOT = os.environ['ROOT'];
sys.path.insert(0,ROOT);

from api.sock_util import *;
from api.process import *;

CONFIG = None;

# ----------------------------------- CARREGANDO CONFIGURAÇÀO A CADA 60 SEGUNDOS
def thread_load_config():
    global CONFIG;
    while True:
        try:
            CONFIG =  json.loads(open( os.environ['ROOT'] + "/data/client/config.json" ).read());
            # Atualizar chaves de criptografia
            for ip in CONFIG["ips"]:
                if not ip['active']:
                    continue;
                trade_pem_client( ip["ip"], ip["port"]  );
        except:
            time.sleep(5);
        time.sleep(60);

# ---------------------------------- TRABALHADORES ---------------
def thread_work(work, mq):
    # {"id": "", "group_id": "hello", "queue_id": "hellocrawler", "queue_step_id": "hellocrawler1", "input": "{}", "err": null, "output": null, "status_code": null, "execute_in": "2022-03-08 11:54:36"}
    try:
        print("Sscript: ", ROOT + "/tmp/project/" +  work['script']);
        p = Process(ROOT + "/tmp/project/" +  work['script'], time_to_life=5,  interpreter="python3", required=[]);
        print("chamando.....");
        p.start(data_in=work);
        print("Retorno do processo: ", p.status_code);
        if p.status_code == 0:
            mq.next(work["id"], work["next"], p.out);
        else:
            raise Exception('Status do projeto é diferente de zero.');
    except:
        mq.err(work["id"], p.status_code,  p.out, p.err ); 

def thread_master(ip):
    mq = None;
    try:
        mq = MQ(ip["ip"], ip["port"]);
        while True:
            buffer_works = mq.haswork();
            threads = [];
            if len(buffer_works) > 0:
                threads_work = [];
                #WORK: ('[{"id": "837cae6d-4e49-440d-84d7-f614491918b6", "group_id": "hello", "queue_id": "hellocrawler", "queue_step_id": "hellocrawler1", "input": "{}", "err": null, "output": null, "status_code": null, "execute_in": "2022-03-08 11:54:36"}]', '111', '222', 'HASWO', '000', '88888888', '7777777', '00000000000023')
                for buffer_work in buffer_works:
                    b = Base(ip["ip"], ip["port"]);
                    b.project_update([buffer_work['group_id']]);
                    t = Thread(target=thread_work, args=(buffer_work, mq, ));
                    threads.append(t);
                    t.start();
                for t in threads:
                    t.join();
    finally:
        mq = None;

def thread_server():
    global CONFIG;
    while True:
        if CONFIG != None:
            threads_server = [];
            for ip in CONFIG["ips"]:
                if not ip['active']:
                    continue;
                print("IP:", ip['ip']);
                if os.path.exists(os.environ['ROOT'] + "/.client/.ssh/public_" + ip['ip'] + ".pem"):
                    t = Thread(target=thread_master, args=(ip,));
                    t.start();
                    threads_server.append(t);
            for t in threads_server:
                t.join(); # Aguardar resposta.......
        time.sleep(10);

class BorgCommuniction():
    def __init__(self, ip, port):
        self.ip = ip;
        self.port = port;
        self.key = None;
        self.session_id = None;
        self.keynew();
    def __del__(self):
        borg_request_raw(self.ip, self.port, "KEYCL", "000", json.dumps({"session_id" : self.session_id}));
    def keynew(self):
        retorno = borg_request_raw(self.ip, self.port, "KEYNW" , "000", "{}");
        # ('{"session_id": "fbd5e380-1db7-40fc-8318-b8cca66b888f", "key": "371abf0a-1953-4398-a8af-dca575a7a811"}', '111', '222', 'KEYNW', '000', '88888888', '7777777', '00000000000010')
        retorno = json.loads(retorno[0]);
        self.key = retorno["key"];
        self.session_id = retorno["session_id"];
        
    def request(self, protocol, protocol_version,  data, type="raw"):
        if type == "raw":
            return json.loads( borg_request_raw(self.ip, self.port, protocol, protocol_version, json.dumps(data))[0] );
        #elif type == "aes":
        #    return borg_request_aes(self.ip, self.port, protocol, protocol_version, json.dumps(data));
        elif type == "rsa":
            return borg_request_rsa(self.ip, self.port, protocol, protocol_version, json.dumps(data));

class Base(BorgCommuniction):
    def __init__(self, ip, start_port):
        super().__init__(ip, start_port + 1);
    
    def file_update(self, file, md5):
        hash_file = None;
        if os.path.exists(ROOT + "/tmp/" + file):
            hash_file = hashlib.md5( open(ROOT + "/tmp/" + file).read().encode() ).hexdigest();
        if md5 != hash_file:
            path_dir = ROOT + "/tmp/" + file[ : file.rfind("/") ];
            if not os.path.exists(path_dir):
                os.makedirs(path_dir);
            with open( ROOT + "/tmp/" + file ,"w") as f:
                print('Será baixado: ', "/tmp/" + file);
                f.write(self.get_file(file));
                f.close();
    def get_file(self, file ):
        return self.request("GETFI", "000",  {"file" : file}, type="raw")['file'];
    
    def project_update(self, project_name ):
        files = self.request("PROFI", "000",  {"name" : project_name}, type="raw");
        for file in files:
            self.file_update(file['file'], file['md5']);
        return files;
    
class MQ(BorgCommuniction):
    def __init__(self, ip, start_port):
        super().__init__(ip, start_port + 3);
    def register(self, group_name, queue_name, queue_step_name, input, execute_in, id="", flag="" ):
        input = json.dumps(input);
        return self.request("REGIS", "000",  {"id" : id , "group_name" : group_name, "queue_name" : queue_name, "queue_step_name" : queue_step_name, "input" : input, "execute_in" : execute_in, "flag" : flag}, type="raw");
    def haswork(self):
        # ('[{"id": "", "group_id": "", "queue_id": "", "queue_step_id": "", "input": "{}", "status_code": null, "name": "list", "next": "hellocrawler2", "script": "/hello/list.py", "need": "[]", "active": 1, "interpreter": "python3"}]', '111', '222', 'HASWO', '000', '88888888', '7777777', '00000000000028')
        works = json.loads(  open(os.environ['ROOT'] + "/data/client/config.json").read());
        return self.request("HASWO", "000",  {"id" : str(uuid.uuid4()) , "groups" : works["mq"]["groups"]}, type="raw");
    def next(self, work_id, queue_step_id, stdout):
        print("Next: ", work_id);
        return self.request("NEXTW", "000",  {"id" : work_id, "stdout" : stdout, "queue_step_id" : queue_step_id}, type="raw");
    def err(self, work_id, status_code, stdout, sterr):
        return self.request("ERRWO", "000",  {"id" : work_id,  "status_code" : status_code,  "stdout" : stdout, "sterr" : sterr}, type="raw");

Thread(target=thread_load_config).start();
Thread(target=thread_server     ).start();

#ba = Base("127.0.0.1", 8080);
#print(ba.project_update(["hello"]));


#mq = MQ("127.0.0.1", 8080);
#print(mq.register("hello", "Hello Crawler", "list", {}, "2000-01-01 00:00:00"));
#works = mq.haswork();
#print(works);
#for work in works:
#    mq.next(work['id'], work['next'], "");

