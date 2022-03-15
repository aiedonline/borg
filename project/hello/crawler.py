# -*- coding: utf-8 -*-
import requests, os, inspect, sys, json, hashlib;


data = sys.stdin.readlines();
input_process = json.loads(data[0].rstrip());

ROOT = os.environ['ROOT'];
sys.path.insert(0,ROOT);
from api.clienthelper import *;

#sys.stderr.write(json.dumps(input_process));
#{"work": {"id": "", "group_id": "", "queue_id": "", "queue_step_id": "", "status_code": null, "name": "crawler", "next": "", 
# "script": "/hello/crawler.py", "need": "[]", "active": 1, "interpreter": "python3", 
# "input": [{"id": 38, "input": "{\"links\": {\"count\": 17}}", "date_input": "2022-03-14 23:42:44", 
# "work_id": "77ccf033-161b-4961-bbca-613d56233279"}, {"id": 35, "input": "{}", "date_input": "2022-03-14 23:40:26", "work_id": "77ccf033-161b-4961-bbca-613d56233279"}]}

total = 0;
if len(input_process['work']['input']) > 0:
    last = json.loads(input_process['work']['input'][len(input_process['work']['input']) - 1]['input']);
    if last.get("links") != None and last['links'].get("count") != None:
        total = last['links']['count'];

db = Database(input_process["config"]["ip"], input_process["config"]["port"]);
db.write("hello", "hello", ["id"], [input_process['work']['id']], ["value1", "value2"], [input_process['work']['id'], str(total) ]);

exit(0);
