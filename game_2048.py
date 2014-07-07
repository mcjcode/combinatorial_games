class Game2048_orig(object) :

    def __init__(self,shape) :
        self.board = np.zeros(shape,int)
        
        self.idxs = np.array(np.fromfunction(lambda*_:_,self.board.shape),int)
        self.idxs = self.idxs.transpose(range(1,len(shape)+1)+[0,])
        self.idxs = self.idxs.reshape([np.product(shape)]+[len(shape)])
        self.score = 0
        self.randomBlank()
    
    def __str__(self) :
        return str(self.board) + '\n' + 'Score: %d' % (self.score,)

    @classmethod
    def compress(cls,Lin) :
        score=0
        n = len(Lin)
        L = [xx for xx in Lin if xx!=0]
        i = 0
        while i < len(L)-1 :
            if L[i]==L[i+1] :
                L[i]=2*L[i]
                score += L[i]
                del L[i+1]
            i += 1
        L.extend([0]*(n-len(L)))
        return (L, score)

    def move(self,axis,sgn) :
        B,score = Game2048.tryMove(self.board,axis,sgn)
        self.board = B
        self.score += score
    
    def checkLose(self) :
        """
        Check whether the player has lost.
        """
        #
        # Perhaps this can be done more efficiently,
        # but for now, try all of the possible moves,
        # and as soon as we find one that does something,
        # bail out.  If we don't find one, we've lost,
        # so return True
        #
        
        return len(self.availableMoves())==0
    
    def availableMoves(self) :
        retval = []
        for axis in range(len(self.board.shape)) :
            for sgn in [+1,-1] :
                B, score = Game2048.tryMove(self.board,axis,sgn)
                if np.any(B != self.board) :
                    retval.append((axis,sgn,self.score+score))
        return retval
    
    @classmethod
    def tryMove(cls,board,axis,sgn) :
        B = board.copy()
        score = 0
        #
        # Move the direction axis to the end
        #
        n = len(B.shape)
        axes = [ (xx-(n-1)+axis)%n for xx in range(n) ]
        B = B.transpose(axes)
        #
        # reshape the board into a list of
        # vectors
        #
        Bshape=B.shape
        # python 3000 did away with reduce
        # nn = reduce(lambda x,y : x*y,Bshape[:-1],1)
        nn = np.prod(Bshape[:-1])
        B = B.reshape((nn,Bshape[-1]))
        for ii, row in enumerate(B) :
            if sgn == -1 :
                row = list(reversed(row))
            row,row_score = Game2048.compress(list(row))
            score += row_score
            if sgn == -1 :
                row = list(reversed(row))
            B[ii,:] = row
        B = B.reshape(Bshape)
        raxes = np.argsort(axes)
        B = B.transpose(raxes)
        return B, score
    
    def getPossibilities(self,board) :
        """
        Return a tuple indicating a uniformly
        random, unoccupied cell in the board
        """
        blankCells = self.idxs[board.reshape((np.product(self.board.shape),))==0]
        nn = len(blankCells)
        possibilities = []
        probabilities = []
        for blankCell in blankCells :
            boardCopy = board.copy()
            boardCopy[tuple(blankCell)] = 2
            possibilities.append( boardCopy )
            probabilities.append( 1.0/(nn*3.0) )
            boardCopy = board.copy()
            boardCopy[tuple(blankCell)] = 4
            possibilities.append( boardCopy )
            probabilities.append( 2.0/(nn*3.0) )
        return possibilities, probabilities
    
    def randomBlank(self) :
        poss, prob = self.getPossibilities(self.board)
        rnd = np.random.random()
        cprob = 0
        for b,p in zip(poss,prob) :
            cprob += p
            if cprob > rnd :
                break
        self.board = b
