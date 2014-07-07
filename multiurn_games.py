#!/usr/bin/env python

import numpy as np
from fractions import Fraction
from IPython.display import Latex, HTML
from utils import boolvec2int, cartprod

import scipy.misc
from scipy.misc import comb as nCk

class Urn(object) :
    """
    An urn, defined as an object containing
    a certain number of black stones and a
    certain number of white stones.
    """
    def __init__(self,b,w) :
        self.b = b
        self.w = w
    def __str__(self,b,w) :
        return 'Urn(b=%d,w=%d)' % (self.b, self.w)
    
def oneUrnP(urn) :
    """
    Calculate the probability of winning
    the one urn 'normal' form game.
    """
    nb = urn.b
    nw = urn.w
    return Fraction(sum([nCk(nb+nw-k,nw-1,exact=True) for k in range(1,nb+2,2)]),nCk(nb+nw,nw,exact=True))

class MultiUrnSolution(object) :
    """
    Provides representations of a solution to a
    multiurn game.
    """

    def __init__(self,ns) :
        self.ns = ns
        self.p=np.ones(ns,dtype=Fraction)

    def __repr__(self) :
        one_half=Fraction(1,2)
        retval = 'Solution()\n'
        if len(self.ns)==2 :
            retval += '\n'.join(' '.join('%6s' % (xx if xx!=one_half else '',) for xx in rr) for rr in self.p)
        return retval

    def _getCells(self) :
        m=2*self.ns[0]
        n=2*self.ns[1]
        cells = np.zeros((m,n),'S20')
        fmt = lambda _ : ('$\\frac{%s}{%s}$' % (_.numerator,_.denominator)) if _.denominator!=1 else ('$%s$' % _.numerator)        
        fstr=np.vectorize(fmt ,otypes=['O'])
        cells[1::2,1::2] = fstr(self.p).astype('S20') # filling the probabilities
        fU=np.vectorize(lambda _: r'$\uparrow$' if (_&2) else '',otypes=['O']) 
        cells[0::2,1::2] = fU(self.plays).astype('S20')
        fL=np.vectorize(lambda _: r'$\leftarrow$' if (_&1) else '',otypes=['O'])
        cells[1::2,0::2] = fL(self.plays).astype('S20')
        return cells
    
    def html(self) :
        """
        Return the html source for a representation
        of the solution to a 2-dimensional multiurn
        game as a table. If the game has only one urn
        or >=3 urns then bail out and return a failure
        message.
        """
        trans={r'$\uparrow$'  :u'\u2191', r'$\leftarrow$':u'\u2190'}
               
        if len(self.ns)==2 :
            m = self.ns[0]
            n = self.ns[1]
            cells = self._getCells()
            retstr = r'<table class="probgrid">'
            retstr += r'<tr><td>m\n</td>' + '<td class="header"></td>' + '<td class="header"></td>'.join('<td class="header">%s</td>' % _ for _ in range(0,n)) + r'</tr>'
            for (rowi,row) in enumerate(cells) :
                if rowi>0 and rowi%2==1 :
                    retstr += '<tr><td class="header">%d</td>' %((rowi-1)/2,)
                else :
                    retstr += '<tr><td class="header"></td>'
                retstr += ''.join(('<td>%s</td>' % trans.get(xx,xx)) for xx in row)
                retstr += '</tr>\n'
            retstr += '</table>\n'
            return retstr
        else :
            return 'Game has 1 or > 2 urns.  No HTML representation available.'
        
    def latex(self) :
        """
        Return the latex source for a representation
        of the solution to a 2-dimensional multiurn
        game as a table. If the game has only one urn
        or >=3 urns then bail out and return a failure
        message.
        """
        if len(self.ns)==2 :
            m = self.ns[0]
            n = self.ns[1]
            rowheaders = ['']*(2*n)
            rowheaders[1::2] = map(str,range(1,n+1))
            cells = self._getCells()
            retstr = '\\begin{tabular}{c|' + ('c'*(2*n)) + '}\n'
            retstr += 'm\\textbackslash n&&' + '&&'.join(map(str,range(1,n+1))) + '\\\\\n'
            retstr += '\\hline\\\\\n'
            for ir,row in enumerate(cells) :
                retstr += rowheaders[ir] + '&' + '&'.join(str(_).strip(' ') for _ in row) + '\\\\\n'
            retstr += '\\end{tabular}\n'
        else :
            retstr = 'Game has 1 or > 2 urns.  No latex representation available.'
        return retstr

