import sys
sys.path.append('..')

from config import Config
from base.cluster import Cluster

class DB(object):
    def __init__(self, username, password, host='127.0.0.1', port=5678, encoding="UTF-8", dbname='cicada', dbtype='postgresql'):
        def _connect_postgresql(dbname, username, password, host, port=5678, encoding=encoding):
            import psycopg2
            return psycopg2.connect(dbname=dbname, user=username, password=password, port=port, host=host, client_encoding=encoding)
        def _connect_mysql(dbname, username, password, host, port=5678, encoding=encoding):
            from mysql.connector import connection
            if "UTF-8" == encoding:
                encoding = 'utf8'
            return connection.MySQLConnection(database=dbname, user=username, password=password, port=port, host=host, charset=encoding)

        self.dbtype = dbtype
        self.conn = None
        if ('postgresql' == self.dbtype):
            self.conn = _connect_postgresql(dbname, username, password, host, port, encoding)
        elif(self.dbtype in ('mysql', 'mariadb')):
            self.conn = _connect_mysql(dbname, username, password, host, port, encoding)

    def exec(self, sql):
        sql = sql.strip()
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

class Node(object):
    def __init__(self, conf_fn):
        conf = Config(conf_fn).read_data()
        self.ips = conf.get('ips')
        self.db = None
        try:
            self.db = DB(
                username=conf.get('username'),
                password=conf.get('password'),
                host='127.0.0.1',#conf.get('ip', '127.0.0.1'),
                port=int(conf.get('port')),
                dbname=conf.get('dbname'),
                dbtype=conf.get('db'))
        except Exception as err:
            print(err)
            import traceback
            print(traceback.format_exc())


    def status(self):
        res = True
        return res

    def is_alive(self):
        return True

    def update_conf(self, option, value, section='node'):
        self.config.write_data(section, option, str(value))

    def add_peer(self, anode):
        self.ips.append(anode.ip)
        self.update_conf('cluster', 'ips', self.ips)

    def remove_peer(self, anode):
        ips = []
        for ip in self.ips:
            if ip != anode.ip:
                ips.append(ip)
        self.ips = ips
        self.update_conf('cluster', 'ips', self.ips)

    def join_cluster(self, cluster):
        pass

    def sync_data(self):
        pass

if '__main__' == __name__:
    node = Node('../db.conf')
    print(node.ips)
    print(node.db.exec('show tables;'))