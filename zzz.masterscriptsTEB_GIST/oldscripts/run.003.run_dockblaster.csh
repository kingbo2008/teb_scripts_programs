#!/bin/csh 


set mountdir = `pwd`
#set mountdir = "/mnt/nfs/work//tbalius/Water_Project/run_DOCK3.7"
#set filedir  = "/mnt/nfs/work//tbalius/Water_Project"

#foreach conf (  "C"  )
foreach conf ( "A" "B" "C" "D" )

set workdir = $mountdir/workingdir/align_CcP_$conf/

  rm -rf  ${workdir}
  mkdir ${workdir}
  cd ${workdir}
  

cat $mountdir/workingdir/align/aligned.$conf.rec.pdb | awk '{if ($1 == "ATOM" || $1 == "HETATM"){print $0}}' | awk '{if($12 != "H"){print $0}}' | sed -e "s/HETATM/ATOM  /g"  >!  rec.pdb
cat $mountdir/workingdir/align_4NVE/aligned.lig.pdb | awk '{if ($1 == "ATOM" || $1 == "HETATM"){print $0}}' | sed -e "s/HETATM/ATOM  /g"  >!  xtal-lig.pdb

# to use the new charge model
  sed -i 's/HEM/HM2/g'   rec.pdb
  #sed -i 's/ FE /  FE/g' rec.pdb



#cp /usr/local2/lib/dms/radii .

## startdockblaster6 calls a modified Makefile
## that uses Ryan G Coleman's reduce procegers:
## blasterAddHydrogens_standalone.py
#startdockblaster6 >& log.txt

#$DOCK_BASE/src/blastermaster_1.0/blastermaster.py --addhOptions=" -HIS -FLIPs " --addhDict="${mountdir}/zzz.for_reduce/reduce_wwPDB_het_dict_mod.txt" --chargeFile="/nfs/home/tbalius/zzz.github/DOCK/proteins/defaults/amb_mod.crg.oxt" --vdwprottable="/nfs/home/tbalius/zzz.github/DOCK/proteins/defaults/prot_mod.table.ambcrg.ambH" -v
cat <<EOF >! qsub.csh
#!/bin/csh 
#\$ -cwd
#\$ -j yes
#\$ -o stderr
#\$ -q all.q
cd $workdir
$DOCKBASE/proteins/blastermaster/blastermaster.py --addhOptions=" -HIS -FLIPs " --addhDict="${mountdir}/zzz.for_reduce/reduce_wwPDB_het_dict_mod.txt" --chargeFile="/nfs/home/tbalius/zzz.github/DOCK/proteins/defaults/amb_mod.crg.oxt" --vdwprottable="/nfs/home/tbalius/zzz.github/DOCK/proteins/defaults/prot_mod.table.ambcrg.ambH" -v
EOF

qsub qsub.csh 

end # conf


