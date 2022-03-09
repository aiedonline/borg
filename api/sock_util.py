# -*- coding: utf-8 -*-
import json, socket, base64, time, traceback, os, sys, inspect, random
import uuid;

PROTOCOLS = [ "HELLO" ];
ROOT = os.environ['ROOT'];

sys.path.insert(0,ROOT);

from api.rsahelper import *;

TEMPO_ESPERA = 0.1;
CONFIG_SERVER = json.loads(open(ROOT + "/data/server/config.json").read());

# -------------------------- TRANSMISSÃO DE DADOS BINÁRIO CRIPTOGRAFADO -----------------
#def borg_response(sock, ip, protocol, version, text):
#    rsa = RsaHelper(path_to_pem= os.environ['ROOT'] + "/.client", name_file_pem= ip + ".pem" );
#    text = rsa.encrypt( envelop_make(protocol, version, text) );
#    sock.sendall(len(text.encode("utf-8")).to_bytes(8, 'big'))
#    sock.sendall(text.encode("utf-8"))



# ===================== RAW ==============================
def borg_response_raw(sock, ip, protocol, version, text):
    array = [envelop_make(protocol, version, text)];
    data_to_send = "raw000" + json.dumps(array).encode("utf-8");
    sock.sendall(len(data_to_send).to_bytes(8, 'big'));
    sock.sendall(data_to_send);

def borg_request_raw(ip, port, protocol, version, text):
    text = envelop_make(protocol, version, text);
    array = [text];
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    sock.connect((ip, port));
    data_to_send = "raw000" + json.dumps(array).encode("utf-8");
    sock.sendall(len(data_to_send).to_bytes(8, 'big'));
    sock.sendall(data_to_send);
    # ---------------- retorno resposta -------------
    return borg_wait(sock, ip);


#def borg_wait_raw(sock, address):
#    expected_size = b""
#    while len(expected_size) < 8:
#        more_size = sock.recv(8 - len(expected_size))
#        if not more_size:
#            raise Exception("Short file length received")
#        expected_size += more_size
#    expected_size = int.from_bytes(expected_size, 'big')
#    packet = b""  # Use bytes, not str, to accumulate
#    while len(packet) < expected_size:
#        buffer = sock.recv(expected_size - len(packet))
#        if not buffer:
#            raise Exception("Incomplete file received")
#        packet += buffer
#    return envelop_split( json.loads(packet.decode("utf-8")) );

# ===================== RSA =================================

def borg_response_rsa(sock, ip, protocol, version, text):
    rsa = RsaHelper(path_to_pem= os.environ['ROOT'] + "/.client", name_file_pem= ip + ".pem" );
    array = rsa.encryptAll( envelop_make(protocol, version, text) );
    sock.sendall(len(json.dumps(array).encode("utf-8")).to_bytes(8, 'big'))
    sock.sendall(json.dumps(array).encode("utf-8"))

def borg_request_rsa(ip, port, protocol, version, text):
    rsa = RsaHelper(path_to_pem= os.environ['ROOT'] + "/.client", name_file_pem= ip + ".pem" );
    text = envelop_make(protocol, version, text);
    array = rsa.encryptAll( text );
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    sock.connect((ip, port));
    sock.sendall(len(json.dumps(array).encode("utf-8")).to_bytes(8, 'big'))
    sock.sendall(json.dumps(array).encode("utf-8"))
    # ---------------- retorno resposta -------------
    expected_size = b""
    while len(expected_size) < 8:
        more_size = sock.recv(8 - len(expected_size))
        if not more_size:
            raise Exception("Short file length received")
        expected_size += more_size
    expected_size = int.from_bytes(expected_size, 'big')
    packet = b""  
    while len(packet) < expected_size:
        buffer = sock.recv(expected_size - len(packet))
        if not buffer:
            raise Exception("Incomplete file received")
        packet += buffer
    rsa = RsaHelper(path_to_pem= os.environ['ROOT'] + "/.server" , name_file_pem= "borg.pem" );
    return envelop_split( rsa.decryptArray(  json.loads(packet.decode("utf-8")) ) );

#def borg_wait_rsa(sock, address):
#    expected_size = b""
#    while len(expected_size) < 8:
#        more_size = sock.recv(8 - len(expected_size))
#        if not more_size:
#            raise Exception("Short file length received")
#        expected_size += more_size
#    expected_size = int.from_bytes(expected_size, 'big')
#    packet = b""  # Use bytes, not str, to accumulate
#    while len(packet) < expected_size:
#        buffer = sock.recv(expected_size - len(packet))
#        if not buffer:
#            raise Exception("Incomplete file received")
#        packet += buffer
#    rsa = RsaHelper(path_to_pem= os.environ['ROOT'] + "/.server", name_file_pem= "borg.pem" );
#    return envelop_split( rsa.decryptArray(  json.loads(packet.decode("utf-8")) ) );


