
## uses local version of python on sublime



import sys 

#import pybel, openbabel

import base64

import math, matplotlib, scipy, pylab
import scipy.cluster.hierarchy as sch


## Writen by Trent Balius in the Shoichet Group

## this program is not functional right now

## THis program will read in the fingerprints generated by SEA and will generate a Tanimoto matrix. 
## It will perform clustering and alow us to see the chemotyes and the reasons for the relationship.
## perhaps this should be a funtion with in SEA code.

## We should call the c code from sea to perform the conversion from Base64 (daylight maping) output to bitstrings.  
## sea/lib/c/fast_tanimoto/fast_tanimoto.c
## sea/lib/c/fconvert/fconvert2py.c
## 

#decimal to binary 
def decimal2binary(n):
    bStr = ''
    if n < 0: raise ValueError, "must be a positive integer"
    if n == 0: return '0'
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n >> 1    
    return bStr

def makeFingerPrintArray(filehandel):
  lines = filehandel.readlines()
  fplist = []
  for line in lines:
      fp = line.split(';')[0] 
      print fp
      b =  base64.b64decode(fp)
      fplist.append(fp)
  return fplist

def calcTanimoto(A,B):
    ## A, B are bool arrays
    ## Tc = (A and B)/(A or B) = sum (ai and bi) / sum ( ai or bi) 

    AandB = 0
    AorB  = 0
    for i in range(len(fp1)):
        AandB = Aandb + (A[i] and B[i])
        AorB  = Aorb + (A[i] or B[i])
    return AandB/AorB

def makeTanimotoMatrix(fingerprints1,fingerprints2):
    if len(fingerprints1) == 1 or len(fingerprints2) == 1:
        print "fingerprints is size 1"

    ## intialize matrix
    print "makeing a " + str(len(fingerprints1)) + "X" + str(len(fingerprints1)) + "Matrix. "
    matrix = []
    for i in range(len(fingerprints1)):
        row = []
        for j in range(len(fingerprints2)):
            row.append(0)
        matrix.append(row)

    ## fill matrix
    for i in range(len(fingerprints1)):
        for j in range(len(fingerprints2)):
            tc = calcTanimoto(fingerprints1[i], fingerprints2[j])
            matrix[i][j] = tc
    return matrix

def write_matrix(filehandel,Matrix):
    for i in range(len(Matrix)):
        for j in range(len(Matrix[i])):
            if (j == 0):
                filehandel.write('%f' % (Matrix[i][j]))
            filehandel.write(',%f' % (Matrix[i][j]))
        filehandel.write('\n')

def mat_to_mat(Mat):
    #print "I AM HERE in mat_to_mat(Mat)"
    ## 1 - tc is more like a distance than tc.
    m = len(Mat)
    n = len(Mat[0])

    if (m != n):
        print "inconsitancy in numbers of rows and columns in the matrix."

    print m,n

    X = scipy.zeros([m,n])

    ## converts from a 2D array to Scipy Matrix 
    for i in range(0,m):
        for j in range(0,n):
               X[i,j] = -Mat[i][j] + 1.0

    return X


def mat_to_vector(Mat):
    ## 1 - tc is more like a distance than tc.
    m = len(Mat)
    n = len(Mat[0])
   
    if (m != n):
        print "inconsitancy in numbers of rows and columns in the matrix."
        sys.exit()
   
    print m,n
   
    X = scipy.zeros([m,n])
    Xvec = scipy.zeros(n*(n-1)/2)
   
    count2    = 0

    ## converts from a 2D array to Scipy Matrix 
    for i in range(0,n):
        for j in range(0,n):
               X[i,j] = -Mat[i][j] + 1.0

    for i in range(0,n):
        for j in range(i+1,n):
               Xvec[count2] = -Mat[i][j] + 1.0
               count2 = count2+1

    return X,Xvec

