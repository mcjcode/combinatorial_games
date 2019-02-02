import numpy as np
import itertools
from itertools import combinations

def F(N,k=0) :
    """
    Applying the persistence algorithm,
    how many cards do we expect to correctly
    guess out of N, given that there are already
    k that we won't get to attempt to guess.
    """
    accum = 0.0
    for i in xrange(1,N+1-k) :
        accum += (1.0+F(N-1,k+i-1))/N
    return accum

def ipartitions(N,k) :
    if N <= 0 :
        yield ()
    else :
        for i in xrange(k,0,-1) :
            for part in ipartitions(N-i,min(N-i,i)) :
                yield (float(i),) + part

def P(N,L) :
    """
    Returns P(1 \notin s(1),...s(L1) and
              2 \notin s(L1+1),...,s(L1+L2) and
              ...
              k \notin s(L1+...+Lk-1),...s(L1+...+Lk)
    where s is a random permutation of N distinct things.
    
    Calculation proceeds via inclusion-exclusion
    """
    accum = 0.0
    sign = 1.0
    for i in xrange(len(L)+1) :
        accum2 = 0.0
        for combin in combinations(L,i) :
            term = 1.0
            j = 0.0
            for Li in combin :
                term *= Li/(N-j)
                j += 1
            accum2 += term
        accum += sign*accum2
        sign *= -1.0
    return accum
