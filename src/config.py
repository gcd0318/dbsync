from configparser import ConfigParser

class Config(ConfigParser):
    def __init__(self, conf_fn):
        ConfigParser.__init__(self)
        self.conf_fn = conf_fn
#        self = configparser.ConfigParser()
        self.read(conf_fn)

    def read_data(self, section=None, option=None):
        res = None
        if (section or option) is None:
            res = {}
            if self.has_section('cluster'):
                for key in self.options('cluster'):
                    res[key] = self.get('cluster', key)
            if self.has_section('node'):
                for key in self.options('node'):
                    res[key] = self.get('node', key)
        elif section is None:
            if self.has_option('cluster', option):
                res = self.get('cluster', option)
            if self.has_option('node', option):
                res = self.get('node', option)
        elif option is None:
            res = {}
            if self.has_section(section):
                for key in self.options(section):
                    res[key] = self.get(section, key)
        else:
            res = self.get(section, option)
        return res

    def write_data(self, section, option, value):
        self.set(section, option, value)
        self.write(open(self.conf_fn, "w"))

    def remove_data(self, section, option):
        if (section or option) is None:
            for section in self.sections():
                self.remove_section(section)
        elif section is None:
            for section in self.sections():
                self.remove_option(section, option)
        elif option is None:
            self.remove_section(section)
        else:
            self.remove_option(section, option)
        self.write(open(self.conf_fn, "w"))


if '__main__' == __name__:
    conf = Config('db.conf')
    print(conf.read_data())
    conf.write_data('cluster', 'test', 'test1')
    print(conf.read_data())
    conf.write_data('node', 'test', 'test2')
    print(conf.read_data())
    conf.remove_data('node', 'test')
    conf.remove_data('cluster', 'test')
    print(conf.read_data(option='dbname'))
    print(conf.read_data(option='ips'))
    print(conf.read_data(section='cluster'))
