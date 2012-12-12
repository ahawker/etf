import decoding
import struct
import tags
import unittest

__author__ = 'ahawker'

class TestDecoder(unittest.TestCase):

    def setUp(self):
        self.decoder = decoding.ETFDecoder()

    def test_incorrect_version(self):
        data = struct.pack('B', 0)[0]
        self.assertRaises(decoding.ETFDecodingError, self.decoder.decode, data)

    def test_correct_version(self):
        data = struct.pack('B', tags.VERSION)
        self.assertIsNotNone(self.decoder.decode(data))

    def test_small_integer_wrong_tag(self):
        data, pos = struct.pack('BB', 0, 255), 0
        self.assertRaises(ValueError, self.decoder.decode_small_integer, data, pos)

    def test_small_integer_no_data(self):
        data, pos = None, 0
        self.assertRaises(ValueError, self.decoder.decode_small_integer, data, pos)

    def test_small_integer_negative_pos(self):
        data, pos = struct.pack('BB', tags.SMALL_INTEGER, 0), -1
        self.assertRaises(ValueError, self.decoder.decode_small_integer, data, pos)

    def test_small_integer_valid_data(self):
        value = 255
        data, pos = struct.pack('>BB', tags.SMALL_INTEGER, value), 0
        self.assertEqual(self.decoder.decode_small_integer(data, pos), value)

    def test_small_integer_out_of_range_data(self):
        value = 1024
        data, pos = struct.pack('>BI', tags.SMALL_INTEGER, value), 0
        self.assertEqual(self.decoder.decode_small_integer(data, pos), 0)