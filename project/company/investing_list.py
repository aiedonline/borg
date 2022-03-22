# -*- coding: utf-8 -*-
import requests, os, inspect, sys, json, hashlib;
#import datetime

from urllib.parse import unquote
from lxml import html

data = sys.stdin.readlines();
input_process = json.loads(data[0].rstrip());

#input_process = { "config" : {}, "data" : {"url" : "https://br.investing.com/equities/", "country" : "russia"} };

os.environ['ROOT'] = "/opt/borg/";

ROOT = os.environ['ROOT'];
sys.path.insert(0,ROOT);
from api.clienthelper import *;
from api.cacherequest import *;

mq = MQ(input_process["config"]["ip"], input_process["config"]["port"]);

last = json.loads(input_process['work']['input'][len(input_process['work']['input']) - 1]['input']);
print(last);
page = CacheRequest(life=60, cache=True);
page.get( last['url'] + last['country'] );
links = page.elements('//table[@id="cross_rate_markets_stocks_1"]/tbody/tr/td[2]/a');

for link in links:
    conteudo = link.text_content();
    url      = link.attrib['href'];
    codigo = url[url.rfind("/") + 1:];
    if codigo.rfind("?") > 0:
        codigo = codigo[:codigo.rfind("?")]
    print(conteudo, url, "\033[91m", codigo, "\033[0m" );
    mq.register("group_name", "queue_name", "queue_step_name", {}, "2000-01-01 00:00:00", id=hashlib.md5( codigo.encode() ).hexdigest());

exit(0);