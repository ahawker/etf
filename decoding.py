import format
import struct
import tags
import terms
import zlib

__author__ = 'ahawker'

class ETFDecodingError(Exception):
    pass

class ETFDecoder(object):
    def __init__(self):
        super(ETFDecoder, self).__init__()
        def _generate_handlers(): #yield all encode_* functions which have term tag
            return ((enc.tag, enc) \
                for enc in (getattr(self, f) \
                for f in self.__class__.__dict__ if f.startswith('decode_')) if hasattr(enc, 'tag'))
        self.handlers = dict(_generate_handlers())

    def decode(self, data):
        version = struct.unpack(format.INT8, data[0])[0]
        if version != tags.VERSION:
            raise ETFDecodingError('Decode got version {0} but expects {1}'.format(version, tags.VERSION))
        return True

    def decode_term(self, data, pos):
        pass

    @tags.tag(tags.COMPRESSED)
    def decode_compressed_term(self, data, pos):
        offset = pos + 4
        ucsize = struct.unpack(format.UINT32, data[pos:offset])[0]
        csize = offset + ucsize
        return zlib.decompress(data[offset:csize])

    @tags.tag(tags.SMALL_INTEGER)
    def decode_small_integer(self, data, pos):
        offset = pos + 1
        return struct.unpack(format.INT8, data[pos:offset])[0]

    @tags.tag(tags.INTEGER)
    def decode_integer(self, data, pos):
        offset = pos + 4
        return struct.unpack(format.INT32, data[pos:offset])[0]

    @tags.tag(tags.FLOAT)
    def decode_float(self, data, pos):
        offset = pos + 4
        return struct.unpack(format.FLOAT, data[pos:offset])[0]

    @tags.tag(tags.ATOM)
    def decode_atom(self, data, pos):
        offset = pos + 2
        length = struct.unpack(format.UINT16, data[pos:offset])[0]
        return terms.Atom(data[offset:offset+length])

    @tags.tag(tags.REFERENCE)
    def decode_reference(self, data, pos):
        node, pos = self.decode_term(data, pos) #???
        offset = pos + 5
        id, creation = struct.unpack(format.ID_CREATION_PAIR, data[pos:offset])
        return terms.Reference(node, id, creation)

    @tags.tag(tags.SMALL_TUPLE)
    def decode_small_tuple(self, data, pos):
        offset = pos + 1
        arity = struct.unpack(format.INT8, data[pos:offset])[0]
        return self._decode_iterable(data[:offset], pos, arity, tuple)

    @tags.tag(tags.LARGE_TUPLE)
    def decode_large_tuple(self, data, pos):
        offset = pos + 4
        arity = struct.unpack(format.UINT32, data[pos:offset])[0]
        return self._decode_iterable(data[:offset], pos, arity, tuple)

    @tags.tag(tags.NIL)
    def decode_nil(self, data, pos):
        return [] # Can we return None here instead ??? TODO

    @tags.tag(tags.STRING)
    def decode_string(self, data, pos):
        offset = pos + 2
        length = struct.unpack(format.UINT16, data[pos:offset])[0]
        string = data[offset:offset+length]
        return [struct.unpack(format.INT8, c) for c in string]

    @tags.tag(tags.LIST)
    def decode_list(self, data, pos):
        pass

    @tags.tag(tags.BINARY)
    def decode_binary(self, data, pos):
        pass

    @tags.tag(tags.SMALL_BIG)
    def decode_small_big(self, data, pos):
        pass

    @tags.tag(tags.LARGE_BIG)
    def decode_large_big(self, data, pos):
        pass

    @tags.tag(tags.NEW_REFERENCE)
    def decode_new_reference(self, data, pos):
        pass

    @tags.tag(tags.SMALL_ATOM)
    def decode_small_atom(self, data, pos):
        pass

    @tags.tag(tags.FUN)
    def decode_fun(self, data, pos):
        pass

    @tags.tag(tags.NEW_FUN)
    def decode_new_fun(self, data, pos):
        pass

    @tags.tag(tags.EXPORT)
    def decode_export(self, data, pos):
        pass

    @tags.tag(tags.BIT_BINARY)
    def decode_bit_binary(self, data, pos):
        pass

    @tags.tag(tags.NEW_FLOAT)
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