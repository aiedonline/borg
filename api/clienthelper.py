import os, sys, time, uuid, datetime;
from threading import Thread

ROOT = os.environ['ROOT'];
sys.path.insert(0,ROOT);

from api.sock_util import *;
from api.process import *;

class BorgCommuniction():
    def __init__(self, ip, port):
        self.ip = ip;
        self.port = port;
        self.key = None;
        self.session_id = None;
        self.keynew();
    def __del__(self):
        borg_request_raw(self.ip, self.port, "KEYCL", "000", json.dumps({"session_id" : self.session_id}));
    def keynew(self):
        retorno = borg_request_raw(self.ip, self.port, "KEYNW" , "000", "{}");
        # ('{"session_id": "fbd5e380-1db7-40fc-8318-b8cca66b888f", "key": "371abf0a-1953-4398-a8af-dca575a7a811"}', '111', '222', 'KEYNW', '000', '88888888', '7777777', '00000000000010')
        retorno = json.loads(retorno[0]);
        self.key = retorno["key"];
        self.session_id = retorno["session_id"];
        
    def request(self, protocol, protocol_version,  data, type="raw"):
        if type == "raw":
            return json.loads( borg_request_raw(self.ip, self.port, protocol, protocol_version, json.dumps(data))[0] );
        #elif type == "aes":
        #    return borg_request_aes(self.ip, self.port, protocol, protocol_version, json.dumps(data));
        elif type == "rsa":
            return borg_request_rsa(self.ip, self.port, protocol, protocol_version, json.dumps(data));

class Database(BorgCommuniction):
    def __init__(self, ip, start_port):
        super().__init__(ip, start_port + 2);

    def write(self, domain, table, keys, values_keys, fields, value_fields ):
        buffer = self.request("WRITE", "000",  {"domain" : domain, "table" : table,  "keys" : keys, "fields" : fields, "values_keys" : values_keys, "values_fields" : value_fields}, type="raw");
        #sys.stderr.write("Buffer: " + str(buffer));
        return buffer;
class Base(BorgCommuniction):
    def __init__(self, ip, start_port):
        super().__init__(ip, start_port + 1);
    
    def file_update(self, file, md5):
        hash_file = None;
        if os.path.exists(ROOT + "/tmp/" + file):
            hash_file = hashlib.md5( open(ROOT + "/tmp/" + file).read().encode() ).hexdigest();
        if md5 != hash_file:
            path_dir = ROOT + "/tmp/" + file[ : file.rfind("/") ];
            if not os.path.exists(path_dir):
                os.makedirs(path_dir);
            with open( ROOT + "/tmp/" + file ,"w") as f:
                print('Será baixado: ', "/tmp/" + file);
                f.write(self.get_file(file));
                f.close();
    def get_file(self, file ):
        return self.request("GETFI", "000",  {"file" : file}, type="raw")['file'];
    def project_update(self, project_name ):
        files = self.request("PROFI", "000",  {"name" : project_name}, type="raw");
        for file in files:
            self.file_update(file['file'], file['md5']);
        return files;
    
class MQ(BorgCommuniction):
    def __init__(self, ip, start_port):
        super().__init__(ip, start_port + 3);
    def register(self, group_name, queue_name, queue_step_name, input, execute_in, id="", flag="" ):
        input = json.dumps(input);
        return self.request("REGIS", "000",  {"id" : id , "group_name" : group_name, "queue_name" : queue_name, "queue_step_name" : queue_step_name, "input" : input, "execute_in" : execute_in, "flag" : flag}, type="raw");
    def haswork(self):
        # ('[{"id": "", "group_id": "", "queue_id": "", "queue_step_id": "", "input": "{}", "status_code": null, "name": "list", "next": "hellocrawler2", "script": "/hello/list.py", "need": "[]", "active": 1, "interpreter": "python3"}]', '111', '222', 'HASWO', '000', '88888888', '7777777', '00000000000028')
        works = json.loads(  open(os.environ['ROOT'] + "/data/client/config.json").read());
        return self.request("HASWO", "000",  {"id" : str(uuid.uuid4()) , "groups" : works["mq"]["groups"]}, type="raw");
    def next(self, work_id, queue_step_id, stdout):
        return self.request("NEXTW", "000",  {"id" : work_id, "stdout" : stdout, "queue_step_id" : queue_step_id}, type="raw");
    def err(self, work_id, status_code, stdout, sterr):
        return self.request("ERRWO", "000",  {"id" : work_id,  "status_code" : status_code,  "stdout" : stdout, "sterr" : sterr}, type="raw");
    def input_add(self, work_id, input):
        return self.request("INPNW", "000",  {"work_id" : work_id,  "input" : input}, type="raw");