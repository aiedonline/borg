import json, os, sys, traceback, socket, hashlib, re;

os.environ['SSHC'] = os.environ['ROOT'] + "/.client";
os.environ['SSHS'] = os.environ['ROOT'] + "/.server";

sys.path.insert(0, os.environ['ROOT']);

from threading import Thread;
from api.sock_util import *;
from main.parts.service import *;

class BorgBase(Service):
    def __init__(self, CONFIG):
        super().__init__(CONFIG, "base");
    
    def hashFile(self, path, saida):
        file_data = open(ROOT + path, 'r').read();
        md5_hash = hashlib.md5();
        md5_hash.update(open( ROOT + path ).read().encode("utf-8"));
        saida.append({"file" :  path, "md5" : md5_hash.hexdigest() });
        resultados = re.findall(r'from(.*?)import', file_data );
        for resultado in resultados:
            resultado = resultado.strip().replace('.', '/');
            if os.path.exists(ROOT + "/" + resultado + ".py" ) == True:
                self.hashFile("/" + resultado + ".py", saida)

    def dispacher_PROFI_000(self, clientsocket, address, server_data):
        server_data = json.loads(server_data[0]);
        protocol = "PROFI"; version = "111";
        arquivos = [];
        for project_name in server_data['name']:
            files_in_project = os.listdir(ROOT + '/project/' + project_name);
            for file_in_project in files_in_project:
                self.hashFile('/project/' + project_name + "/" + file_in_project, arquivos);
        borg_response_raw(clientsocket, address, protocol, version, json.dumps( arquivos ));

    def dispacher_GETFI_000(self, clientsocket, address, server_data):
        server_data = json.loads(server_data[0]);
        protocol = "GETFI"; version = "111";
        borg_response_raw(clientsocket, address, protocol, version, json.dumps( {"file" : open( ROOT + server_data["file"] ).read() } ));

    def dispacher_HELLO(self, clientsocket, address, server_data):
        protocol = "HELLO"; version = "111";
        borg_response_raw(clientsocket, address, protocol, version, "OLAAMIGO");
        
    
try:
    CONFIG = json.loads(open(os.environ['ROOT'] + "/data/server/config.json", "r").read());
    BorgBase(CONFIG);
except KeyboardInterrupt:
    print( 'Interrupted');
    sys.exit(0);
except:
    traceback.print_exc();
