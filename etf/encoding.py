import functools
import format
import itertools
import struct
import tags
import terms
import zlib

__author__ = 'ahawker'
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
    def __init__(self, minor_version=1):
        super(ETFEncoder, self).__init__()
        def _generate_handlers(): #yield all encode_* functions which have types tuple
            return ((enc.types, enc) \
                for enc in (getattr(self, f) \
                for f in self.__class__.__dict__ if f.startswith('encode_')) if hasattr(enc, 'types'))
        #flatten type tuple into individual keys
        self.handlers = dict((t, enc) for types, enc in _generate_handlers() for t in types)
        self.minor_version = minor_version

    def encode(self, value):
        pass

    def encode_term(self, term):
        term = self.handlers[type(term)](term)
        if len(term) == 1: #NIL only has tag
            return chr(term[0])
        tag, term = term
        return chr(tag), term

    def encode_compressed_term(self, data):
        pass

#    def encode_small_integer(self, data):
#        pass

    @types(int)
    def encode_integer(self, value):
        if 0 <= value <= 255:
            return tags.SMALL_INTEGER, struct.pack(format.INT8, value)
        if -2147483648 <= value <= 2147483647:
            return tags.INTEGER, struct.pack(format.INT32, value)

    @types(float)
    def encode_float(self, value):
        if not self.minor_version:
            value = '{0:.20e}'.format(value)
            pad = 31 - len(value)
            return tags.FLOAT, ''.join((value, '\x00'*pad))
        return tags.NEW_FLOAT, struct.pack(format.DOUBLE, value)

    @types(bool, type(None), terms.Atom)
    def encode_atom(self, atom): #& small atom?
        atom = str(atom)
        return tags.ATOM, struct.pack(format.UINT16, len(atom)), atom

    @types(terms.Reference)
    def encode_reference(self, ref): #& new reference
        length = len(ref.id)
        node = self.encode_atom(ref.node)
        creation = struct.pack(format.INT8, ref.creation)
        ids = struct.pack(format.VARIABLE_UINT32.format(length), *ref.id)
        return tags.NEW_REFERENCE, length, node, creation, ids

#    def encode_small_tuple(self, data):
#        pass
#
#    def encode_large_tuple(self, data):
#        pass

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

#    def encode_nil(self, data):
#        pass

    @types(str, unicode)
    def encode_string(self, data): #& binary
        pass

    @types(list)
    def encode_list(self, lst): #& NIL
        if not lst:
            return tags.NIL,
        length = struct.pack(format.UINT32, len(lst))
        return (tags.LIST, length) + self._encode_iterable(lst) + (tags.NIL,)

#    def encode_binary(self, data):
#        pass

#    def encode_small_big(self, data):
#        pass
#
#    def encode_large_big(self, data):
#        pass

    @types(long)
    def encode_big(self, data):#small/big
        pass

#    @types(terms.Reference)
#    def encode_new_reference(self, data):
#        pass

#    def encode_small_atom(self, data):
#        pass

    def encode_fun(self, data):
        pass

    def encode_new_fun(self, data):
        pass

    @types(terms.Export)
    def encode_export(self, data):
        pass

    def encode_bit_binary(self, data):
        pass

    def _encode_iterable(self, iterable):
        return tuple(itertools.chain.from_iterable(map(lambda t: self.encode_term(t), iterable)))

if __name__ == '__main__':
    e = ETFEncoder()
    pass