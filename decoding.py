__author__ = 'ahawker'

import format
import functools
import struct
import tags
import terms
import zlib

class ETFDecodingError(Exception):
    pass

def validate(expected_tag=None):
    def decorator(decode):
        @functools.wraps(decode)
        def f(*args, **kwargs):
            if not args[1]: #data
                raise ETFDecodingError('{0} expects data but got none'.format(decode.__name__))
            if args[2] < 0: #pos
                raise ValueError('{0} expects position >= zero'.format(decode.__name__))
            #args[1] is our data, args[1][0] is the tag byte, unpack returns tuple
            tag = struct.unpack(format.INT8, args[1][0])[0]
            if expected_tag and tag != expected_tag:
                raise ETFDecodingError('{0} got tag {1} but expects {2}'.format(decode.__name__, tag, expected_tag))
            return decode(*args, **kwargs)
        return f
    return decorator

class ETFDecoder(object):
    def __init__(self, encoding='utf-8'):
        super(ETFDecoder, self).__init__()
        self.encoding = encoding

    def decode(self, data):
        version = struct.unpack(format.INT8, data[0])
        if version != tags.VERSION:
            raise ETFDecodingError('Decode got version {0} but expects {1}'.format(version, tags.VERSION))

    def decode_term(self, data, pos):
        pass

    def decode_compressed_term(self, data, pos):
        offset = pos + 4
        ucsize = struct.unpack(format.UINT32, data[pos:offset])[0]
        csize = offset + ucsize
        return zlib.decompress(data[offset:csize])

    @validate(tags.SMALL_INTEGER)
    def decode_small_integer(self, data, pos):
        offset = pos + 1
        return struct.unpack(format.INT8, data[pos:offset])[0]

    def decode_integer(self, data, pos):
        offset = pos + 4
        return struct.unpack(format.INT32, data[pos:offset])[0]

    def decode_float(self, data, pos):
        offset = pos + 4
        return struct.unpack(format.FLOAT, data[pos:offset])[0]

    def decode_atom(self, data, pos):
        offset = pos + 2
        length = struct.unpack(format.UINT16, data[pos:offset])[0]
        return terms.Atom(data[offset:offset+length])

    def decode_reference(self, data, pos):
        node, pos = self.decode_term(data, pos) #???
        offset = pos + 5
        id, creation = struct.unpack(format.ID_CREATION_PAIR, data[pos:offset])
        return terms.Reference(node, id, creation)

    def decode_small_tuple(self, data, pos):
        offset = pos + 1
        arity = struct.unpack(format.INT8, data[pos:offset])[0]
        return self._decode_iterable(data[:offset], pos, arity, tuple)

    def decode_large_tuple(self, data, pos):
        offset = pos + 4
        arity = struct.unpack(format.UINT32, data[pos:offset])[0]
        return self._decode_iterable(data[:offset], pos, arity, tuple)

    def decode_nil(self, data, pos):
        return [] # Can we return None here instead ??? TODO

    def decode_string(self, data, pos):
        offset = pos + 2
        length = struct.unpack(format.UINT16, data[pos:offset])[0]
        string = data[offset:offset+length]
        return [struct.unpack(format.INT8, c) for c in string]

    def decode_list(self, data, pos):
        pass

    def decode_binary(self, data, pos):
        pass

    def decode_small_big(self, data, pos):
        pass

    def decode_large_big(self, data, pos):
        pass

    def decode_new_reference(self, data, pos):
        pass

    def decode_small_atom(self, data, pos):
        pass

    def decode_fun(self, data, pos):
        pass

    def decode_new_fun(self, data, pos):
        pass

    def decode_export(self, data, pos):
        pass

    def decode_bit_binary(self, data, pos):
        pass

    def decode_new_float(self, data, pos):
        pass

    def _decode_iterable(self, data, pos, length, type):
        def _decoded_term_generator(data, pos, length):
            for _ in range(0, length):
                data, pos = self.decode_term(data, pos)
                yield data
        return type(_decoded_term_generator(data, pos, length))
