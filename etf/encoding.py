import array
import functools
import format
import itertools
import struct
import tags
import terms
import zlib

__author__ = 'Andrew Hawker <andrew.r.hawker@gmail.com>'
__all__ = ['ETFEncodingError', 'ETFEncoder']

def types(*etypes):
    def decorator(func):
        @functools.wraps(func)
        def f(*args, **kwargs):
            if not isinstance(args[1], etypes):
                raise ValueError('{0} got type {1} but expects {1}'.format(func.__name__, type(args[1]), etypes))
            return func(*args, **kwargs)
        f.types = etypes
        return f
    return decorator

class ETFEncodingError(Exception):
    pass

class ETFEncoder(object):
    def __init__(self):
        super(ETFEncoder, self).__init__()
        def _generate_handlers(): #yield all encode_* functions which have types tuple
            return ((enc.types, enc) \
                for enc in (getattr(self, f) \
                for f in self.__class__.__dict__ if f.startswith('encode_')) if hasattr(enc, 'types'))
        #flatten type tuple into individual keys
        self.handlers = dict((t, enc) for types, enc in _generate_handlers() for t in types)

    def encode(self, term, compress=False):
        term = self.encode_term(term)
        if compress:
            term = self.compress_term(term)
        return tags.VERSION + term

    def encode_term(self, term):
        return ''.join(self.handlers[type(term)](term))

    def compress_term(self, term):
        cterm = zlib.compress(term)
        if len(cterm) < len(term):
            return tags.COMPRESSED, struct.pack(format.UINT32, len(term)), cterm
        return term

    @types(int)
    def encode_integer(self, value):
        if 0 <= value <= 255:
            return tags.SMALL_INTEGER, struct.pack(format.INT8, value)
        if -2147483648 <= value <= 2147483647:
            return tags.INTEGER, struct.pack(format.INT32, value)

    @types(terms.Float)
    def encode_float(self, value):
        value = '{0:.20e}'.format(value)
        pad = 31 - len(value)
        return tags.FLOAT, ''.join((value, '\x00'*pad))

    @types(bool, type(None), terms.Atom)
    def encode_atom(self, atom): #& small atom?
        atom = str(atom)
        return tags.ATOM, struct.pack(format.UINT16, len(atom)), atom

    @types(terms.Reference)
    def encode_reference(self, ref):
        node = self.encode_atom(ref.node)
        id = struct.pack(format.UINT32, ref.id)
        creation = struct.pack(format.INT8, ref.creation)
        return tags.REFERENCE, node, id, creation

    @types(terms.Port)
    def encode_port(self, port):
        node = self.encode_atom(port.node)
        id = struct.pack(format.UINT32, port.id)
        creation = struct.pack(format.INT8, port.creation)
        return tags.PORT, node, id, creation

    @types(terms.Pid)
    def encode_pid(self, pid):
        node = self.encode_atom(pid.node)
        id = struct.pack(format.UINT32, pid.id)
        serial = struct.pack(format.UINT32, pid.serial)
        creation = struct.pack(format.INT8, pid.creation)
        return tags.PID, node, id, serial, creation

    @types(tuple)
    def encode_tuple(self, tup):
        arity = len(tup)
        if 0 <= arity <= 255:
            tag = tags.SMALL_TUPLE
            arity = struct.pack(format.INT8, arity)
        else:
            tag = tags.LARGE_TUPLE
            arity = struct.pack(format.UINT32, arity)
        return (tag, arity) + self._encode_iterable(tup)

    @types(unicode, terms.String)
    def encode_string(self, string):
        string = [ord(c) for c in string]
        if len(string) > 65535:
            return self.encode_list(string)
        return tags.STRING, struct.pack(format.UINT16, len(string)), string

    @types(list)
    def encode_list(self, lst): #& NIL
        if not lst:
            return tags.NIL,
        length = struct.pack(format.UINT32, len(lst))
        return (tags.LIST, length) + self._encode_iterable(lst) + (tags.NIL,)

    @types(str, terms.Binary)
    def encode_binary(self, binary):
        return tags.BINARY, struct.pack(format.UINT32, len(binary)), binary

    @types(long)
    def encode_big(self, big):
        def to_byte_string(big):
            bytes = array.array('B')
            while big > 0:
                bytes.append(big & 0xFF)
                big >>= 8
            return bytes.tostring()
        sign = struct.pack(format.INT8, (big < 0))
        big = to_byte_string(abs(big))
        length = len(big)
        if 0 <= length <= 255:
            tag = tags.SMALL_BIG
            length = struct.pack(format.INT8, length)
        else:
            tag = tags.LARGE_BIG
            length = struct.pack(format.UINT32, length)
        return tag, length, sign, big

    @types(terms.NewReference)
    def encode_new_reference(self, ref):
        length = len(ref.ids)
        node = self.encode_atom(ref.node)
        creation = struct.pack(format.INT8, ref.creation)
        ids = struct.pack(format.VARIABLE_UINT32.format(length), *ref.ids)
        return tags.NEW_REFERENCE, length, node, creation, ids

    @types(terms.Function)
    def encode_fun(self, func):
        pid = self.encode_pid(func.pid)
        module = self.encode_atom(func.module)
        index = self.encode_integer(func.index)
        uniq = self.encode_integer(func.uniq)
        vars = self._encode_iterable(func.vars) #???
        return tags.FUN, pid, module, index, uniq, vars

    @types(terms.NewFunction)
    def encode_new_fun(self, func):
        size = struct.pack(format.UINT32, func.size)
        arity = struct.pack(format.INT8, func.arity)
        uniq = struct.pack(format.UINT128, (func.uniq >> 64) & (1<<64)-1, func.uniq & (1<<64)-1)
        index = struct.pack(format.UINT32, func.index)
        numvars = len(func.vars) #???
        module = self.encode_atom(func.module)
        oldindex = self.encode_integer(func.oldindex)
        olduniq = self.encode_integer(func.olduniq)
        pid = self.encode_pid(func.pid)
        vars = self._encode_iterable(func.vars)
        return tags.NEW_FUN, size, arity, uniq, index, numvars, module, oldindex, olduniq, pid, vars

    @types(terms.Export)
    def encode_export(self, export):
        module = self.encode_atom(export.module)
        function = self.encode_atom(export.function)
        arity = self.encode_integer(export.arity)
        return tags.EXPORT, module, function, arity

    @types(terms.BitBinary)
    def encode_bit_binary(self, value):
        length = struct.pack(format.UINT32, len(value))
        bits = struct.pack(format.INT8, value.bits)
        return tags.BIT_BINARY, length, bits, value

    @types(float, terms.NewFloat)
    def encode_new_float(self, value):
        return tags.NEW_FLOAT, struct.pack(format.DOUBLE, value)

    def _encode_iterable(self, iterable):
        return tuple(itertools.chain.from_iterable(map(lambda t: self.encode_term(t), iterable)))