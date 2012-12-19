from etf import decoding, tags, format
import struct
import unittest
import zlib

__author__ = 'ahawker'

class TestDecoder(unittest.TestCase):

    def setUp(self):
        self.decoder = decoding.ETFDecoder()

    def test_incorrect_version(self):
        data = struct.pack('>B', 0)[0]
        self.assertRaises(decoding.ETFDecodingError, self.decoder.decode, data)

    def test_correct_version(self):
        data = tags.VERSION + tags.NIL
        self.assertIsNotNone(self.decoder.decode(data))

    def test_small_integer_wrong_tag(self):
        data, pos = chr(0), 0
        self.assertRaises(ValueError, self.decoder.decode_small_integer, chr(0) + data, pos)

    def test_small_integer_negative_pos(self):
        data, pos =  chr(0), -1
        self.assertRaises(ValueError, self.decoder.decode_small_integer, tags.SMALL_INTEGER + data, pos)

    def test_small_integer_out_of_range_data(self):
        value = 1024
        data, pos = struct.pack(format.UINT32, value), 0
        self.assertEqual(self.decoder.decode_small_integer(tags.SMALL_INTEGER + data, pos), 0)

    def test_small_integer_valid_data(self):
        value = 255
        data, pos = struct.pack(format.INT8, value), 0
        result = self.decoder.decode_small_integer(tags.SMALL_INTEGER + data, pos)
        self.assertEqual(result, value)
        self.assertTrue(isinstance(result, int))

    def test_compressed_term_wrong_tag(self):
        data, pos = struct.pack(format.UINT32, 0), 0
        self.assertRaises(ValueError, self.decoder.decode_compressed_term, chr(0) + data, pos)

    def test_compressed_term_negative_pos(self):
        data, pos = struct.pack(format.UINT32, 0), -1
        self.assertRaises(ValueError, self.decoder.decode_compressed_term, tags.COMPRESSED + data, pos)

    def test_compressed_term_zero_size(self):
        data, pos = struct.pack(format.UINT32, 0), 0
        self.assertRaises(zlib.error, self.decoder.decode_compressed_term, tags.COMPRESSED + data, pos)

    def test_compressed_term_valid_data(self):
        #need to encode a term that is large enough to be compressed
        pass

if __name__ == '__main__':
    unittest.main()