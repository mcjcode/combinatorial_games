#!/usr/bin/env

def printIndent(s,lvl) :
    """
    Print the \n separated lines in the
    string s, indented lvl levels.
    """
    for line in s.split('\n') :
        print('%s%s' % ('  '*lvl,line))
        
class SCG(list) :
    @staticmethod
    def nimPile(size) :
        return SCG(map(SCG.nimPile,range(size)))
    
    @staticmethod
    def joinOr(g1, g2) :
        return SCG([SCG.joinOr(g,g2) for g in g1] + \
                   [SCG.joinOr(g1,g) for g in g2])
    @staticmethod
    def sum(games) :
        return SCG(__builtin__.sum(games,SCG([])))
        
    @staticmethod
    def nim(sizes) :
        return SCG.sum(map(SCG.nimPile,sizes))

    def solve(self) :
        """
        Return a winning move for the first
        player, or None, if there is none
        """
        for g in self :
            if not g.solve() :
                return g
        return None
        
    def solveAll(self) :
        """
        Return a list of the winning moves for
        the first player.
        """
        return [g for g in self if not g.solveAll()]

    def __add__(self,rhs) :
        return SCG.joinOr(self,rhs)
        
    pass

class ACG(object) :
    """
    A class for modelling asymmetric
    combinatorial games
    """
    def __init__(self,L,R) :
        """
        Construct a combinatorial game
        for where the left hand moves
        are given by the list L and the
        right hand moves are given by
        the list R
        """
        self.Llist = lambda : L
        self.Rlist = lambda : R
    
    def Tie(self) :
        """
        Override this method in your game to check
        whether the game is currently in a tie
        state.
        """
        return False

    def L(self) :
        return self.Llist
    
    def R(self) :
        return self.Rlist
    
    def solveL(self,level=-1) :
        """
        Find a winning move for L, if one exists,
        otherwise return None.
        """
        for g in self.L() :
            if level >= 0 :
                printIndent('%s' % (g,),level=level)
                print            
            if g.solveR(level=(level+1) if level>=0 else level) is None :               
                return g
        return None
    
    def leafL(self) :
        return len(self.L()) == 0
    
    def leafR(self) :
        return len(self.R()) == 0

    def leafScore(self) :
        """
        For end positions (leaves), return the score
        of the position, positive is good for Left,
        negative is good for Right.  Override this for
        your specific game.
        """
        return 0
        
    def scoreL(self) :
        """
        Return the score of the game if L is the
        next to move.  L looks for high scores.
        """
        if self.leafL() :
            return (self.leafScore(),self)
        else :
            return max(g.scoreR()+(g,) for g in self.L())
    
    def scoreR(self) :
        """
        Return the score of the game if R is the
        next to move.  R looks for low scores
        """
        if self.leafR() :
            return (self.leafScore(),self)
        else :
            return min(g.scoreL()+(g,) for g in self.R())
            
    def playL(self,level=-1) :
        """
        Find a winning move for L, if one exists,
        a Tie move if there is no winning move,
        and just any old move if there is no winning
        or tying.
        """
        g = None
        if level >= 0 :
            level += 1
        for g in self.L() :
            if level>=0 :
                printIndent('%s' % (g,),level=level)
                print            
            if g.playR(level) == None and not g.Tie() :
                return g
        for g in self.L() :
            if g.playR(level) == None and g.Tie() :
                return g
        return g
    
    def solveR(self,level=-1) :
        """
        Find a winning move for R, if one exists,
        otherwise return None.
        """
        for g in self.R():
            if level>=0 :
                printIndent('%s' % (g,),level=level)
                print            
            if g.solveL(level=(level+1) if level>=0 else level) is None :
                return g
        return None
    
    def playR(self,level=-1) :
        """
        Find a winning move for R, if one exists,
        a Tie move if there is no winning move,
        and just any old move if there is no winning
        or tying.
        """
        g = None
        if level >= 0 :
            level += 1
        for g in self.R():
            if level>=0 :
                printIndent('%s' % (g,),level=level)
                print
            if g.playL(level) == None and not g.Tie() :
                return g

        for g in self.R():
            if g.playL(level) == None and g.Tie():
                return g
        return g
