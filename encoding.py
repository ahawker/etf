import format
import struct
import tags
import terms
import zlib

__author__ = 'ahawker'

class ETFEncodingError(Exception):
    pass

class ETFEncoder(object):
    def __init__(self):
        super(ETFEncoder, self).__init__()

    def encode(self, data):
        pass

    def encode_term(self, data):
        pass

    def encode_compressed_term(self, data):
        pass

    def encode_small_integer(self, data):
        pass

    def encode_integer(self, data):
        pass

    def encode_float(self, data):
        pass

    def encode_atom(self, data):
        pass

    def encode_reference(self, data):
        pass

    def encode_small_tuple(self, data):
        pass

    def encode_large_tuple(self, data):
        pass

    def encode_nil(self, data):
        pass

    def encode_string(self, data):
        pass

    def encode_list(self, data):
        pass

    def encode_binary(self, data):
        pass

    def encode_small_big(self, data):
        pass

    def encode_large_big(self, data):
        pass

    def encode_new_reference(self, data):
        pass

    def encode_small_atom(self, data):
        pass

    def encode_fun(self, data):
        pass

    def encode_new_fun(self, data):
        pass

    def encode_export(self, data):
        pass

    def encode_bit_binary(self, data):
        pass

    def encode_new_float(self, data):
        pass

if __name__ == '__main__':
    e = ETFEncoder()
    pass