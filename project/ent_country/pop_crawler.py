# -*- coding: utf-8 -*-
import requests, os, inspect, sys, json, hashlib, traceback;

data = sys.stdin.readlines();
input_process = json.loads(data[0].rstrip());

ROOT = os.environ['ROOT'];
sys.path.insert(0,ROOT);
from api.clienthelper import *;
from api.cacherequest import *;

db = Database(input_process["config"]["ip"], input_process["config"]["port"]);

if len(input_process['work']['input']) > 0:
    last = json.loads(input_process['work']['input'][len(input_process['work']['input']) - 1]['input']);
    page = CacheRequest(life=60, cache=True);
    page.get("https://en.wikipedia.org" + last['url']);
    header = page.elements('//*[@id="firstHeading"]')[0];
    print("TITLE:", header.text_content(), " in ", last['url']);
    # db.write("entity", "country", ["id"], [  id_coutry ], ["name", "region", "flag", "url_wiki_population"], [country['name'], country['region'], country['flag'], country['url'] ]);
exit(0);
















