from config import Config

class Node(object):

    def __init__(self, conf_fn):
        conf = Config(conf_fn)
        self.node_ip = conf.get('ip', '127.0.0.1')
        self.ips = conf.get('ips', [node_ip])
        self.db = conf.get('db')
        self.port = None
        try:
            self.port = int(conf.get('port'))
        except Exception as err:
            pass
        self.dbname = conf.get('dbname')
        self.username = conf.get('username')
        self.password = conf.get('password')


    def status(self):
        res = True

        return res