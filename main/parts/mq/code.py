
import json, os, sys, traceback, socket, traceback, uuid, datetime;
from warnings import catch_warnings;

os.environ['SSHC'] = os.environ['ROOT'] + "/.client";
os.environ['SSHS'] = os.environ['ROOT'] + "/.server";

sys.path.insert(0, os.environ['ROOT']);

from threading import Thread;
from api.sock_util import *;
from api.mysqlhelper import *;
from main.parts.service import *;

DEFAULT_TIME_WAIT_CLIENT = 5;
CREATOR_DATE = '1979-06-12 09:04:00';

class BorgMq(Service):
    def __init__(self, CONFIG):
        super().__init__(CONFIG, "mq");
        self.semaphore = [];
    
    def dispacher_HASWO_000(self, clientsocket, address, server_data):
        #server_data : ('{"id": "", "group_name": "hello", "queue_name": "hello", "queue_step_name": "list", "input": "{}", "execute_in": "2000-01-01 00:00:00", "flag": ""}', '111', '222', 'REGIS', '000', '88888888', '7777777', '00000000000014')
        my = My();
        protocol = "HASWO"; version = "000";
        server_data = json.loads(server_data[0]);
        groups = server_data['groups'];
        groups_id = "";

        # Montar a lista de GRUPOS por ID
        sql = "select * from mq_group where name = %s limit 1";
        for i in range(len(groups)):
            dados = my.datatable(sql, [groups[i]]);
            if len(dados) > 0:
                if len(groups_id) > 0:
                    groups_id += ", ";
                groups_id += "'" + dados[0]['id'] + "'";
        
        # Semáforo e execuçào da consulta
        my_thread_id = str(uuid.uuid4());
        self.semaphore.append(my_thread_id);
        while self.semaphore[0] != my_thread_id:
            time.sleep(0.3); 
        try:
            sql = "SELECT wor.id, wor.group_id, wor.queue_id, wor.queue_step_id, wor.input, wor.status_code,      qus.name, qus.next, qus.script, qus.need, qus.active, qus.interpreter       FROM mq_work as wor  inner join mq_group as gro on wor.group_id = gro.id inner join mq_queue_step as qus on wor.queue_step_id = qus.id where gro.name in ( "+ groups_id +" )  and wor.execute_in < '"+ datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') +"' order by wor.execute_in asc limit 1";
            #mq_queue_step
            #
            #mq_work

            dados = my.datatable(sql, [] );

            for dado in dados:
                sql = "UPDATE mq_work set execute_in = %s where id = %s ";
                # TODO: tempo de 5 minutos tem que ser colocado na tabela mq_work
                my.noquery(sql, [(datetime.datetime.utcnow() + datetime.timedelta(minutes=DEFAULT_TIME_WAIT_CLIENT)).strftime('%Y-%m-%d %H:%M:%S') ,dado["id"]]);
        finally:
            self.semaphore.pop(0);
        borg_response_raw(clientsocket, address, protocol, version,  json.dumps(dados, default=str) );

    def dispacher_NEXTW_000(self, clientsocket, address, server_data):
        protocol = "NEXTW"; version = "000";
        server_data = json.loads(server_data[0]);
        my = My();
        queue_step_dt = my.datatable("SELECT * FROM mq_queue_step where id= %s ", [  server_data["queue_step_id"] ] ); 
        
        # Criando variáveis
        queue_step_next = queue_step_dt[0]["next"]; 
        sql = "UPDATE mq_work set queue_step_id= %s, input= %s, execute_in= '"+ CREATOR_DATE +"' where id= %s";
        retorno = my.noquery(sql, [queue_step_next, ?????  ,server_data["id"]]);
        # invocando o método genérico
        borg_response_raw(clientsocket, address, protocol, version,  json.dumps( retorno ) );
        
    def dispacher_REGIS_000(self, clientsocket, address, server_data):
        #server_data : ('{"id": "", "group_name": "hello", "queue_name": "hello", "queue_step_name": "list", "input": "{}", "execute_in": "2000-01-01 00:00:00", "flag": ""}', '111', '222', 'REGIS', '000', '88888888', '7777777', '00000000000014')
        protocol = "REGIS"; version = "000";
        server_data = json.loads(server_data[0]);
        my = My();
        # Carregando dados para FK
        group_dt =      my.datatable("select * from mq_group where name = %s", [ server_data["group_name"] ] );
        queue_dt =      my.datatable("select * from mq_queue where name = %s", [ server_data["queue_name"] ] ); 
        queue_step_dt = my.datatable("SELECT * FROM mq_queue_step where mq_queue_id= %s and name = %s", [ queue_dt[0]["id"] , server_data["queue_step_name"]] ); 
        ????
        # Criando variáveis
        group_id = group_dt[0]["id"]; 
        queue_id = queue_dt[0]["id"];
        queue_step_id =  queue_step_dt[0]["id"];
        input = server_data["input"]; 
        execute_in = server_data["execute_in"];

        # invocando o método genérico
        borg_response_raw(clientsocket, address, protocol, version,  json.dumps( self._register(group_id, queue_id, queue_step_id, input, execute_in)) );
    def _register(self, group_id, queue_id, queue_step_id, input, execute_in):
        my = My();
        try:
            sql = "INSERT INTO mq_work(id, group_id, queue_id, queue_step_id, input, execute_in) values(%s, %s, %s, %s, %s, %s)";
            id = str( uuid.uuid4() );
            values = [id, group_id, queue_id, queue_step_id, input, execute_in];
            retorno = my.noquery(sql, values);
            noquerys(self, sqls, valuess):??????? auqi....
            return {"status" : True, "return" : retorno};
        except Exception as e:
            traceback.print_exc();
            return {"status" : False, "return" : str(e)};

try:
    CONFIG = json.loads(open(os.environ['ROOT'] + "/data/server/config.json", "r").read());
    BorgMq(CONFIG);
except KeyboardInterrupt:
    print( 'Interrupted');
    sys.exit(0);
except:
    traceback.print_exc();

