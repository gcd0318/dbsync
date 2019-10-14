class Client(self):
    def __init__(self, server_ip):
        self.server = server_ip

class Cluster(object):
    def __init__(self, nodes=[]):
        self.nodes = nodes

    def add_node(self, anode):
        if anode.is_alive():
            self.nodes.append(anode)

    def remove_node(self, anode):
        nodes = []
        for node in self.nodes:
            if node.ip != anode.ip:
                nodes.append(node)
        self.nodes = nodes

    def exec_sql(self, sql):
        for node in nodes:
            node.db.exec(sql)

if '__main__' == __name__:
    c = Cluster()