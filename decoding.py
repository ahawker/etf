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
        x = lambda d,p: ((d,p) for (d,p) in self.decode_term(d,p) for _ in range(0, arity))
        #z = lambda c: ((d,p) for (d,p) in x for _ in range(0, c) )
        #y = ((d,p) for (d,p) in )
        #x = list(term for (term, pos) in (self.decode_term(data, pos) ))
        x = []
        for i in range(0, arity):
            data, pos = self.decode_term(data, pos)
            x.append(data)
        return data, pos
