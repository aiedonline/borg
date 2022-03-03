import mysql.connector,json;
from mysql.connector.cursor import MySQLCursorPrepared

class My():
    def __init__(self, host, database,  user, password):
        self.connection = mysql.connector.connect(
           host=host, user=user,
           password=password, database=database );
    
    def process_meta(self, tables):
        print("Criando tabelas e colunas.");


    def datatable(self, sql, values=()):
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
        print(sql, values);
        cursor = self.connection.cursor();
        cursor.execute(sql, values);
        self.connection.commit();
        return cursor.lastrowid;

        
