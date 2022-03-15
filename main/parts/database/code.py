import json, os, sys, traceback, socket;

os.environ['ROOT'] = "/home/well/projects/borg/";
os.environ['SSHC'] = os.environ['ROOT'] + "/.client";
os.environ['SSHS'] = os.environ['ROOT'] + "/.server";

sys.path.insert(0, os.environ['ROOT']);

from threading import Thread;
from api.sock_util import *;
from main.parts.service import *;
from api.mysqlhelper import *;

class BorgDatabase(Service):
    def __init__(self, CONFIG):
        super().__init__(CONFIG, "database");
    
    def dispacher_WRITE_000(self, clientsocket, address, server_data):
        # keys, fieds
        # values_keys, values_fields
        # domain, table
        protocol = "WRITE"; version = "000";
        server_data = json.loads(server_data[0]);
        my = My(file=server_data['domain']);

        values1 = [];
        sql_values = "";
        sql_keys_insert_fields = "";
        for key in server_data['keys']:
            if len(sql_keys_insert_fields) > 0:
                sql_keys_insert_fields += " ,";
            if len(sql_values) > 0:
                sql_values += " , ";
            sql_keys_insert_fields += "`" + key + "`";
            sql_values += " %s ";
        
        sql_fields_insert_fields = "";
        for field in server_data['fields']:
            if len(sql_fields_insert_fields) > 0:
                sql_fields_insert_fields += ', ';
            if len(sql_values) > 0:
                sql_values += " , ";
            sql_fields_insert_fields += "`" + field + "`";
            sql_values += " %s ";
        
        sql_fields_update_fields = "";
        for field in server_data['fields']:
            if len(sql_fields_update_fields) > 0:
                sql_fields_update_fields += ', ';
            sql_fields_update_fields += "`" + field + "` = %s ";

        for value in server_data['values_keys']:
            values1.append(value);
        for i in range(2):
            for value in server_data['values_fields']:
                values1.append(value);

        sql1 = "INSERT INTO "+ server_data['table'] +"("+ sql_keys_insert_fields +", "+ sql_fields_insert_fields +") VALUES("+ sql_values +") ON DUPLICATE KEY UPDATE " + sql_fields_update_fields;
        retorno = my.noquery(sql1, values1 );
        borg_response_raw(clientsocket, address, protocol, version,  json.dumps( { "return" :  retorno } ) );
try:
    CONFIG = json.loads(open(os.environ['ROOT'] + "/data/server/config.json", "r").read());
    BorgDatabase(CONFIG);
except KeyboardInterrupt:
    print( 'Interrupted');
    sys.exit(0);
except:
    traceback.print_exc();
