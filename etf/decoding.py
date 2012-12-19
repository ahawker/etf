import functools
import format
import struct
import tags
import terms
import zlib

__author__ = 'ahawker'
__all__ = ['ETFDecodingError', 'ETFDecoder']

def tag(tag):
    def decorator(func):
        @functools.wraps(func)
        def f(*args, **kwargs):
            pos = args[2]
            if pos < 0:
                raise ValueError('{0} expects non-negative position'.format(func.__name__))
            tbyte = args[1][pos]
            if tag != tbyte:
                raise ValueError('{0} got tag {1} but expects {2}'.format(func.__name__, tbyte, tag))
            return func(*(args[0], args[1], pos+1), **kwargs)
        f.tag = tag
        return f
    return decorator

class ETFDecodingError(Exception):
    pass

class ETFDecoder(object):
    def __init__(self):
        super(ETFDecoder, self).__init__()
        def _generate_handlers(): #yield all decode_* functions which have term tag
            return ((dec.tag, dec) \
                for dec in (getattr(self, f) \
                for f in self.__class__.__dict__ if f.startswith('decode_')) if hasattr(dec, 'tag'))
        self.handlers = dict(_generate_handlers())

    def decode(self, data):
        version = data[0]
        if version != tags.VERSION:
            raise ETFDecodingError('Decode got version {0} but expects {1}'.format(version, tags.VERSION))
        return self.decode_term(data, pos=1)

    def decode_term(self, data, pos=0):
        tag = data[pos]
        return self.handlers[tag](data, pos)

    @tag(tags.COMPRESSED)
    def decode_compressed_term(self, data, pos):
        offset = pos + 4
        ucsize = struct.unpack(format.UINT32, data[pos:offset])[0]
        csize = offset + ucsize
        return self.decode_term(zlib.decompress(data[offset:csize]))

    @tag(tags.SMALL_INTEGER)
    def decode_small_integer(self, data, pos):
        offset = pos + 1
        return struct.unpack(format.INT8, data[pos:offset])[0]

    @tag(tags.INTEGER)
    def decode_integer(self, data, pos):
        offset = pos + 4
        return struct.unpack(format.INT32, data[pos:offset])[0]

    @tag(tags.FLOAT)
    def decode_float(self, data, pos):
        offset = pos + 4
        return struct.unpack(format.FLOAT, data[pos:offset])[0]

    @tag(tags.ATOM)
    def decode_atom(self, data, pos):
        offset = pos + 2
        length = struct.unpack(format.UINT16, data[pos:offset])[0]
        return terms.Atom(data[offset:offset+length])

    @tag(tags.REFERENCE)
    def decode_reference(self, data, pos):
        node, pos = self.decode_term(data, pos) #???
        offset = pos + 5
        id, creation = struct.unpack(format.ID_CREATION_PAIR, data[pos:offset])
        return terms.Reference(node, id, creation)

    @tag(tags.SMALL_TUPLE)
    def decode_small_tuple(self, data, pos):
        offset = pos + 1
        arity = struct.unpack(format.INT8, data[pos:offset])[0]
        return self._decode_iterable(data[:offset], pos, arity, tuple)

    @tag(tags.LARGE_TUPLE)
    def decode_large_tuple(self, data, pos):
        offset = pos + 4
        arity = struct.unpack(format.UINT32, data[pos:offset])[0]
        return self._decode_iterable(data[:offset], pos, arity, tuple)

    @tag(tags.NIL)
    def decode_nil(self, data, pos):
        return [] # Can we return None here instead ??? TODO

    @tag(tags.STRING)
    def decode_string(self, data, pos):
        offset = pos + 2
        length = struct.unpack(format.UINT16, data[pos:offset])[0]
        string = data[offset:offset+length]
        return [struct.unpack(format.INT8, c) for c in string]

    @tag(tags.LIST)
    def decode_list(self, data, pos):
        pass

    @tag(tags.BINARY)
    def decode_binary(self, data, pos):
        pass

    @tag(tags.SMALL_BIG)
    def decode_small_big(self, data, pos):
        pass

    @tag(tags.LARGE_BIG)
    def decode_large_big(self, data, pos):
        pass

    @tag(tags.NEW_REFERENCE)
    def decode_new_reference(self, data, pos):
        pass

    @tag(tags.SMALL_ATOM)
    def decode_small_atom(self, data, pos):
        pass

    @tag(tags.FUN)
    def decode_fun(self, data, pos):
        pass

    @tag(tags.NEW_FUN)
    def decode_new_fun(self, data, pos):
        pass

    @tag(tags.EXPORT)
    def decode_export(self, data, pos):
        pass

    @tag(tags.BIT_BINARY)
    def decode_bit_binary(self, data, pos):
        pass

    @tag(tags.NEW_FLOAT)
    def decode_new_float(self, data, pos):
        pass

    def _decode_iterable(self, data, pos, length, type):
        def _decoded_term_generator(data, pos, length):
            for _ in range(0, length):
                data, pos = self.decode_term(data, pos)
                yield data
        return type(_decoded_term_generator(data, pos, length))

if __name__ == '__main__':
    d = ETFDecoder()
    pass