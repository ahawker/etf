__author__ = 'ahawker'
__all__ = ['Atom', 'Export', 'Port', 'Pid', 'Reference']

class Atom(str):
    def __new__(cls, string):
        if string and isinstance(string, str):
            if len(string) > 255:
                raise ValueError('Atom max length is 255')
            if string.lower() in ('true', 'false', 'none'):
                return eval(string.capitalize())
        return super(Atom, cls).__new__(cls, string)
    def __init__(self, string):
        super(Atom, self).__init__(string)
    def __repr__(self):
        return '<Atom({0})>'.format(self)

class Export(object):
    def __init__(self, module, function, arity):
        pass

class Port(object):
    def __init__(self, node, id, creation):
        pass

class Pid(object):
    def __init__(self, node, id, serial, creation):
        pass

class Reference(object):
    def __init__(self, node, id, creation):
        pass