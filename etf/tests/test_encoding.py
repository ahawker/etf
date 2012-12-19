from etf import encoding, tags, terms
import struct
import unittest
import uuid
import zlib

__author__ = 'Andrew Hawker <andrew.r.hawker@gmail.com>'

class TestEncoder(unittest.TestCase):

    def setUp(self):
        self.encoder = encoding.ETFEncoder()

    def test_incorrect_version(self):
        pass

    def test_correct_version(self):
        pass

    def test_compress_too_small_term(self):
        term = self.encoder.encode_term(0)
        cterm = self.encoder.compress_term(term)
        tag = cterm[0]
        self.assertNotEqual(tag, tags.COMPRESSED)

    def test_compress_large_term(self):
        term = self.encoder.encode_term([1] * 4096)
        cterm = self.encoder.compress_term(term)
        tag = cterm[0]
        self.assertEqual(tag, tags.COMPRESSED)

    def test_small_integer_too_low(self):
        term = self.encoder.encode_integer(-1)
        tag = term[0]
        self.assertNotEqual(tag, tags.SMALL_INTEGER)
        self.assertEqual(tag, tags.INTEGER)

    def test_small_integer_lower_bound(self):
        term = self.encoder.encode_integer(0)
        tag = term[0]
        self.assertEqual(tag, tags.SMALL_INTEGER)

    def test_small_integer_valid(self):
        term = self.encoder.encode_integer(100)
        tag = term[0]
        self.assertEqual(tag, tags.SMALL_INTEGER)

    def test_small_integer_upper_bound(self):
        term = self.encoder.encode_integer(255)
        tag = term[0]
        self.assertEqual(tag, tags.SMALL_INTEGER)

    def test_small_integer_too_large(self):
        term = self.encoder.encode_integer(256)
        tag = term[0]
        self.assertNotEqual(tag, tags.SMALL_INTEGER)
        self.assertEqual(tag, tags.INTEGER)

    def test_integer_lower_bound(self):
        term = self.encoder.encode_integer(-2147483648)
        tag = term[0]
        self.assertEqual(tag, tags.INTEGER)

    def test_integer_valid(self):
        term = self.encoder.encode_integer(4096)
        tag = term[0]
        self.assertEqual(tag, tags.INTEGER)

    def test_integer_upper_bound(self):
        term = self.encoder.encode_integer(2147483647)
        tag = term[0]
        self.assertEqual(tag, tags.INTEGER)

    def test_atom_false(self):
        term = self.encoder.encode_atom(False)
        tag = term[0]
        self.assertEqual(tag, tags.ATOM)

    def test_atom_true(self):
        term = self.encoder.encode_atom(True)
        tag = term[0]
        self.assertEqual(tag, tags.ATOM)

    def test_atom_none(self):
        term = self.encoder.encode_atom(None)
        tag = term[0]
        self.assertEqual(tag, tags.ATOM)

    def test_atom_name_lower_bound(self):
        term = self.encoder.encode_atom(terms.Atom(''))
        tag = term[0]
        self.assertEqual(tag, tags.ATOM)

    def test_atom_name_upper_bound(self):
        term = self.encoder.encode_atom(terms.Atom(' ' * 255))
        tag = term[0]
        self.assertEqual(tag, tags.ATOM)

    def test_atom_valid_name(self):
        term = self.encoder.encode_atom(terms.Atom('AtomName'))
        tag = term[0]
        self.assertEqual(tag, tags.ATOM)

    def test_float_zero(self):
        term = self.encoder.encode_float(terms.Float(0))
        tag = term[0]
        self.assertEqual(tag, tags.FLOAT)

    def test_float_negative(self):
        term = self.encoder.encode_float(terms.Float(1))
        tag = term[0]
        self.assertEqual(tag, tags.FLOAT)

    def test_float_valid(self):
        term = self.encoder.encode_float(terms.Float(4098))
        tag = term[0]
        self.assertEqual(tag, tags.FLOAT)

    def test_new_float_zero(self):
        self.encoder.minor_version = 1
        term = self.encoder.encode_new_float(terms.NewFloat(0))
        tag = term[0]
        self.assertEqual(tag, tags.NEW_FLOAT)

    def test_new_float_negative(self):
        term = self.encoder.encode_new_float(terms.NewFloat(1))
        tag = term[0]
        self.assertEqual(tag, tags.NEW_FLOAT)

    def test_new_float_valid(self):
        term = self.encoder.encode_new_float(terms.NewFloat(4096))
        tag = term[0]
        self.assertEqual(tag, tags.NEW_FLOAT)

    def test_new_float_builtin_zero(self):
        self.encoder.minor_version = 1
        term = self.encoder.encode_new_float(float(0))
        tag = term[0]
        self.assertEqual(tag, tags.NEW_FLOAT)

    def test_new_float_builtin_negative(self):
        term = self.encoder.encode_new_float(float(1))
        tag = term[0]
        self.assertEqual(tag, tags.NEW_FLOAT)

    def test_new__float_builtin_valid(self):
        term = self.encoder.encode_new_float(float(4096))
        tag = term[0]
        self.assertEqual(tag, tags.NEW_FLOAT)

    def test_small_tuple_empty(self):
        term = self.encoder.encode_tuple(tuple())
        tag = term[0]
        self.assertEqual(tag, tags.SMALL_TUPLE)

    def test_small_tuple_one_item(self):
        term = self.encoder.encode_tuple((1,))
        tag = term[0]
        self.assertEqual(tag, tags.SMALL_TUPLE)

    def test_small_tuple_max_items(self):
        term = self.encoder.encode_tuple((0,) * 255)
        tag = term[0]
        self.assertEqual(tag, tags.SMALL_TUPLE)

    def test_large_tuple_min_items(self):
        term = self.encoder.encode_tuple((0,) * 256)
        tag = term[0]
        self.assertEqual(tag, tags.LARGE_TUPLE)

    def test_large_tuple_many_items(self):
        term = self.encoder.encode_tuple((0,) * 4096)
        tag = term[0]
        self.assertEqual(tag, tags.LARGE_TUPLE)

    def test_list_empty(self):
        term = self.encoder.encode_list([])
        tag = term[0]
        self.assertEqual(tag, tags.NIL)

    def test_list_one_item(self):
        term = self.encoder.encode_list([1])
        tag = term[0]
        self.assertEqual(tag, tags.LIST)

    def test_list_many_items(self):
        term = self.encoder.encode_list([1] * 4096)
        tag = term[0]
        self.assertEqual(tag, tags.LIST)

    def test_reference_valid(self):
        ref = terms.Reference(terms.Atom(True), 0, 0)
        term = self.encoder.encode_reference(ref)
        tag = term[0]
        self.assertEqual(tag, tags.REFERENCE)

    def test_new_reference_one_id(self):
        ref = terms.NewReference(terms.Atom(True), 0, 0)
        term = self.encoder.encode_new_reference(ref)
        tag = term[0]
        self.assertEqual(tag, tags.NEW_REFERENCE)

    def test_new_reference_many_ids(self):
        ref = terms.NewReference(terms.Atom(True), 0, *((0,) * 4096))
        term = self.encoder.encode_new_reference(ref)
        tag = term[0]
        self.assertEqual(tag, tags.NEW_REFERENCE)

    def test_port_valid(self):
        port = terms.Port(terms.Atom(True), 0, 0)
        term = self.encoder.encode_port(port)
        tag = term[0]
        self.assertEqual(tag, tags.PORT)

    def test_pid_valid(self):
        pid = terms.Pid(terms.Atom(True), 0, 0, 0)
        term = self.encoder.encode_pid(pid)
        tag = term[0]
        self.assertEqual(tag, tags.PID)

    def test_string_empty(self):
        term = self.encoder.encode_string(terms.String(''))
        tag = term[0]
        self.assertEqual(tag, tags.STRING)

    def test_string_valid(self):
        term = self.encoder.encode_string(terms.String('HelloWorld'))
        tag = term[0]
        self.assertEqual(tag, tags.STRING)

    def test_string_max_length(self):
        term = self.encoder.encode_string(terms.String(' ' * 65535))
        tag = term[0]
        self.assertEqual(tag, tags.STRING)

    def test_string_too_long(self):
        term = self.encoder.encode_string(terms.String(' ' * 65536))
        tag = term[0]
        self.assertEqual(tag, tags.LIST)

    def test_string_builtin_empty(self):
        term = self.encoder.encode_string(unicode(''))
        tag = term[0]
        self.assertEqual(tag, tags.STRING)

    def test_string_builtin_valid(self):
        term = self.encoder.encode_string(unicode('HelloWorld'))
        tag = term[0]
        self.assertEqual(tag, tags.STRING)

    def test_string_builtin_max_length(self):
        term = self.encoder.encode_string(unicode(' ' * 65535))
        tag = term[0]
        self.assertEqual(tag, tags.STRING)

    def test_string_builtin_too_long(self):
        term = self.encoder.encode_string(unicode(' ' * 65536))
        tag = term[0]
        self.assertEqual(tag, tags.LIST)

    def test_binary_empty(self):
        term = self.encoder.encode_binary(terms.Binary(''))
        tag = term[0]
        self.assertEqual(tag, tags.BINARY)

    def test_binary_valid(self):
        term = self.encoder.encode_binary(terms.Binary('HelloWorld'))
        tag = term[0]
        self.assertEqual(tag, tags.BINARY)

    def test_binary_builtin_empty(self):
        term = self.encoder.encode_binary(str(''))
        tag = term[0]
        self.assertEqual(tag, tags.BINARY)

    def test_binary_builtin_valid(self):
        term = self.encoder.encode_binary(str('HelloWorld'))
        tag = term[0]
        self.assertEqual(tag, tags.BINARY)

    def test_bit_binary_empty(self):
        term = self.encoder.encode_bit_binary(terms.BitBinary('', 0))
        tag = term[0]
        self.assertEqual(tag, tags.BIT_BINARY)

    def test_bit_binary_valid(self):
        term = self.encoder.encode_bit_binary(terms.BitBinary('HelloWorld', 1))
        tag = term[0]
        self.assertEqual(tag, tags.BIT_BINARY)

    def test_export_valid(self):
        export = terms.Export(terms.Atom('Module'), terms.Atom('Function'), 3)
        term = self.encoder.encode_export(export)
        tag = term[0]
        self.assertEqual(tag, tags.EXPORT)

    def test_fun_valid(self):
        pid = terms.Pid(terms.Atom('Pid'), 0, 0, 0)
        module = terms.Atom('Module')
        fun = terms.Function(pid, module, 0, 1, terms.Atom('Var1'))
        term = self.encoder.encode_fun(fun)
        tag = term[0]
        self.assertEqual(tag, tags.FUN)

    def test_new_fun_valid(self):
        size = 0
        arity = 0
        uniq = uuid.uuid4().int
        index = 0
        module = terms.Atom('Module')
        oldindex = 0
        olduniq = 0
        pid = terms.Pid(terms.Atom('Pid'), 0, 0, 0)
        vars = (terms.Atom('Var1'), terms.Atom('Var2'))
        fun = terms.NewFunction(size, arity, uniq, index, module, oldindex, olduniq, pid, vars)
        term = self.encoder.encode_new_fun(fun)
        tag = term[0]
        self.assertEqual(tag, tags.NEW_FUN)

    def test_small_big_positive_byte(self):
        term = self.encoder.encode_big(long(2**8-1))
        tag = term[0]
        sign = ord(term[2])
        self.assertEqual(tag, tags.SMALL_BIG)
        self.assertEqual(sign, 0)

    def test_small_big_negative_byte(self):
        term = self.encoder.encode_big(long(-2**8-1))
        tag = term[0]
        sign = ord(term[2])
        self.assertEqual(tag, tags.SMALL_BIG)
        self.assertEqual(sign, 1)

    def test_small_big_positive_short(self):
        term = self.encoder.encode_big(long(2**16-1))
        tag = term[0]
        sign = ord(term[2])
        self.assertEqual(tag, tags.SMALL_BIG)
        self.assertEqual(sign, 0)

    def test_small_big_negative_short(self):
        term = self.encoder.encode_big(long(-2**16-1))
        tag = term[0]
        sign = ord(term[2])
        self.assertEqual(tag, tags.SMALL_BIG)
        self.assertEqual(sign, 1)

    def test_small_big_positive_int(self):
        term = self.encoder.encode_big(long(2**32-1))
        tag = term[0]
        sign = ord(term[2])
        self.assertEqual(tag, tags.SMALL_BIG)
        self.assertEqual(sign, 0)

    def test_small_big_negative_int(self):
        term = self.encoder.encode_big(long(-2**32-1))
        tag = term[0]
        sign = ord(term[2])
        self.assertEqual(tag, tags.SMALL_BIG)
        self.assertEqual(sign, 1)

    def test_small_big_positive_max(self):
        term = self.encoder.encode_big(long(255**255))
        tag = term[0]
        sign = ord(term[2])
        self.assertEqual(tag, tags.SMALL_BIG)
        self.assertEqual(sign, 0)

    def test_small_big_negative_max(self):
        term = self.encoder.encode_big(long(-255**255))
        tag = term[0]
        sign = ord(term[2])
        self.assertEqual(tag, tags.SMALL_BIG)
        self.assertEqual(sign, 1)

    def test_large_big_positive_min(self):
        term = self.encoder.encode_big(long(256**256))
        tag = term[0]
        sign = ord(term[2])
        self.assertEqual(tag, tags.LARGE_BIG)
        self.assertEqual(sign, 0)

    def test_large_big_negative_min(self):
        term = self.encoder.encode_big(long(-256**256))
        tag = term[0]
        sign = ord(term[2])
        self.assertEqual(tag, tags.LARGE_BIG)
        self.assertEqual(sign, 1)

    def test_large_big_positive_very_large(self):
        term = self.encoder.encode_big(long(1024**10000))
        tag = term[0]
        sign = ord(term[2])
        self.assertEqual(tag, tags.LARGE_BIG)
        self.assertEqual(sign, 0)

    def test_large_big_negative_very_small(self):
        term = self.encoder.encode_big(long(-1024**10000))
        tag = term[0]
        sign = ord(term[2])
        self.assertEqual(tag, tags.LARGE_BIG)
        self.assertEqual(sign, 1)


if __name__ == '__main__':
    unittest.main()