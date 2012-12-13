from etf import decoding, tags
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
        data = struct.pack('>B', tags.VERSION)
        self.assertIsNotNone(self.decoder.decode(data))

    def test_small_integer_wrong_tag(self):
        data, pos = struct.pack('>BB', 0, 0), 0
        self.assertRaises(ValueError, self.decoder.decode_small_integer, data, pos)

    def test_small_integer_negative_pos(self):
        data, pos = struct.pack('>BB', tags.SMALL_INTEGER, 0), -1
        self.assertRaises(ValueError, self.decoder.decode_small_integer, data, pos)

    def test_small_integer_out_of_range_data(self):
        value = 1024
        data, pos = struct.pack('>BI', tags.SMALL_INTEGER, value), 0
        self.assertEqual(self.decoder.decode_small_integer(data, pos), 0)

    def test_small_integer_valid_data(self):
        value = 255
        data, pos = struct.pack('>BB', tags.SMALL_INTEGER, value), 0
        result = self.decoder.decode_small_integer(data, pos)
        self.assertEqual(result, value)
        self.assertTrue(isinstance(result, int))

    def test_compressed_term_wrong_tag(self):
        data, pos = struct.pack('>BI', 0, 0), 0
        self.assertRaises(ValueError, self.decoder.decode_compressed_term, data, pos)

    def test_compressed_term_negative_pos(self):
        data, pos = struct.pack('>BI', tags.COMPRESSED, 0), -1
        self.assertRaises(ValueError, self.decoder.decode_compressed_term, data, pos)

    def test_compressed_term_zero_size(self):
        data, pos = struct.pack('>BI', tags.COMPRESSED, 0), 0
        self.assertRaises(zlib.error, self.decoder.decode_compressed_term, data, pos)

    def test_compressed_term_valid_data(self):
        #need to encode a term that is large enough to be compressed
        pass
