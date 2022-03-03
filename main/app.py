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
