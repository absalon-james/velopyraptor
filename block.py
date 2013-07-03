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
from bitarray import bitarray

class Source(list):

    """
    Represents a list of bitarrays that are the source symbols
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
        self.padding = 0 # Bytes
