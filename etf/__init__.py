__author__ = 'Andrew Hawker <andrew.r.hawker@gmail.com>'
__version__ = '0.0.1'
__all__ = ['ETFEncoder', 'ETFDecoder', 'load', 'loads', 'dump', 'dumps']

from .encoding import ETFEncoder
from .decoding import ETFDecoder

encode = ETFEncoder().encode
decode = ETFDecoder().decode

def load(fp):
    return loads(fp.read())

def loads(s):
    return decode(s)

def dump(obj, fp):
    fp.write(dumps(obj))

def dumps(obj, compress=False):
    return encode(obj, compress)