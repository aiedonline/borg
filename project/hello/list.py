# -*- coding: utf-8 -*-
import requests, os, inspect, sys, json, hashlib;
#import datetime

from urllib.parse import unquote
from lxml import html

data = sys.stdin.readlines();
input_process = json.loads(data[0].rstrip());

ROOT = os.environ['ROOT'];
sys.path.insert(0,ROOT);
from api.clienthelper import *;
from api.cacherequest import *;

page = CacheRequest(life=60, cache=False);
page.get("https://www.google.com");

links = page.elements('//a');

mq = MQ(input_process["config"]["ip"], input_process["config"]["port"]);
mq.input_add(input_process["work"]["id"], json.dumps({"links" : {"count" : len(links)}}));

exit(0);