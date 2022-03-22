# -*- coding: utf-8 -*-
import requests, os, inspect, sys, json, hashlib, traceback;


data = sys.stdin.readlines();
input_process = json.loads(data[0].rstrip());

ROOT = os.environ['ROOT'];
sys.path.insert(0,ROOT);
from api.clienthelper import *;

db = Database(input_process["config"]["ip"], input_process["config"]["port"]);
mq = MQ(input_process["config"]["ip"], input_process["config"]["port"]);

if len(input_process['work']['input']) > 0:
    last = json.loads(input_process['work']['input'][len(input_process['work']['input']) - 1]['input']);
    for country in last:
        try:
            id_coutry = hashlib.md5( country['name'].lower().encode() ).hexdigest();
            db.write("entity", "country", ["id"], [  id_coutry ], ["name", "region", "flag", "url_wiki_population"], [country['name'], country['region'], country['flag'], country['url'] ]);
            mq.register("ent_country", "Entity Country Base", "pop_crawler", {"url" : country['url']  }, "2000-01-01 00:00:00", id=hashlib.md5( country['url'].encode() ).hexdigest());
        except:
            traceback.print_exc();
exit(0);
















