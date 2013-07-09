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

def choose(n, r):
    """
    Quick and dirty nCr

    Arguments:
    n -- Integer n in n choose r (n should be > r)
    r -- Integer r in n choose r (r shoudl be < n)
    """
    # Factorial
    reducer = lambda x, y: x * y

    # should calculate (n!) / r!(n-r)!
    numerator = reduce(reducer, xrange(r + 1, n + 1), 1)
    denominator = reduce(reducer, xrange(1, n - r + 1), 1)
    return numerator / denominator

def generate_halves(cap):
    """
    Generates all H choose (H/2) values where H is the list index
    and the value of l(H) is H choose (H/2)

    All values of H are calculated from 1 to cap

    Arguments:
    cap -- Integer cap to limit ourselves
    """
    l = [None]
    for i in xrange(1, cap + 1):
        l.append(choose(i, int(math.ceil(i / (2.0)))))
    return l

# Maintain a list of halves for ease of use
# @TODO - Compute the first halves and keep them in a list
# so that they do not have to be computed every time this module
# is fresh imported
HALVES = generate_halves(300)

def next(n):
    """
    Search for the next half > n

    Arguments:
    n -- Integer to search
    """
    for i in xrange(1, len(HALVES)):
        if HALVES[i] > n:
            return i
    return None
