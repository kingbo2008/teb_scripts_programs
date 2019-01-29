
## This script is writen by
## Trent E Balius
## 2013/12 
################################################################
## This script  
## scrapes the pdb webpage for the smiles string for a given 
## residue name. 
################################################################


import sys,urllib,urllib2

if len(sys.argv) != 2:
    print "Error: two arguments are needed"
    print "ligand resid = "
    sys.exit()

ligresid     = sys.argv[1]

#url = 'http://zinc.docking.org/results/structure?structure.smiles='+smiles+'&structure.similarity=' + similarity
#url = 'http://www.rcsb.org/pdb/ligand/ligandsummary.do?hetId=' + ligresid
url = 'https://www3.rcsb.org/ligand/' + ligresid

#print "url = " + url

#page=requests.get(url)

webfile = urllib.urlopen(url)
page    = webfile.read()
webfile.close()

#print page

splitpage=page.split('\n')

flag = False

count = 0 
for line in splitpage:
    #print line
    if len(line.split())==0:
        continue
    if "Isomeric SMILES" in line:
       #print line
       flag = True
       smilesline = ""
    #elif (flag and 'td' in line):
    if (flag): 
       smilesline = smilesline+line
    if (flag and '</td>' in line):
       #print smilesline
       #smiles=smilesline.replace('<',' ').replace('>',' ').split()[1]
       smiles=smilesline.split()[3]
       flag = False
       ## <li id="sub-72436952" class="zinc summary-item">
       #sliteline = line.replace('<',' ').replace('>',' ').replace('-',' ').replace('=',' ').replace('"','').split()
       #print line
       #print sliteline
       #zincid = sliteline[3]
       #print "Isomeric SMILES = " + smiles
       print smiles + " " + ligresid 
       count = count+1

if (count == 0):
   print "code not found"
elif (count > 1):
   print "something werd is happening. count > 1"


fileoutput = ligresid+".smi"
fileh = open(fileoutput,'w')
fileh.write(smiles+' '+ligresid+'\n')
fileh.close()


