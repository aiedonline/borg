#!/usr/bin/python3
# -*- coding: utf-8 -*-
from email.policy import default
import os, sys, time, inspect, json, datetime, hashlib, shutil, psutil, traceback;
import subprocess, argparse;

# sudo apt install python3-pip -y
# sudo apt-get install python-setuptools
# sudo apt-get install python3-lxml
# sudo apt install whois -y
# -----sudo python3 -m pip install --upgrade setuptools
# sudo python3 -m pip install netifaces
# sudo python3 -m pip install miniupnpc
# sudo python3 -m pip install tinydb
# sudo python3 -m pip install python-telegram-bot
# sudo python3 -m pip install psutil
# sudo python3 -m pip install requests
# sudo python3 -m pip install dnspython

from threading import Thread

os.environ['ROOT'] = os.path.abspath("./");
os.environ['SSHC'] = os.environ['ROOT'] + "/.client";
os.environ['SSHS'] = os.environ['ROOT'] + "/.server";

ROOT = os.environ['ROOT'];
sys.path.insert(0,ROOT);

from api.process import *;
from api.rsahelper import *;
#from main.work import BorgWork
#from main.server import BorgServer
#from api.socketUtil_info import *;
#from api.localjson import *;
#from api.log import *;
#MACHINE = LocalJson(ROOT + "/data/machines.json");

server_process = None;

ap = argparse.ArgumentParser();
ap.add_argument("-s", "--server", default=True,  const=True, nargs="?",  required=False, help="Ativar o servidor?");
ap.add_argument("-c", "--client", default=True,  const=True,  nargs="?", required=False, help="Ativar o cliente?");
ap.add_argument("-t", "--threads", default=5,    const=5,     nargs="?", required=False, help="Informe a quantidade de Threads");
args = vars(ap.parse_args())

try:
    rsa = RsaHelper(path_to_pem=os.environ['SSHS'], name_file_pem="borg.pem", create_private=True);
    if args["server"]:
        server_process = Process( os.environ["ROOT"] + "/main/server.py", time_to_life=0, 
                                    required=[{"name" : "netifaces", "install" : "netifaces"}]);
        server_process.start();
except:
    traceback.print_exc();
    if server_process != None:
        server_process.close();

#def prepare():
#    if os.path.exists(ROOT + "/database/telegram") == True:
#        shutil.rmtree(ROOT + "/database/telegram")
#    os.makedirs(ROOT + "/database/telegram");

#def infoborg(element):
#    global MACHINE;
#    time.sleep(30);

#def findBorg():
#    global MACHINE;
#    while True:
#        try:
#            if MACHINE != None and MACHINE.get("elements") != None:
#                for element in MACHINE.get("elements"):
#                    thread = Thread(target = infoborg, args = (element, ));
#                    thread.start(); 
#        except KeyboardInterrupt:
#            print( 'Interrupted');
#            sys.exit(0);
#        except:
#            Log.send(traceback.format_exc());
#            traceback.print_exc();
#        time.sleep(60);

#def recursivlefiles(path, files):
#    try:
#        lista = os.listdir(path);
#        for i in range(len(lista)):
#            try:
#                #if lista[i][:1] == ".":
#                #    continue;
#                if lista[i] == "__pycache__" or lista[i] == "info.json":
#                    continue;
#                if os.path.isdir(path + "/" + lista[i]):
#                    recursivlefiles(path + "/" + lista[i], files);
#                else:
#                    referencial = (path + "/" + lista[i])[len(ROOT):];
#                    files.append({"path" : referencial, "hash" : hashlib.md5(open(path + "/" + lista[i]).read().encode('utf-8')).hexdigest() });
#            except:
#                Log.send(traceback.format_exc() + " ao baixar <b>" + path + "/" + lista[i] + "</b>");
#                traceback.print_exc();
#    except:
#        traceback.print_exc();

