class SCG(list) :
    pass

def treeSearchSymmetric(game) :
    for g in game :
        if treeSearchSymmetric is None :
            return g
    return None

def scoreTreeSolverLeft(game,scorer,depth) :
    bestScore = float('-inf')
    bestGame = None
    for g in game.Left :
        if depth > 0 :
            gp, score = scoreTreeSolverRight(g,scorer,depth-1)
        else :
            score = scorer(g)
        if score > bestScore :
            bestScore = score
            bestGame = g
    return bestGame, bestScore

def scoreTreeSolverRight(game,scorer,depth) :
    bestScore = float('+inf')
    bestGame = None
    for g in game.Right :
        if depth > 0 :
            gp, score = scoreTreeSolverLeft(g,scorer,depth-1)
        else :
            score = scorer(g)
        if score < bestScore :
            bestScore = score
            bestGame = g
        return bestGame, bestScore
    

        
        
