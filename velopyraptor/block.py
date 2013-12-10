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
import numpy
import config


class Source(list):

    """
    Represents a list of unsigned integer arrays that are the source symbols
    for an encoding
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
        # Bytes
        self.padding = 0

        if config._64BIT:
            self.dtype = 'uint64'
        else:
            self.dtype = 'uint32'

    def pad(self):
        """
        Pads the block to have k symbols of each symbolsize bytes.
        Each symbol will be interepreted as an array of unsigned integers
        """

        # loop through checking each symbol
        for i in xrange(len(self)):

            # Look for strings that are not numpy arrays
            if not isinstance(self[i], numpy.ndarray):

                # Figure out padding if any
                difference = self.symbolsize - len(self[i])
                self.padding += difference
                self[i] += b'\x00' * difference

                # Convert to numpy array
                self[i] = numpy.fromstring(self[i], dtype=self.dtype)

        # Add as many zero symbols as necessary to have a full block
        for i in xrange(len(self), self.k):
            src = b'\x00' * self.symbolsize
            self.padding += self.symbolsize
            array = numpy.fromstring(src, dtype=self.dtype)
            self.append(array)
