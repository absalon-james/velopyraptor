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
import matrix
from raptor import RaptorR10

class Encoder(RaptorR10):
    """
    Encoder for producing encoded symbols
    from source symbols.  It is essentially the same as
    decoder only we decode from the source
    """

    def __init__(self, k, symbols):
        """
        Arguments:
        k       -- Integer number of source symbols
        symbols -- List of k source symbols to decode
        """
        # Use parent class to gen parameters
        super(Encoder, self).__init__(k)
        self.symbols = symbols
        self.calculate_i_symbols()

class EncoderHard(RaptorR10):
    """
    The same as the Encoder except for the option to
    produce the intermediate symbols in an extremely
    inefficient way
    """

    def __init__(self, k, symbols):
        """
        Arguments:
        k       -- Integer number of source symbols
        symbols -- List of k source symbols to decode
        """
        # Use parent class to gen parameters
        super(EncoderHard, self).__init__(k)

        self.symbols = symbols

    def calculate_i_symbols_hard(self):
        """
        Calculates list of intermediate symbols.

        This is ineffecient.  Calculates a, the inverse of a
        and then does matrix multiplication between a^-1 and d

        This WILL take a long time for larger symbolsizes

        Returns list of bit arrays representing intermediate symbols
        """
        a = self.a()
        ai = matrix.inverse(a)
        d = self.calculate_d()
        return matrix.multiply(ai, d)        
