import math, sys
import os.path

from math import sqrt

# take a syble atom type and returns an element.  
# does this by spliting on the dot (.) in the type 
# and returning the chars before the dot.
def sybel_to_ele(atom_type):
    atom_type=atom_type.replace(" ","")
    ele = atom_type.split('.')[0]
    return ele


# read in a mol2 file and replace atom type with the element name. 
def read_mol2(filename,text1):
    file1 = open(filename,'r')
    lines  =  file1.readlines()

    atom_flag = False;

    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) > 0):
             if (linesplit[0] == "@<TRIPOS>BOND"):
                atom_flag = False
             if (atom_flag):
                atom_type = line[47:51] 
                print atom_type
                ele = sybel_to_ele(atom_type) 
                line_mod = '%s%-5s%s\n'%(line[0:47],ele,line[52:-1])
                #text1 = text1+line
                text1 = text1+line_mod
             elif (not atom_flag):
                text1 = text1+line # add line to text1 for output
             if ( linesplit[0] == "@<TRIPOS>ATOM" ):
                atom_flag =  True
 

    file1.close()
    return text1
#################################################################################################################
#################################################################################################################
def main():
    if (len(sys.argv) != 3): # if no input
        print " (1) mol2 file name," 
        print " (3) output mol2 ";
        return

    filename    = sys.argv[1]
    output      = sys.argv[2]

    text1 = '' # text to be writen to output
    text1 = read_mol2(filename,text1)

    file2 = open(output,'w')
    file2.write(text1)
    file2.close()

    return; 
#################################################################################################################
#################################################################################################################
main()
