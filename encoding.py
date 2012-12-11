__author__ = 'ahawker'

class ETFEncoder(object):
    def __init__(self, encoding='utf-8'):
        super(ETFEncoder, self).__init__()
        self.encoding = encoding

    def encode(self, data):
        pass

class ETFCodec(object):
    pass
#codec contains both encoding and decoding
#codec is created in __init__