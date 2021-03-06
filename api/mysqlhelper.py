import mysql.connector,json, os;
from mysql.connector.cursor import MySQLCursorPrepared

class My():
    def __init__(self, host=None, database=None,  user=None, password=None, file=None):
        if file == None:
            self.host = host; self.database = database; self.user = user; self.password = password;
            if self.host == None:
                CONFIG = json.loads( open(os.environ['ROOT'] + "/data/server/database.json", "r").read() );
                self.host = CONFIG['host'];
                self.database = CONFIG['database'];
                self.user = CONFIG['user'];
                self.password = CONFIG['password'];
        else:
            CONFIG = json.loads( open(os.environ['ROOT'] + "/main/parts/database/data/" + file + ".json", "r").read() );
            self.host = CONFIG['host'];
            self.database = CONFIG['database'];
            self.user = CONFIG['user'];
            self.password = CONFIG['password'];            
        self.connection = mysql.connector.connect( host=self.host, user=self.user, password= self.password, database= self.database );
    def process_meta(self, tables):
        print("Criando tabelas e colunas.");


    def datatable(self, sql, values):
        cursor = self.connection.cursor()
        cursor.execute(sql, values)
        field_names = [i[0] for i in cursor.description];
        buffer_json = [];
        buffer_dictionary = cursor.fetchall();
        for row in buffer_dictionary:
            buffer_row = {};
            for i in range(len( field_names )):
                buffer_row[field_names[i]] = row[i];
            buffer_json.append(buffer_row);
        return buffer_json;  
              
    def noquery(self, sql, values):
        cursor = self.connection.cursor();
        cursor.execute(sql, values);
        self.connection.commit();
        return cursor.lastrowid;
    def noquerys(self, sqls, valuess):
        cursor = None;
        ids = [];
        try:
            self.connection.autocommit = False;
            cursor = self.connection.cursor();
            for i in range(len(sqls)):
                sql = sqls[i];
                values = valuess[i];
                cursor.execute(sql, values);
                ids.append(cursor.lastrowid);
            self.connection.commit();

        except mysql.connector.Error as error:
            self.connection.rollback()
        finally:
            # closing database connection.
            if self.connection.is_connected():
                if cursor != None:
                    cursor.close();
                #self.connection.close()
                #print("connection is closed")
        return ids;
        