#def replication():
#    global MACHINE; 
#    time.sleep(50); # aguardar ativar o serviço.
#    #print("Passar isso para um cliente....");
#    #queen = json.loads(open(ROOT + "/main/parts/replication/queen.json").read());
#    #config = LocalJson(ROOT + "/main/parts/replication/config.json");
#    #if not config.has("download") or config.get("download") == False:
#    #    print("Esta máquina não atualiza.");
#    #    return;
#    #while True:
#    #    try:
#    #        total = 0;
#    #        atualizados = "";
#    #        if os.path.exists(ROOT + "/main/parts/replication/config.json") == True:
#    #            me = LocalJson(ROOT + "/data/server/config.json");
#    #            files = [];
#    #            recursivlefiles(ROOT + "/api", files);
#    #            recursivlefiles(ROOT + "/data/server/mq", files);
#    #            recursivlefiles(ROOT + "/main", files);
#    #            recursivlefiles(ROOT + "/project", files);
#    #            for i in range(len(queen['web'])):
#    #                return_queen = writeHas(queen['web'][i]['url'], files, me.get('uuid') );
#    #                if return_queen != None:
#    #                    for j in range(len(return_queen)):
#    #                        file = writeDownload(queen['web'][i]['url'], return_queen[j]['path']);
#    #                        path_file = file['path'].strip();
#    #                        path_dir = path_file[:path_file.rfind("/")];
#    #                        if os.path.exists(ROOT + path_dir) == False:
#    #                            os.makedirs(ROOT + path_dir);
#    #                        if path_file.find("config.json") > 0:
#    #                            continue;
#    #                        if path_file.find("config.json") > 0 and os.path.exists(ROOT + path_file) == True:
#    #                            continue;
#    #                        print("Download: ", ROOT + path_file);
#    #                        with open( ROOT + path_file, "w" ) as f:
#    #                            f.write(file['data']);
#    #                            f.close();
#    #                            atualizados += " " + path_file;
#    #                            total +=1;
#    #        if total > 0:
#    #            Log.send("Arquivos atualizados: " + str(total) + ": " + atualizados, "INFO");
#    #    except KeyboardInterrupt:
#    #        print( 'Interrupted');
#    #        sys.exit(0);
#    #    except:
#    #        Log.send(traceback.format_exc());
#    #        traceback.print_exc();
#    #        os._exit(1);
#    #    time.sleep(120);

#def dados_processos():
#    while True:
#        try:
#            with open("/tmp/borg.out", "w") as f:
#                psutil.cpu_percent()
#                psutil.virtual_memory()
#                dict(psutil.virtual_memory()._asdict())
#                f.write("Threads: " + str(psutil.cpu_count() / psutil.cpu_count(logical=False)) + "\n");
#                f.write("Memória: " + str(psutil.virtual_memory().percent)+ "\n");
#                f.write("Memória available: " + str(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)+ "\n");
#
#                load1, load5, load15 = psutil.getloadavg();                    
#                cpu_usage = (load15/os.cpu_count()) * 100;
#                f.write("CPU: " + str(cpu_usage) + "\n")
#                
#                for proc in psutil.process_iter():
#                    try:
#                        if len(proc.cmdline()) < 2:
#                            continue;
#                        if proc.cmdline()[1].find("/borg/") < 0:
#                            continue;
#                        
#                        f.write(str(proc.num_threads()).ljust(10, " ") + proc.cmdline()[1].split("/")[-2].ljust(20, " ") + str(proc.memory_info().rss).ljust(10, " ") );
#                        proc.dict = proc.as_dict(['username', 'nice', 'memory_info', 'memory_percent', 'cpu_percent', 'cpu_times', 'name', 'status']);
#                        f.write(str(proc.dict['cpu_percent']) + "%\n");
#                    except:
#                        traceback.print_exc();
#                        f.write(traceback.format_exc());
#                        break;
#                f.close();
#        except KeyboardInterrupt:
#            sys.exit(0);
#        time.sleep(60);

#def main(cli, ser, number_threads):
#    global MACHINE; 
#
#    os.environ['ROOT'] = ROOT;
#    # Cliente e servidor iniciados auqi...
#    if ser == True:
#        server = BorgServer(ROOT, MACHINE);
#        server.start();
#        time.sleep(2);
#    if cli == True:
#        work = BorgWork(ROOT, number_threads, MACHINE);
#        work.start();
#    time.sleep(5);
#    # Thread que monitora dados da rede BORG
#    thread = Thread(target = findBorg, args = ());
#    thread.start();
#    thread2 = Thread(target = dados_processos, args = ());
#    thread2.start();
#    #replication();

# ---------------------------------- INICIO -----------------------
#client_par = False;
#server_par = False;
#number_threads = 10;

# chama o codigo que perpara o ambiente, diretórios de preferência.
#prepare();

# limpando qualquer coisa anterior
#os.system("ps -ef | grep '/borg/main/' | grep -v app.py | grep -v grep | awk '{print $2}' | xargs -r kill -9");
#time.sleep(3);

#if len(sys.argv) == 1:
#    print("Você não digitou argumentos...");
#else:
#    i = 0;
#    while True:
#        if i == len(sys.argv):
#            break;
#        if sys.argv[i] == "-s":
#            server_par = True;
#        elif sys.argv[i] == "-c":
#            client_par = True;
#        elif sys.argv[i] == "-t":
#            number_threads = int(sys.argv[i + 1]);
#            i += 1;
#        i += 1;
#    if os.path.exists(ROOT + "/data/ips.json"):
#        os.unlink(ROOT+ "/data/ips.json");    
#    main(client_par, server_par, number_threads);

