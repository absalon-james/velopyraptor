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

import math
import operator

def generate_grays_group_by_nbits(n):
    """
    Computes the gray sequence and groups elements by the number of bits they
    contain.
    """

    def count_ones(n):
        """
        Quick function to sum the number of 1's in a binary
        represention of a number

        @ TODO -- Maybe increase to 64 bits instead of 32
        """
        s = 0
        mask = 1
        for i in xrange(32):
            if (mask << i) & n:
                s += 1
        return s

    # Function that xors a number by half of itself
    gray = lambda i: i ^ int(math.floor(i / 2.0))

    # Create a list 
    grouped_grays = [[] for i in xrange(64)]
    for i in xrange(n):
        g = gray(i)
        bits = count_ones(g)
        grouped_grays[bits].append(g)
    return grouped_grays

# Create a sequence of grays grouped by the number of bits in each gray
# The index in the the list indicates the number of bits
SEQUENCE = generate_grays_group_by_nbits(8192)
