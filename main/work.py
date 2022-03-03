import os, sys, time;

from threading import Thread

os.environ['ROOT'] = "/home/well/projects/borg/";
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
                print(os.environ['ROOT'] + "/.client/.ssh/public_" + ip['ip'] + ".pem");
                if os.path.exists(os.environ['ROOT'] + "/.client/.ssh/public_" + ip['ip'] + ".pem"):
                    print("Chegou como resposta: ", borg_request(ip["ip"], ip["port"] + 1, "HELLO", "0001", "HELLO")[0]);
        time.sleep(10);

Thread(target=thread_load_config).start();
Thread(target=thread_mestre     ).start();


