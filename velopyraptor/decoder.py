"""
Copyright [2013] [James Absalon]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from raptor import RaptorR10

class Decoder(RaptorR10):
    """
    Instances of this class take a known set of encoding symbols
    and id's and decodes the intermediate symbols.

    To get the source symbols, just decoded the first k encoding
    symbols
    """

    def __init__(self, k, symbols=None):
        """
        Arguments:
        block -- Block with set k and symbol size.  Each of the block's
                 k symbols should be the same size

        Keyword Arguments:
        symbols -- Optional list of symbols to initialize the
                   decoder with.
        """
        # Use parent class to gen parameters
        super(Decoder, self).__init__(k)
        if symbols is None:
            symbols = []
        self.symbols = symbols

    def append(self, symbol_tuple):
        """
        Appends another symbol to the decoder.

        Argument:
        symbol_tuple -- Should be a 2 tuple (Integer id, Bitarray symbol)
        """
        self.symbols.append(symbol_tuple)
        return self.can_decode()

    def decode(self):
        """
        Nice way of saying decode the intermediate symbols
        Difference between the encoder and the decoder
        is that you choose when to decode with the decoder
        """
        super(Decoder, self).calculate_i_symbols()
