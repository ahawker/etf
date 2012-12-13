import functools
import format
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
    def __init__(self):
        super(ETFEncoder, self).__init__()
        def _generate_handlers(): #yield all encode_* functions which have types tuple
            return ((enc.types, enc) \
                for enc in (getattr(self, f) \
                for f in self.__class__.__dict__ if f.startswith('encode_')) if hasattr(enc, 'types'))
        #flatten type tuple into individual keys
        self.handlers = dict((t, enc) for types, enc in _generate_handlers() for t in types)

    def encode(self, data):
        pass

    def encode_term(self, data):
        return self.handlers[type(data)](data)

    def encode_compressed_term(self, data):
        pass

#    def encode_small_integer(self, data):
#        pass

    @types(int)
    def encode_integer(self, data):
        pass

    @types(float)
    def encode_float(self, data):
        pass

    @types(bool, type(None), terms.Atom)
    def encode_atom(self, data): #& small atom
        pass

    @types(terms.Reference)
    def encode_reference(self, data): #& new reference
        pass

#    def encode_small_tuple(self, data):
#        pass
#
#    def encode_large_tuple(self, data):
#        pass

    @types(tuple)
    def encode_tuple(self, data): #small/large tuple
        pass

#    def encode_nil(self, data):
#        pass

    @types(str, unicode)
    def encode_string(self, data): #& binary
        pass

    @types(list)
    def encode_list(self, data): #& NIL
        pass

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

    def encode_new_float(self, data):
        pass

if __name__ == '__main__':
    e = ETFEncoder()
    pass