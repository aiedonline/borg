import uuid;


class Service():
    def __init__(self):
        self.sessions = {};
    def keynew(self):
        session_id = str(uuid.uuid4());
        self.sessions[session_id] = str(uuid.uuid4());
        return ( session_id, self.sessions[session_id]);
    def keyclose(self, session_id):
        self.sessions[session_id] = None;

    def dispacher_KEYNW_000(self, clientsocket, address, server_data):
        retorno = self.keynew();
        borg_response_rsa(clientsocket, address, protocol, version,  json.dumps( {"session_id" : retorno[0], "key" : retorno[1] } ) );
    def dispacher_KEYCL_000(self, clientsocket, address, server_data):
        retorno = self.keynew();
        self.keyclose(server_data["session_id"]);
        borg_response_rsa(clientsocket, address, protocol, version,  json.dumps( {"status" : True } ) );