def CalculateMultiUrnSolution(urns,form='misere') :
    """
    Calculate the solution to russian roulette.
    urns is a list of urn objects.  form should take the
    value 'misere' (last player to move wins) or
    'normal' (last player to move loses).
    """
    N=len(urns)
    ns  = [urn.b for urn in urns]
    nws = [urn.w for urn in urns]
    
    if not nws : nws = [1]*N
    eye=np.eye(N,dtype=Fraction)
    
    nsp1 = [_+1 for _ in ns]
    s = MultiUrnSolution(nsp1)
    
    #for move_type in ['optimal','greedy','urn_greedy'] :
    #    s.__setattr__(move_type,np.zeros(ns,int))

    plays = np.zeros(nsp1,int)
    greedy_plays = np.zeros(nsp1,int)
    urn_plays = np.zeros(nsp1,int)
    
    if form=='misere' :
        #for move_type in ['optimal','greedy','urn_greedy'] :
        #    s.__setattr__('p_'+move_type,np.ones(ns,dtype=Fraction))
        mm  = np.ones(nsp1,dtype=Fraction)
        mmg = np.ones(nsp1,dtype=Fraction)
        mmo = np.ones(nsp1,dtype=Fraction)
        #
        # Loop over all of the nodes in the game, corresponding
        # to the numbers of black stones left in each urn.
        #
        for nbs in cartprod(*map(range,nsp1)) :
            #
            # Make a tuple of the list, because we'll need it
            # frequently to index into our arrays (can't index
            # into a numpy array with a list, need a tuple.)
            #
            tnbs=tuple(nbs)
            #
            # Use three different rubrics for judging the different
            # moves available to us at this node in the game
            #
            # Greedy rubric, just judge moves based on the
            # probability of getting a white stone in this
            # move.
            #
            pi = map(lambda (nb,nw) : Fraction(nw,nb+nw), zip(nbs,nws))
            #
            # Urn-greedy.  Judge moves based on the probability
            # of winning were we and our opponent to only play
            # in the selected node.
            #
            piu = map(lambda (nb,nw) : oneUrnP(Urn(nb,nw)), zip(nbs,nws))
            #
            # Optimal.  Judge moves based on the probability that
            # we win if we start with selecting each urn.  Calculate
            # this recursively.
            #
            opts     = map(lambda (p,eyei) : 1-(1-p)*mm[tuple(nbs-eyei)], zip(pi,eye) ) 

            mm[tnbs]  = max(opts); plays[tnbs]        = boolvec2int(map(lambda _ : _== mm[tnbs],opts))
            mmg[tnbs] = max(pi);   greedy_plays[tnbs] = boolvec2int(map(lambda _ : _==mmg[tnbs],  pi))
            mmo[tnbs] = max(piu);  urn_plays[tnbs]    = boolvec2int(map(lambda _ : _==mmo[tnbs], piu))
            
    else :
        mm = np.zeros(ns,dtype=Fraction)
        for nbs in cartprod(*map(range,ns))[1:] :
            tnbs=tuple(nbs)
            pi = map(lambda (nb,nw) : Fraction(nb,nb+nw), zip(nbs,nws))
            #Uwaga - there are sometimes negative indices in nbs-eyei.
            opts = [p*(1-mm[tuple(nbs-eyei)]) if all(nbs-eyei>=0) else -1 for (p,eyei) in zip(pi,eye)]
            mm[tnbs] = max( opts )
            plays[tnbs] = boolvec2int(map(lambda _ : _==mm[tnbs],opts))
    s.p = mm
    s.pg = mmg
    s.po = mmo

    s.plays = plays
    s.greedy_plays = greedy_plays
    s.urn_plays = urn_plays
    return s
