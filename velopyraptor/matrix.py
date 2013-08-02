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

The methods contained within this module are designed to facilitate
matrix operations over GF(2).  I did consider numpy, but I believe
numpy to use 8 bit booleans.  When our symbol sizes easily exceed 10 MB
it makes sense to use bitarrays which fit 8 booleans into one byte.
"""
import copy
from bitarray import bitarray

def zeros(n, m):
    """
    Creates a zero n by m matrix    
    Arguments:
    n -- Integer number of rows
    m -- Integer number of columns 
    """
    matrix = []
    for i in xrange(n):
        ba = bitarray(m)
        ba.setall(False)
        matrix.append(ba)
    return matrix

def identity(n):
    """
    Creates an n by n identity matrix
    Arguments:
    n -- Integer indicates rows and columns
    """

    matrix = []
    for i in xrange(n):
        ba = bitarray(n)
        ba.setall(False)
        ba[i] = True
        matrix.append(ba)
    return matrix

def inverse(a):
    """
    Calculates the inverse of a (n x n)matrix over GF(2)
    The n x n identity matrix is adjoined to a and then gaussian elimination
    is performed to produce first an upper triangular matrix.
    Gaussian elimination is further used to produce an nxn identity matrix
    over the side that was originally a.  The right should is then the inverse

    @TODO - Add check for invertible matrices

    Arguments:
    a - n array of n sized bitarray
    """
    # Check dimensions.  Matrix must be square
    size = len(a)
    if not (size == len(a[0])):
        raise Exception("Tried to invert a %s by %s matrix. Matrix must be square" % (size, len(a[0])))

    # We dont want to change a
    a = copy.deepcopy(a)

    id = identity(size)
    for i in xrange(size):
        a[i] += id[i]

    # First produce the upper triangular matrix (1's in the diangonal
    # and 0's below
    for i in xrange(size):

        # First swap row i for a lower low if a[i][i] is not 1
        if not a[i][i]:
            # Look for rows BENEATH row i
            for j in xrange(i + 1, size):
                if a[j][i]:
                    temp = a[i]
                    a[i] = a[j]
                    a[j] = temp
                    break

        # XOR row i to all rows > i where a[i][j] = 1
        for j in xrange(i + 1, size):
            if a[j][i]:
                a[j] ^= a[i]

    # We should have 1s for the diagonal and all 0s
    for i in xrange(size):
        if not a[i][i]:
            raise Exception("Tried to invert invertible matrix.  Matrix does not have ones in diagonal in upper triangular form")

    # start at bottom right and XOR rows to rows above
    # to get rid of 1's
    for i in xrange(size):
        for j in xrange(i + 1, size):
            if a[size - j - 1][size - i - 1]:
                a[size - j - 1] ^= a[size - i - 1]

    # Git rid of original a(now a diagonal) and return the right side
    for i in xrange(size):
        a[i] = a[i][size:]
    return a

def multiply(a, b):
    """
    Multiplies (x by n) matrix a by (n by y) matrix b over GF(2)
    Will produce a (x by y) matrix

    Arguments:
    a -- x sized array of n sized bitarrays
    b -- n sized array of y bitarrays
    """

    x = len(a)
    n = len(a[0])
    y = len(b[0])
    if not (n == len(b)):
        raise Exception("Attempted to multiply %s by %s matrix a by %s by %s matrix b" % (x, n, len(b), y))

    # Init matrix
    matrix = []

    for i in xrange(x):
        row = bitarray(y)
        row.setall(False)
        for j in xrange(y):
            for k in xrange(n):
                row[j] ^= a[i][k] & b[k][j]
        matrix.append(row)
    return matrix

def rank(a):
    """
    Determines the rank of bit matrix a

    Arguments:
    a -- List of even length bitarrays
    """

    m = copy.deepcopy(a)
    rows = len(m)

    for i in xrange(rows):

        # Swap a row with a one into position i, i
        if not m[i][i]:
            for j in xrange(i + 1, rows):
                if m[j][i]:
                    m[i] ^= m[j]
                    m[j] ^= m[i]
                    m[i] ^= m[j]
                    break

        # loop down xoring all rows beneath the pivot
        for j in xrange(i + 1, rows):
            if m[j][i]:
                m[j] ^= m[i]

    # Look and xor duplicate rows
    for i in xrange(rows):
        for j in xrange(i + 1, rows):
            if m[i] == m[j]:
                m[j] ^= m[i]

    # count th enumber of non zero rows
    rank = 0
    for row in m:
        if row.count():
            rank += 1
    return rank
