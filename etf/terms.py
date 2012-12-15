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
        self.module = module
        self.function = function
        self.arity = arity

    def __repr__(self):
        return '<Export({0})>'.format(self)
    def __str__(self):
        return '{0}.{1}({2})'.format(self.module, self.function, self.arity)

class Port(object):
    def __init__(self, node, id, creation):
        self.node = node
        self.id = id
        self.creation = creation

    def __repr__(self):
        return '<Port({0})>'.format(self)
    def __str__(self):
        return '[{0}]: Atom({1}): {2}'.format(self.creation, self.node, ','.join(str(i) for i in self.id))

class Pid(object):
    def __init__(self, node, id, serial, creation):
        self.node = node
        self.id = id
        self.serial = serial
        self.creation = creation

    def __repr__(self):
        return '<Pid({0})>'.format(self)
    def __str__(self):
        return '[{0}/{1}]: Atom({2}): {3}'.format(self.creation, self.serial,
                                                  self.node, ','.join(str(i) for i in self.id))

class Reference(object):
    def __init__(self, node, id, creation):
        self.node = node
        self.id = id
        self.creation = creation

    def __repr__(self):
        return '<Reference({0})>'.format(self)
    def __str__(self):
        return '[{0}]: Atom({1}): {2}'.format(self.creation, self.node, ','.join(str(i) for i in self.id))