import os, sys, time, uuid;

from threading import Thread

os.environ['ROOT'] = "/opt/borg"; #os.path.abspath("./");
os.environ['SSHC'] = os.environ['ROOT'] + "/.client";
os.environ['SSHS'] = os.environ['ROOT'] + "/.server";
ROOT = os.environ['ROOT'];
sys.path.insert(0,ROOT);

from api.sock_util import *;

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
def thread_mestre():
    global CONFIG;
    while True:
        if CONFIG != None:
            for ip in CONFIG["ips"]:
                if not ip['active']:
                    continue;
                print("IP:", ip['ip']);
                if os.path.exists(os.environ['ROOT'] + "/.client/.ssh/public_" + ip['ip'] + ".pem"):
                    mq = MQ(ip["ip"], ip["port"]);
                    works = mq.haswork();
                    print(works);
                    #print("Chegou como resposta: ", borg_request(ip["ip"], ip["port"] + 1, "HELLO", "222", "HELLO")[0]);
        time.sleep(10);

class BorgCommuniction():
    def __init__(self, ip, port):
        self.ip = ip;
        self.port = port;
    def request(self, protocol, protocol_version,  data):
        print(self.ip, self.port);
        return borg_request(self.ip, self.port, protocol, protocol_version, json.dumps(data));

class MQ(BorgCommuniction):
    def __init_(self, ip, start_port):
        self.__super.__init__(ip, start_port + 3);
    def register(self, group_name, queue_name, queue_step_name, input, execute_in, id="", flag="" ):
        input = json.dumps(input);
        return self.request("REGIS", "000",  {"id" : id , "group_name" : group_name, "queue_name" : queue_name, "queue_step_name" : queue_step_name, "input" : input, "execute_in" : execute_in, "flag" : flag});
    def haswork(self):
        works = json.loads(  open(os.environ['ROOT'] + "/data/client/config.json").read());
        print(works["mq"]["groups"]);
        return self.request("HASWO", "000",  {"id" : str(uuid.uuid4()) , "groups" : works["mq"]["groups"]});

#Thread(target=thread_load_config).start();
#Thread(target=thread_mestre     ).start();

mq = MQ("127.0.0.1", 8083);
#print(mq.register("hello", "Hello Crawler", "list", {}, "2000-01-01 00:00:00"));
print(mq.haswork());


