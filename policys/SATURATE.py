# SATURATE (Krause et al. 2008) 
# Paper: https://papers.nips.cc/paper/2007/file/eae27d77ca20db309e056e3d2dcd7d69-Paper.pdf
# version adapted for best separater selection


def SATURATE(F, uccg, sparse):
    """
    SATURATE (Krause et al. 2008) for approximate best separator set
    """
    V = set(uccg)

    maxc = len(V)
    minc = 0
    TOL = 1
    maxiter = 50
    ssetmax = set()

    iter = 0
    while not (iter>=maxiter or maxc-minc < TOL):
        iter += 1
        c = int((maxc+minc)/2)
        sset = GPC(c, F, uccg, sparse)

        if len(sset) > sparse:
            minc = c
        else:
            maxc = c
            ssetmax = sset
        
    return ssetmax


def GPC(c, F, uccg, sparse):
    """
    greedy submodular partial cover for checking feasibility of c
    """
    V = set(uccg)

    sset = set()
    f = F(c, sset, uccg)
    while len(sset) <= sparse and f > c:
        best_i = None
        best_diff = 0

        for i in V - sset:
            diff = F(c, sset.union({i}), uccg)-f
            if diff <= best_diff:
                best_i = i
                best_diff = diff
        
        sset.add(best_i)
        f += best_diff
    
    return sset