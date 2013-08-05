"""
This is in no way finished.  Started with the idea of producing only linearly
independent symbols.  This symbol generator seems to be able to only find
k + 1 linearly independent symbols.

This is a heavy handed and SLOW approach to findining optimal symbols.
When finished, this should only be used to produce look up tables
"""

import copy
import itertools
import matrix
from raptor import RaptorR10 as raptor

def gen_esis(k, cap=50000):

    xors = 2
    esis = []
    i = -1
    
    # Create an encoder
    r = raptor(k)

    # Create the first two sections of matrix a
    ldpc = r.ldpc_section()
    hdpc = r.hdpc_section()
    suba = ldpc + hdpc

    # Start the collection
    a = copy.deepcopy(suba)
    while len(a) < r.l:
        i = (i + 1) % cap
        if not i:
            xors += 1
            print "Increasing xors to %s" % xors

        ba = r.lt_row(i)
        if ba.count() == xors:
            a.append(ba)
            if matrix.rank(a) == len(a):
                esis.append(i)
            else:
                a.pop()

    # We should k esis now
    assert len(esis) is k

    while len(esis) < k * 4 and xors < r.l:
        i = (i + 1) % cap
        if not i:
            xors += 1
            print "Increasing xors to %s" % xors
      
        if check_esi(r, suba, esis, xors, i):
            esis.append(i)
    return esis

def check_esi(r, suba, esis, xors, i):

    ba = r.lt_row(i)
    if not (ba.count() == xors):
        return False

    possible_esis = [i] + esis
    seqs = itertools.combinations(possible_esis, r.k)

    for seq in seqs:
        a = suba + [r.lt_row(s) for s in seq]
        if matrix.rank(a) < r.l:
            return False
    return True
