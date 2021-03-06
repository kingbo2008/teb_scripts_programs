
import sys


def convert(arr):
# sed -e 's/ALA/A/g' -e 's/GLY/G/g' -e 's/VAL/V/g' -e 's/ILE/I/g' -e 's/LEU/L/g' -e 's/PHE/F/g' -e 's/PRO/P/g' -e 's/MET/M/g' -e 's/SER/S/g' -e 's/THR/T/g' -e 's/TYR/Y/g' -e 's/CYS/C/g' -e 's/TRP/W/g' -e 's/HIS/H/g' -e 's/ARG/R/g' -e 's/GLU/E/g' -e 's/GLN/Q/g' -e 's/ASP/D/g' -e 's/ASN/N/g' -e 's/LYS/K/g'
    count = 0      
    resabbstr = ''
    for res_str in arr:
        if count == 80: 
           count = 0
           resabbstr = resabbstr + '\n'
        resname = res_str[0:3]
        if (resname == "ALA"):
            resabbstr = resabbstr+"A"
        if (resname == "GLY"):
            resabbstr = resabbstr+"G"
        if (resname == "VAL"):
            resabbstr = resabbstr+"V"
        if (resname == "ILE"):
            resabbstr = resabbstr+"I"
        if (resname == "LEU"):
            resabbstr = resabbstr+"L"
        if (resname == "PHE"):
            resabbstr = resabbstr+"F"
        if (resname == "PRO"):
            resabbstr = resabbstr+"P"
        if (resname == "MET"):
            resabbstr = resabbstr+"M"
        if (resname == "SER"):
            resabbstr = resabbstr+"S"
        if (resname == "THR"):
            resabbstr = resabbstr+"T"
        if (resname == "TYR"):
            resabbstr = resabbstr+"Y"
        if (resname == "TRP"):
            resabbstr = resabbstr+"W"
        if (resname == "HIS"):
            resabbstr = resabbstr+"H"
        if (resname == "CYS"):
            resabbstr = resabbstr+"C"
        if (resname == "ARG"):
            resabbstr = resabbstr+"R"
        if (resname == "GLU"):
            resabbstr = resabbstr+"E"
        if (resname == "GLN"):
            resabbstr = resabbstr+"Q"
        if (resname == "ASP"):
            resabbstr = resabbstr+"D"
        if (resname == "ASN"):
            resabbstr = resabbstr+"N"
        if (resname == "LYS"):
            resabbstr = resabbstr+"K"
        count = count + 1
   
    return resabbstr

def main():
   if len(sys.argv) != 2: 
      print "Error. not the right number of arguments."
      print "one input: pdb file name"
   
   
   #filename = '5CEM.pdb'
   filename = sys.argv[1]
   
   #splitfilename = filename.split('.')
   #fastafilename   = ""
   #for i in range(len(splitfilename)-1):
   #    fastafilename = fastafilename+splitfilename[i]+'.' 
   #fastafilename = fastafilename+"fasta"
   fastafilename = filename+".fasta"
   
   
   fh = open(filename,'r')
   
   dic_chain_arr = {}
   arr       = []
   dic_count = {}
   for line in fh: 
       if 'ATOM' == line[0:4]:
         #print line
         #print line[17:26]
         res_str = line[17:26] # resname chain resid
         chainid = line[21] # resname chain resid
   
         if not (chainid in dic_chain_arr):
            dic_chain_arr[chainid] = []
   
         if not (res_str in dic_count):
            dic_count[res_str] = 1
            arr.append(res_str)
            dic_chain_arr[chainid].append(res_str)
         else:
            dic_count[res_str] = dic_count[res_str] + 1
   fh.close()
   
   resabbstr = convert(arr)
   
   fh2 = open(fastafilename+'full','w')
   
   name = filename+".convert"
   fh2.write(">"+name+":A|PDBID|CHAIN|SEQUENCE\n")
   fh2.write(resabbstr+'\n')
   fh2.close()
   
   fh3 = open(fastafilename,'w')
   
   for key in sorted(dic_chain_arr.keys()):
      # for each chain write to a specific file for that chain and write to a 
      # file that contains all the chains.  
      fastafilename_chain = filename+'.'+str(key)+".fasta"
      fh4 = open(fastafilename_chain,'w')
      resabbstr = convert(dic_chain_arr[key])
      fh4.write(">"+name+":"+key+"|PDBID|CHAIN|SEQUENCE\n")
      fh4.write(resabbstr+'\n')
      fh4.close()
      fh3.write(">"+name+":"+key+"|PDBID|CHAIN|SEQUENCE\n")
      fh3.write(resabbstr+'\n')
   fh3.close()

main()   
