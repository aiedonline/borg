import os, sys, time, uuid
from pickle import GLOBAL;
from threading import Thread

os.environ['ROOT'] = "/opt/borg"; #os.path.abspath("./");
os.environ['SSHC'] = os.environ['ROOT'] + "/.client";
os.environ['SSHS'] = os.environ['ROOT'] + "/.server";


ROOT = os.environ['ROOT'];
sys.path.insert(0,ROOT);

from api.sock_util import *;
from api.process import *;
from api.clienthelper import *;

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
def thread_work(work, mq, ip):
    # {"id": "", "group_id": "hello", "queue_id": "hellocrawler", "queue_step_id": "hellocrawler1", "input": "{}", "err": null, "output": null, "status_code": null, "execute_in": "2022-03-08 11:54:36"}
    try:
        print("Script: ", ROOT + "/tmp/project/" +  work['script']);
        p = Process(ROOT + "/tmp/project/" +  work['script'], time_to_life=5,  interpreter="python3", required=[]);
        p.start(data_in={ "work" : work, "config" : ip});
        if p.status_code == 0:
            mq.next(work["id"], work["next"], p.out);
        else:
            print(p.out, p.err);
            print("Status:" , p.status_code);
            p = None;
            time.sleep(60);
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
                    t = Thread(target=thread_work, args=(buffer_work, mq, ip,  ));
                    threads.append(t);
                    t.start();
                    t.join();
                #for t in threads:
                #    t.join();
            time.sleep(5);
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

Thread(target=thread_load_config).start();
Thread(target=thread_server     ).start();

#ba = Base("127.0.0.1", 8080);
#print(ba.project_update(["hello"]));

#print("hello");
#mq = MQ("127.0.0.1", 8080);
#print(mq.register("hello", "Hello Crawler", "list", {}, "2000-01-01 00:00:00"));
#works = mq.haswork();
#print(works);
#for work in works:
#    mq.next(work['id'], work['next'], "");

#db = Database("127.0.0.1", 8080);
#print(db.write("hello", "hello",  ["id"], [ datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') ], ["value1", "value2"], ["aaaa", "bbbbb"]));