def heatmap_not_sym(Mat,filename,idx1,idx2):
     m = len(Mat)
     n = len(Mat[0])
     print m,n

     #print 'test',len(idx1),len(idx2)

     ylabel = []
     xlabel = [] 
     for i in range(0,m):
        ylabel.append('lig_'+str(idx1[i]+1))
     for i in range(0,n):
        xlabel.append('lig_'+str(idx2[i]+1))

     fig = pylab.figure(figsize=(8,8))

     Mat = mat_to_mat(Mat)
     Mat = Mat[idx1,:]
     Mat = Mat[:,idx2]

     axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])

     cdict = {'red': ((0.0, 0.0, 0.0),
                       (0.0, 0.0, 0.0),
                       (1.0, 1.0, 1.0)),
               'green': ((0.0, 0.0, 0.0),
                         (0.0, 0.0, 0.0),
                         (1.0, 1.0, 1.0)),
               'blue': ((0.0, 0.0, 0.0),
                        (0.0, 0.0, 0.0),
                        (1.0, 1.0, 1.0))}
     
    
     my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,100)
    
     im = axmatrix.imshow(Mat, aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)

     im.set_clim(0,1)
     axmatrix.set_xlim(-0.5, n-0.5)
     axmatrix.set_ylim(-0.5, n-0.5)
     axmatrix.set_xticks(range(0,n))
     axmatrix.set_xticklabels(xlabel)

     axmatrix.set_yticks(range(0,m))
     axmatrix.set_yticklabels(ylabel)
     for i in range(0,m):
         label = axmatrix.yaxis.get_major_ticks()[i].label
         label.set_fontsize(4)
     
     for i in range(0,n):
         label = axmatrix.xaxis.get_major_ticks()[i].label
         label.set_fontsize(4)
         label.set_rotation('vertical')
    
     # Plot colorbar.
     axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
     pylab.colorbar(im, cax=axcolor)
     fig.show()
     fig.savefig(filename,dpi=600)


def heatmap(Mat,bool_sort,filename):
     m = len(Mat)
     n = len(Mat[0])
     print m,n

     xlabel = [] 
     for i in range(0,m):
        xlabel.append('lig_'+str(i+1))
     ylabel = []
     for i in range(0,n):
        ylabel.append('lig_'+str(i+1))

     fig = pylab.figure(figsize=(8,8))

     if (bool_sort):
         Mat, Matvec = mat_to_vector(Mat)
         Y = sch.linkage(Matvec, method='single')
         threshold = 0.2
         clusters = sch.fcluster(Y, threshold, 'distance')
         print clusters

         ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
         Z1 = sch.dendrogram(Y, orientation='right')
         #help(sch.dendrogram)
         ax1.set_xticks([])
         ax1.set_yticks([])
        
         # Compute and plot second dendrogram.
         ax2 = fig.add_axes([0.3,0.71,0.6,0.2])
         Z2 = sch.dendrogram(Y)
         ax2.set_xticks([])
         ax2.set_yticks([])
         #ax2.set_xlim(-1, n)
        
         # Plot distance matrix.
         axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
         idx1 = Z1['leaves']
         idx2 = Z2['leaves']
         Mat = Mat[idx1,:]
         Mat = Mat[:,idx2]
         #xlabel[:] = xlabel[idx2]
         xlabel_new = []
         for i in range(len(idx2)):
             xlabel_new.append(xlabel[idx2[i]])
         del xlabel[:]
         xlabel = xlabel_new

     else:
         Mat = mat_to_mat(Mat)
         axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])

     cdict = {'red': ((0.0, 0.0, 0.0),
                       (0.0, 0.0, 0.0),
                       (1.0, 1.0, 1.0)),
               'green': ((0.0, 0.0, 0.0),
                         (0.0, 0.0, 0.0),
                         (1.0, 1.0, 1.0)),
               'blue': ((0.0, 0.0, 0.0),
                        (0.0, 0.0, 0.0),
                        (1.0, 1.0, 1.0))}
     
    
     my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,100)
    
     im = axmatrix.imshow(Mat, aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)

     if (bool_sort):
         v = range(0,n)
         axmatrix.plot(v,v,'yo',markersize=2)
         

     im.set_clim(0,1)
     axmatrix.set_xlim(-0.5, n-0.5)
     axmatrix.set_ylim(-0.5, n-0.5)
     axmatrix.set_xticks(range(0,m))
     axmatrix.set_xticklabels(xlabel)

     if (not bool_sort):
         axmatrix.set_yticks(range(0,n))
         axmatrix.set_yticklabels(ylabel)
         for i in range(0,n):
             label = axmatrix.yaxis.get_major_ticks()[i].label
             label.set_fontsize(4)
     else:
         axmatrix.set_yticks([])
     
     for i in range(0,m):
         label = axmatrix.xaxis.get_major_ticks()[i].label
         label.set_fontsize(4)
         label.set_rotation('vertical')
    
     # Plot colorbar.
     axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
     pylab.colorbar(im, cax=axcolor)
     fig.show()
     fig.savefig(filename,dpi=600)


def main():
  if len(sys.argv) != 4: # if no input
     print "You must entered in 3 inputs:"
     print "fingerprints1, fingerprints2, output prefix"
     exit()     

  file1name  = sys.argv[1] 
  file2name  = sys.argv[2] 
  outname    = sys.argv[3] 
  print "input file = " + file1name
  print "output matrix file = " + file2name
  file1handel = open(file1name,'r')
  file2handel = open(file2name,'r')
  makeFingerPrintArray(file1handel)

  file1handel.close()
  file2handel.close()
  return
  #heatmap(m,True,file2name+'.png')
 
main()

