import configparser

class Config(object):
    def __init__(self, conf_fn):
        self.conf_fn = conf_fn
        self.conf = configparser.ConfigParser()
        self.conf.read(conf_fn)

    def read(self, section=None, option=None):
        res = None
        if (section or option) is None:
            res = {}
            if self.conf.has_section('cluster'):
                for key in self.conf.options('cluster'):
                    res[key] = self.conf.get('cluster', key)
            if self.conf.has_section('node'):
                for key in self.conf.options('node'):
                    res[key] = self.conf.get('node', key)
        elif section is None:
            if self.conf.has_option('cluster', option):
                res = self.conf.get('cluster', option)
            if self.conf.has_option('node', option):
                res = self.conf.get('node', option)
        elif option is None:
            if self.conf.has_section(section):
                for key in self.conf.options(section):
                    res[key] = self.conf.get(section, key)
        else:
            res = self.conf.get(section, option)
        return res

    def write(self, section, option, value):
        self.conf.set(section, option, value)
        self.conf.write(open(self.conf_fn, "w"))

    def remove(self, section, option):
        if (section or option) is None:
            for section in self.conf.sections():
                self.conf.remove_section(section)
        elif section is None:
            for section in self.conf.sections():
                self.conf.remove_option(section, option)
        elif option is None:
            self.conf.remove_section(section)
        else:
            self.conf.remove_option(section, option)
        self.conf.write(open(self.conf_fn, "w"))


if '__main__' == __name__:
    conf = Config('db.conf')
    conf.write('cluster', 'test', 'test1')
    print(conf.read())
    conf.write('node', 'test', 'test2')
    print(conf.read())
    conf.remove('node', 'test')
    conf.remove('cluster', 'test')
    print(conf.read(option='dbname'))
    print(conf.read(option='cluster'))
