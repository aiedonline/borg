import uuid, sys, os;


sys.path.insert(0, os.environ['ROOT']);

from api.sock_util import *;

class Service():
    def __init__(self, CONFIG, module_label):
        self.module_label = module_label;
        self.sessions = {};
        self.CONFIG = CONFIG;
        self.LOCAL = json.loads(open(os.environ['ROOT'] + "/main/parts/"+ module_label +"/config.json").read());
        print("\t...::: Módulo " +  module_label + ":" , self.CONFIG['port'] + self.LOCAL["port"], ":::...");
        try:
            self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            self.serversocket.bind(('0.0.0.0', self.CONFIG['port'] + self.LOCAL["port"]));
            self.serversocket.listen(1500);
            self.run();
        except KeyboardInterrupt:
            print( 'Interrupted');
            sys.exit(0);
        except:
            traceback.print_exc();
            sys.stdout.write("Falha ao abrir portas.")
            os._exit(1);
    def run(self):
        while True:
            try:
                (clientsocket, address) = self.serversocket.accept();
                Thread(target=self.dispacher, args=(clientsocket, address[0], )).start();
            except KeyboardInterrupt:
                print( 'Interrupted');
                sys.exit(0);
            except:
                traceback.print_exc();
    def dispacher(self, clientsocket, address):
        # ('6', '000', '000', '00AAA', '000', '10000000', '0000000', '00000000000000')
        server_data = borg_wait(clientsocket, address, local="server");
        class_method = getattr(self, "dispacher_" + server_data[3] + "_" + server_data[4]);
        result = class_method(clientsocket, address, server_data );
    
    def keynew(self):
        session_id = str(uuid.uuid4());
        self.sessions[session_id] = str(uuid.uuid4());
        return ( session_id, self.sessions[session_id]);
    def keyclose(self, session_id):
        self.sessions[session_id] = None;

    def dispacher_KEYNW_000(self, clientsocket, address, server_data):
        retorno = self.keynew();
        borg_response_raw(clientsocket, address, "KEYNW", "000",  json.dumps( {"session_id" : retorno[0], "key" : retorno[1] } ) );
    def dispacher_KEYCL_000(self, clientsocket, address, server_data):
        #('{"session_id": "66a4e807-efde-42cd-a339-2b80e1a9233e"}', '111', '222', 'KEYCL', '000', '88888888', '7777777', '00000000000005')
        server_data = json.loads(server_data[0]);    
        self.keyclose(server_data["session_id"]);
        borg_response_raw(clientsocket, address, "KEYCL", "000",  json.dumps( {"status" : True } ) );
