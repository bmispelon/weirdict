import unittest
from weirdict.examples import CaseInsensitiveDict, TruncatedKeyDict, ModuloKeyDict

class CaseInsensitiveTestCase(unittest.TestCase):
    def setUp(self):
        self.d = CaseInsensitiveDict(foo='bar')
    
    def test_keyfunc_passthrough(self):
        self.d[42] = 'bar'
        self.assertEqual(self.d[42], 'bar')
    
    def test_getitem(self):
        self.assertEqual(self.d['FOO'], 'bar')
    
    def test_setitem(self):
        self.d['BAR'] = 'baz'
        self.assertEqual(self.d['bar'], 'baz')
    
    def test_delitem(self):
        del self.d['FOO']
        with self.assertRaises(KeyError):
            self.d['foo']
    
    def test_update_new_key(self):
        self.d.update({'bar': 'baz', 'BAZ': 'quux'})
        self.assertEqual(self.d['bar'], 'baz')
        self.assertEqual(self.d['baz'], 'quux')
    
    def test_update_overwrite(self):
        self.d.update({'FOO': 'baz'})
        self.assertEqual(self.d['foo'], 'baz')
    
    def test_setdefault(self):
        self.d.setdefault('FOO', 'baz')
        self.assertEqual(self.d['foo'], 'bar')


class TruncatedTestCase(unittest.TestCase):
    def setUp(self):
        self.d = TruncatedKeyDict(3, foo='bar')
    
    def test_zero_keylength(self):
        d = TruncatedKeyDict(0, foo='bar', bar='baz')
        self.assertEqual(d['foo'], 'baz')
        self.assertEqual(d[''], 'baz')
    
    def test_basic(self):
        self.assertEqual(self.d['fooXXX'], 'bar')
    
    def test_copy(self):
        d = self.d.copy()
        self.assertEqual(d['fooXXX'], 'bar')


class ModuloTestCase(unittest.TestCase):
    def setUp(self):
        self.d = ModuloKeyDict(10, {2: 'bar'})
    
    def test_basic(self):
        self.assertEqual(self.d[42], 'bar')
    
    def test_copy(self):
        d = self.d.copy()
        self.assertEqual(d[42], 'bar')
