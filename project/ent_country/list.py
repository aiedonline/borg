# -*- coding: utf-8 -*-
import requests, os, inspect, sys, json, hashlib;
#import datetime

from urllib.parse import unquote
from lxml import html

data = sys.stdin.readlines();
input_process = json.loads(data[0].rstrip());

os.environ['ROOT'] = "/opt/borg/";

ROOT = os.environ['ROOT'];
sys.path.insert(0,ROOT);
from api.clienthelper import *;
from api.cacherequest import *;

#https://en.wikipedia.org/wiki/Lists_of_countries_and_territories
page = CacheRequest(life=60, cache=True);
page.get("https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population");
table = page.elements('//table/tbody')[0];
print(table);
trs = table.xpath("./tr");

elements = [];
for tr in trs:
    tds = tr.xpath("./td");
    if len(tds) == 0:
        continue;
    a_name =      tds[0].xpath("./a");
    if len(a_name) == 0:
        continue;
    img_name = tds[0].xpath("./span/img"); 
    if len(img_name) == 0:
        continue;
    
    name =    a_name[0].text_content();
    url =     a_name[0].attrib['href'];
    flag =    img_name[0].attrib['src'];
    regiao =  tds[1].text_content();
    pop =     tds[2].text_content();
    elements.append({"name" : name, "population" : pop, "region" : regiao, "url" : url, "flag" : flag});

mq = MQ(input_process["config"]["ip"], input_process["config"]["port"]);
mq.input_add(input_process["work"]["id"], json.dumps(elements));

exit(0);