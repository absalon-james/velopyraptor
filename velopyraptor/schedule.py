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


class Schedule(object):
    """
    Class is used to keep track of operations on a matrix that can
    be mirrored onto another matrix
    """

    def __init__(self, l, m):
        """
        Initializes the sequences c and d

        Arguments:
        l -- Integer combined h + s + k(number of source symbols)
        m -- Integer combined h + s + n(number of encoding symbols.
             n should be >= k)
        """
        # Let c[0] = 0, c[1] = 1,...,c[L-1] = L-1
        self.c = range(l)

        # Let d[0] = 0, d[1] = 1,...,d[M-1] = M-1
        self.d = range(m)

        # Init xors to empty list
        self.xors = []

    def xor(self, r1, r2):
        """
        Indicates r2 is xored into r1.  Appends a tuple(d[r2], d[r1])
        to the list of xors
        Ordering of r1, r2 DOES matter

        Arguments:
        r1 -- Integer indicating target row
        r2 -- Integer indicating source row
        """
        self.xors.append((self.d[r2], self.d[r1]))

    def exchange_row(self, r1, r2):
        """
        Indicates row r1 is swapped with row r2
        Ordering of r1, r2 DOES NOT matter

        Arguments:
        r1 -- Integer first row to swap
        r2 -- Integer second row to swap
        """
        swap = self.d[r1]
        self.d[r1] = self.d[r2]
        self.d[r2] = swap

    def exchange_column(self, c1, c2):
        """
        Indicates column c1 is swapped with column c2.
        Ordering of c1, c2 DOES NOT matter.

        Arguments:
        c1 -- Integer first column to swap
        c2 -- Integer second column to swap
        """
        swap = self.c[c1]
        self.c[c1] = self.c[c2]
        self.c[c2] = swap