# ----------------------------------- ENVELOPE DE COMUNICAÇÃO ----------------------------
def envelop_split(message_server):
    #rsa = RsaHelper(name_file_pem="borg.pem");
    # versão zero do protocolo....
    #00-02	Versão do mecanismo de leitura e escrita (3 bytes);*
    #03-05	Sigla do módulo (3 bytes);*
    #06-10	Sigla do protocolo (5 bytes);*
    #11-13	Versão do protocolo (3 bytes);*
    #14-21 	Identificação do parasita (8 bytes);*
    #22-29 	Identificação do alvo (8 bytes);
    #30-44	Tamanho do Playload de dados (15 bytes);
    #000BRL00OLA0008888888800000000000000000000000
    if message_server != type(""):
        buffer = "";
        for element in message_server:
            buffer += element;
        message_server = buffer;
    try:
        header = message_server[:45];
        try:
            version_mec     = header[0:3];
            module_sigla    = header[3:6];
            protocol        = header[6:11];
            version         = header[11:14];
            ident_parasita  = header[14:22];
            ident_alvo      = header[22:29];
            lenght = int(header[30:45]);
            return (  message_server[45: 45 + lenght] , version_mec, module_sigla, protocol, version, ident_parasita, ident_alvo,  header[30:44] );
        except:
            print(header);
            pass;
    except:
        return (None, None, None, None, None, None, None, None);

def random_text(min, max):
    s = "";
    while len(s) < max:
        s = s + str(uuid.uuid4());
    return s[:random.randint(min, max)];

def envelop_make(protocol, version, message, uuid="88888888"):
    global CONFIG_SERVER;
    version_mec     = "111";
    module          = "222";
    alvo            = "77777777";
    try:
        return ( version_mec.zfill(3) + module.zfill(3) + protocol.zfill(5) + version.zfill(3) + uuid.zfill(8) + alvo.zfill(8) + str(len(message)).zfill(15) + message + random_text(10, 2048)); #.encode("utf-8");
    except:
        pass;


def borg_response(sock, ip, protocol, version, text):
    return borg_response_raw(sock, ip, protocol, version, text);
def borg_request(ip, port, protocol, version, text):
    return borg_request_raw(ip, port, protocol, version, text);

def borg_wait(sock, address):
    expected_size = b""
    while len(expected_size) < 8:
        more_size = sock.recv(8 - len(expected_size))
        if not more_size:
            raise Exception("Short file length received")
        expected_size += more_size
    expected_size = int.from_bytes(expected_size, 'big')
    packet = b""  # Use bytes, not str, to accumulate
    while len(packet) < expected_size:
        buffer = sock.recv(expected_size - len(packet))
        if not buffer:
            raise Exception("Incomplete file received")
        packet += buffer
    packet = packet.decode("utf-8");
    algoritm = packet[0:3];
    version  = packet[3:6];
    data = packet[6:];
    if aloritm == "raw":
        return envelop_split( json.loads(packet) );
    elif algoritm == "rsa":
        return envelop_split( rsa.decryptArray(  json.loads(packet) );
    elif algoritm == "aes":
        return envelop_split( aes.decrypt(  json.loads(packet) );                     
        

# ------------------------------- TRANSMISSÃO DE ARQUIVO PEM PÚBLICO RSA -------------
# Usado para trocar PEM file
def trade_pem_client(ip, port):
    if os.path.exists(os.environ['SSHC'] + "/.ssh/public_" + ip + ".pem"):
        return;
    #envio de PEM
    with open( os.environ['SSHS'] + "/.ssh/public_borg.pem", 'rb') as f:
        raw = f.read();
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    sock.connect((ip, port));
    sock.sendall(len(raw).to_bytes(8, 'big'))
    sock.sendall(raw)
    # recebimento do PEM
    expected_size = b""
    while len(expected_size) < 8:
        more_size = sock.recv(8 - len(expected_size))
        if not more_size:
            raise Exception("Short file length received")
        expected_size += more_size
    expected_size = int.from_bytes(expected_size, 'big')
    packet = b""
    while len(packet) < expected_size:
        buffer = sock.recv(expected_size - len(packet))
        if not buffer:
            raise Exception("Incomplete file received")
        packet += buffer
    with open(os.environ['SSHC'] + "/.ssh/public_" + ip + ".pem", 'wb') as f:
        f.write(packet)



