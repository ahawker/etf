__author__ = 'ahawker'
__all__ = ['Atom', 'Binary', 'BitBinary', 'Export', 'Float', 'NewFloat', 'Port', 'Pid', 'Reference', 'String']

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

class Binary(str):
    def __init__(self, value):
        super(Binary, self).__init__(value)

    def __repr__(self):
        return '<Binary({0})>'.format(self)

class BitBinary(str):
    def __init__(self, value, bits):
        super(BitBinary, self).__init__(value)
        self.bits = bits

    def __repr__(self):
        return '<BitBinary({0})>'.format(self)
    def __str__(self):
        return '[{0}] {1}'.format(self.bits, super(BitBinary, self).__str__)

class Export(object):
    def __init__(self, module, function, arity):
        self.module = module
        self.function = function
        self.arity = arity

    def __repr__(self):
        return '<Export({0})>'.format(self)
    def __str__(self):
        return '{0}.{1}({2})'.format(self.module, self.function, self.arity)

class Float(float):
    def __init__(self, value):
        super(Float, self).__init__(value)

    def __repr__(self):
        return '<Float({0})>'.format(self)

class NewFloat(float):
    def __init__(self, value):
        super(NewFloat, self).__init__(value)

    def __repr__(self):
        return '<NewFloat({0})>'.format(self)

class Port(object):
    def __init__(self, node, id, creation):
        self.node = node
        self.id = id
        self.creation = creation

    def __repr__(self):
        return '<Port({0})>'.format(self)
    def __str__(self):
        return '[{0}]: Atom({1}) Id:{2}'.format(self.creation, self.node, self.id)

class Pid(object):
    def __init__(self, node, id, serial, creation):
        self.node = node
        self.id = id
        self.serial = serial
        self.creation = creation

    def __repr__(self):
        return '<Pid({0})>'.format(self)
    def __str__(self):
        return '[{0}/{1}]: Atom({2}) Id:{3}'.format(self.creation, self.serial, self.node, self.id)

class Reference(object):
    def __init__(self, node, creation, id):
        self.node = node
        self.creation = creation
        self.id = id

    def __repr__(self):
        return '<Reference({0})>'.format(self)
    def __str__(self):
        return '[{0}]: Atom({1}) Id:{2}'.format(self.creation, self.node, self.id)

class NewReference(object):
    def __init__(self, node, creation, *ids):
        self.node = node
        self.creation = creation
        self.ids = ids
        self.length = len(self.ids)

    def __repr__(self):
        return '<NewReference({0})>'.format(self)
    def __str__(self):
        return '[{0}]: Atom({1}) Id:{2}'.format(self.creation, self.node, ','.join(str(i) for i in self.ids))

class String(unicode):
    def __init__(self, value):
        super(String, self).__init__(value)

    def __repr__(self):
        return '<String({0})>'.format(self)