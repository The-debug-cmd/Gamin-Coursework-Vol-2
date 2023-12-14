import numpy as np

import matplotlib.pyplot as plt

def PayoffMat(n):
    a= -(np.tri(n,n,-2))
    return (a+np.transpose(a))

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
        if list(prevmat[j]) in Mat.tolist():
            j = Mat.tolist().index(list(prevmat[j]))
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

def EquilibriumFinder(n):
    Mat = PayoffMat(n)
    prevMat = PayoffMat(n+1)
    rowlist = list(range(1,n+1))
    collist = list(range(1,n+1))
    
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

    print(UniqueMat)
    display([rowlist[i] for i in indexrow],[collist[i] for i in indexcol],n)
    print(f"The optimal strategy for A should be to go to {[rowlist[i] for i in indexrow]} with probability 1/{len(UniqueMat)}. (Note the following pairs of states are interchangable {indlistrow}).")
    print(f"The optimal strategy for B should be to go to {[collist[i] for i in indexcol]} with probability 1/{len(UniqueMat)}. (Note the following pairs of states are interchangable {indlistcol}).")

def display(rowlist,collist,n):
    equibcount = []
    List = [rowlist,collist]
    for i in List:
        #count
        count = [i.count(j) for j in list(range(1,n+1))]
        count = [0]+ count
        equibcount.append(count)
    plt.imshow(equibcount, interpolation = "nearest", cmap = "BuGn")
    plt.xlim(0.5, 0.5+n)
    plt.xticks(list(range(1,n+1)))
    plt.yticks([0,1,2])
    plt.xlabel("Mixed Equilibrium Position")
    plt.ylabel("Player")
    plt.title(f"N = {n}", fontdict={"fontsize":20})
    plt.savefig(f"Mixed N = {n}.png")


for i in [4,5,6,7,8,9]:
    EquilibriumFinder(i)