import os, json;

from api.process import Process
from threading import Thread;

class Part():
    def __init__(self, part_name):
        self.part_name = part_name;
        if os.path.exists(self.part_name + "/config.json"):
            self.CONFIG = json.loads(open(part_name + "/config.json", "r").read());
            if self.CONFIG['active'] == True:
                t = Thread(target=self.start);
                t.start();
    def start(self):
        p = Process(self.part_name + "/code.py");
        p.start();
