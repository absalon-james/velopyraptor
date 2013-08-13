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
import config
import copy

class Source(list):

    """
    Represents a list of string source symbols for an encoding
    """

    def __init__(self, k, symbolsize, block_id):
        """
        Block constructor
        
        Arguments:
        k          -- number of symbols
        symbolsize -- Size of each symbol in bytes
        block_id   -- id of this block
        """
        self.k = k
        self.symbolsize = symbolsize
        self.id = block_id
        self.padding = 0 # Bytes

        if config._64BIT:
            self.dtype = 'uint64'
        else:
            self.dtype = 'uint32'

    def pad(self):
        """
        Pads the block to have k symbols of each symbolsize bytes.
        Each symbol will be interepreted as an array of unsigned integers        """

        # loop through checking each symbol
        for i in xrange(len(self)):

            if len(self[i]) < self.symbolsize:
                # Add to padding
                self.padding += self.symbolsize - len(self[i])
                # Do the symbol padding
                self[i] = self[i].ljust(self.symbolsize, "\x00")

        # Add as many zero symbols as necessary to have a full block
        if len(self) < self.k:
            zeros = "\x00" * self.symbolsize
            for i in xrange(len(self), self.k):
                self.padding += self.symbolsize
                self.append(copy.copy(zeros))
