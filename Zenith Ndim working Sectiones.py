import numpy as np
import matplotlib.pyplot as plt


def payoffvalue(a,b,n,k):
    alist = [a//(n**i) + 1 for i in range(k)]
    alist[0] = (a % n) + 1
    alist = alist + [i-1 for i in alist] + [i+1 for i in alist]
    aset = set(alist)
    blist = [b//(n**i) + 1 for i in range(k)]
    blist[0] = (b % n) + 1
    bset = set(blist)
    difdic = {i: max((blist.count(i)-alist.count(i)),0) for i in bset.intersection(aset)}
    freedic = {i: blist.count(i) for i in bset.difference(bset.intersection(aset))}   
    return -(sum(difdic.values())+sum(freedic.values()))

def PayoffMat(n, k):
    mat = []
    for i in range(n**k):
        ro = []
        for j in range(n**k):
            ro.append(payoffvalue(i,j,n,k))
        mat.append(ro)
    return (np.array(mat))

def RowLess(test,compare):
    if (test == compare).all():
        return False
    return (test <= compare).all()

def ColMore(test,compare):
    if (test == compare).all():
        return False
    return (test >= compare).all()

def RowDel1(i, Mat,lis):
    prevmat = Mat
    for j in range(len(Mat)):
        #dodgy stuff
        if list(prevmat[j]) in Mat.tolist() and list(prevmat[i]) in Mat.tolist():
            j = Mat.tolist().index(list(prevmat[j]))
            i = Mat.tolist().index(list(prevmat[i]))
            if not(i == j):
                if RowLess(Mat[i], Mat[j]):
                    Mat = np.delete(Mat, i, 0)
                    lis.pop(i)
    return Mat,lis

def RowDel(Mat, lis):
    prevmat = Mat
    for i in range(len(Mat)):
        if list(prevmat[i]) in Mat.tolist():
            i = Mat.tolist().index(list(prevmat[i]))
            Mat, lis = RowDel1(i, Mat,lis)
    return Mat, lis

def ColDel1(i, Mat,lis):
    prevmat = Mat
    for j in range(len(Mat)):
        if list(prevmat[j]) in Mat.tolist():
            j = Mat.tolist().index(list(prevmat[j]))
            if not(i == j):
                if ColMore(Mat[i], Mat[j]):
                    Mat = np.delete(Mat, i, 0)
                    lis.pop(i)
    return Mat,lis

def ColDel(Mat, lis):
    prevmat = Mat
    for i in range(len(Mat)):
        if list(prevmat[i]) in Mat.tolist():
            i = Mat.tolist().index(list(prevmat[i]))
            Mat, lis = ColDel1(i, Mat,lis)
    return Mat, lis

def decoder(a,n,k):
    alist = [a//(n**i) + 1 for i in range(k)]
    alist[0] = (a % n) + 1
    alist.reverse()   
    return alist

def EquilibriumFinder(n,k):
    Mat = PayoffMat(n,k)
    prevMat = PayoffMat(n+1,k)
    rowlist = list(range(1,n**k+1))
    collist = list(range(1,n**k+1))
    
    while not((Mat.tolist() == prevMat.tolist())):
        prevMat = Mat
        Mat, collist = ColDel(np.transpose(Mat),collist)
        Mat, rowlist = RowDel(np.transpose(Mat),rowlist)


    UniqueMat,indexrow, repeatrow = np.unique(Mat, axis=0, return_index = True, return_counts = True)
    UniqueMat,indexcol, repeatcol  = np.unique(UniqueMat, axis=1, return_index = True, return_counts = True)

    indlistrow= []
    for i in range(len((repeatrow))):
        if repeatrow[i] > 1:
            indices = [j for j, x in enumerate(Mat.tolist()) if x == Mat.tolist()[i]]
            indices= [rowlist[i] for i in indices]
            indlistrow.append(indices)

    indlistcol= []
    Mat1 = np.transpose(Mat)
    for i in range(len((repeatcol))):
        if repeatcol[i] > 1:
            indices = [j for j, x in enumerate(Mat1.tolist()) if x == Mat1.tolist()[i]]
            indices= [collist[i] for i in indices]
            indlistcol.append(indices)

    indexrow.sort()
    indexcol.sort()
    UniqueMat = np.fliplr(UniqueMat)

    rowlist1 =[rowlist[i] -1 for i in indexrow]
    collist1 = [collist[i] -1 for i in indexcol]
    rowlist1 = [decoder(i,n,k) for i in rowlist1]
    collist1 = [decoder(i,n,k) for i in collist1]

    for j in range(0,k):
        print(f"The set of mixed equilibria have locations at {[i for i in collist1 if len(set(i))==k-j]} for attackers and {[i for i in rowlist1 if len(set(i))==k-j]} for defenders when k = {j} repeats are allowed")
EquilibriumFinder(7,2)    