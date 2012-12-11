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
        data = struct.pack('B', tags.VERSION)[0]
        self.assertIsNotNone(self.decoder.decode(data))

    def test_small_integer_wrong_tag(self):
        data, pos = struct.pack('BB', 0, 255), 0
        self.assertRaises(decoding.ETFDecodingError, self.decoder.decode_small_integer, data, pos)

    def test_small_integer_no_data(self):
        data, pos = None, 0
        self.assertRaises(decoding.ETFDecodingError, self.decoder.decode_small_integer, data, pos)

    def test_small_integer_negative_pos(self):
        data, pos = ['\x00' * 2], -1
        self.assertRaises(ValueError, self.decoder.decode_small_integer, data, pos)