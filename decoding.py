__author__ = 'ahawker'

import format
import struct
import terms
import zlib

class ETFEncodingError(Exception):
    pass

class ETFDecoder(object):
    def __init__(self, encoding='utf-8'):
        super(ETFDecoder, self).__init__()
        self.encoding = encoding

    def decode(self, data):
        version = ord(data[0])
        #if compressed, uncompress

    def decode_term(self, data, pos):
        pass

    def decode_compressed_term(self, data, pos):
        offset = pos + 4
        ucsize = struct.unpack(format.UINT32, data[pos:offset])[0]
        csize = offset + ucsize
        return zlib.decompress(data[offset:csize])

    def decode_small_integer(self, data, pos):
        offset = pos + 1
        return struct.unpack(format.INT8, data[pos:offset])[0]

    def decode_integer(self, data, pos):
        offset = pos + 4
        return struct.unpack(format.INT32, data[pos:offset])[0]

    def decode_float(self, data, pos):
        return struct.unpack(format.FLOAT, data[pos:pos+4])[0]

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
        return [struct.unpack(format.INT8, i) for i in data[offset:offset+length]]

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
