import numpy as np
import scipy
from scipy import misc

from fractions import Fraction

def comb_frac(n,k) :
    retval = Fraction(1,1)
    for i in xrange(1,k+1) :
        retval *= Fraction(n-i+1,i)
    return retval

def multiply(a,b) :
    n = len(a)+len(b)-1
    retval = np.zeros((n,),Fraction)
    for i in xrange(n) :
        for j in xrange(i+1) :
            if j < len(a) and i-j < len(b) :
                retval[i] += a[j]*b[i-j]
    return retval

def coefficients(w) :
    """
    w white stones
    """
    mat = np.zeros((w+1,w+1),dtype=Fraction)
    for i in xrange(0,w) :
        for j in xrange(i+1) :
            mat[w-1-j,w-1-i] = comb_frac(i+1,i+1-j)*Fraction(2,1)**(i+1-j)
    mat[w,:] = Fraction(1,1)
    
    return mat
