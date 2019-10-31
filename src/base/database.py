class Database(object):
    def __init__(self, username, password, host='127.0.0.1', port=5678, encoding="UTF-8", dbname='dbsync', dbtype='postgresql', timeout=60):
        def _connect_postgresql(dbname, username, password, host, port=5678, encoding=encoding, timeout=timeout):
            import psycopg2
            return psycopg2.connect(dbname=dbname, user=username, password=password, port=port, host=host, client_encoding=encoding)
        def _connect_mysql(dbname, username, password, host, port=5678, encoding=encoding, timeout=timeout):
            from mysql.connector import connection
            if "UTF-8" == encoding:
                encoding = 'utf8'
            return connection.MySQLConnection(database=dbname, user=username, password=password, port=port, host=host, charset=encoding, connect_timeout=timeout)

        self.dbtype = dbtype
        self.conn = None
        if ('postgresql' == self.dbtype):
            self.conn = _connect_postgresql(dbname, username, password, host, port, encoding)
        elif(self.dbtype in ('mysql', 'mariadb')):
            self.conn = _connect_mysql(dbname, username, password, host, port, encoding)

    def is_alive(self):
        r = self.exec('show tables;') 
        return r is not None

    def exec(self, sql):
        print(sql)
        if not sql.endswith(';'):
            sql = sql + ';'
        action, *_ = sql.split()
        action = action.lower()
        res = None
        if(self.conn is not None):
            cursor = self.conn.cursor()
            cursor.execute(sql)
            if action in ('desc', 'select', 'show'):
                res = cursor.fetchall()
            elif 'insert' == action:
                cursor.commit()
        else:
            pass
        return res

if __name__ == '__main__':
    db = DB(host='127.0.0.1', port=3306, dbtype='mariadb', username='dbsync', password='dbsync', dbname='dbsync')
    r = db.exec('show tables;')
    print(r)
