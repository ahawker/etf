from etf import terms
import unittest

__author__ = 'ahawker'

class TestAtom(unittest.TestCase):

    def test_none_string(self):
        #uppercase
        atom = terms.Atom('None')
        self.assertIsNone(atom, 'Failed on Atom("None")')
        #lowercase
        atom = terms.Atom('none')
        self.assertIsNone(atom, 'Failed on Atom("none")')

    def test_true_string(self):
        #uppercase
        atom = terms.Atom('True')
        self.assertTrue(atom, 'Failed on Atom("True")')
        self.assertIsInstance(atom, bool)
        #lowercase
        atom = terms.Atom('true')
        self.assertTrue(atom, 'Failed on Atom("true")')
        self.assertIsInstance(atom, bool)

    def test_false_string(self):
        #uppercase
        atom = terms.Atom('False')
        self.assertFalse(atom, 'Failed on Atom("False")')
        self.assertIsInstance(atom, bool)
        #lowercase
        atom = terms.Atom('false')
        self.assertFalse(atom, 'Failed on Atom("false")')
        self.assertIsInstance(atom, bool)

    def test_none_keyword(self):
        atom = terms.Atom(None)
        self.assertEqual(str(atom), 'None', 'Failed on Atom(None)')

    def test_true_keyword(self):
        atom = terms.Atom(True)
        self.assertEqual(str(atom), 'True', 'Failed on Atom(True)')

    def test_false_keyword(self):
        atom = terms.Atom(False)
        self.assertEqual(str(atom), 'False', 'Failed on Atom(False)')

    def test_empty_string(self):
        atom = terms.Atom('')
        self.assertEqual(str(atom), '', 'Failed on Atom("")')

    def test_valid_string(self):
        name = 'AtomName'
        atom = terms.Atom(name)
        self.assertEqual(str(atom), name, 'Failed on Atom("AtomName")')

    def test_max_length_string(self):
        name = ' ' * 255
        atom = terms.Atom(name)
        self.assertEqual(str(atom), name, 'Failed on Atom("255 char string")')

    def test_invalid_length_string(self):
        self.assertRaises(ValueError, terms.Atom, ' ' * 256)

if __name__ == '__main__':
    unittest.main()
