#Author: Cedric Salame
#Script Name: generate_singleTraj.py
#Date Created: May 25th 2021
#Last Mod Date: May 20th 2022
#Last Modification: Generalized it to generate all input files for every pair possible.

#Program: Python 3
import os
import numpy as np
#Description: This script will generate the input files and submission scripts for LAMMPS single trajectory post REMD runs to run on SCC.
hours          = "6"
repname        = "temperature" 
temperatures   = [300.0, 307.595, 315.381, 323.365, 331.551, 339.945, 348.55, 357.374, 366.421, 375.697, 385.208, 394.959, 404.958, 415.209,425.72,436.497] 
name_middle    = "_snapshot" 
RunLength      = 37294000 # Get Total Run Length from log.lammps of REMD Run
PostProcLength = 30000000 # change depending on run length
EffRunLength   = np.floor((RunLength-50000)/100000)*100000
timestep_start = int(EffRunLength - PostProcLength + 2500)
timestep_end   = int(EffRunLength + 2500) 
timestep_space = 10000
timesteps      = np.arange(timestep_start,timestep_end+timestep_space,timestep_space)
cores          = 8 # choose 4 8 16 28 
snaps          = 3000 # change depending on run length 
pair= "AC4DCAsaltTFSI" #Different options are defined in the dictionary below.

Pair_Dic= { 'AC4DCAneat':{'Atoms':'1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18','Cores':'1 3 4 6 7 9 11 12 14 15 16 17 18', 'Drudes':'19 20 21 22 23 24 25 26 27 28 29 30 31','Cation':'1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 ','Anion': '16 17 18','Dump': 'C H C C H N C H C H C C H C C N C N D D D D D D D D D D D D D', 'FixDrude': 'C N C C N C C N C N C C N C C C C C D D D D D D D D D D D D D', 'Pair_style':'', 'Include':'','pairPath':'/projectnb/nonadmd/cedric17/proj2b_lammps/7-pair_AC4-DCA/'},
            'P111DCAneat':{'Atoms':'1 2 3 4 5 6 7 8 9 10','Cores':'1 3 5 6 7 8 9 10', 'Drudes': '11 12 13 14 15 16 17 18','Cation': '1 2 3 4 5 6 7 ','Anion':'8 9 10','Dump':'C H C H P C C N C N D D D D D D D D', 'FixDrude':'C N C N C C C C C C D D D D D D D D', 'Pair_style':'', 'Include':'','pairPath':'/projectnb/nonadmd/cedric17/proj2b_lammps/4-pair_P111-DCA/'},
            'P101TFSIneat':{'Atoms':'1 2 3 4 5 6 7 8 9 10 11 12 13','Cores':'1 3 5 6 7 9 10 11 12 13 ', 'Drudes':'14 15 16 17 18 19 20 21 22 23','Cation':'1 2 3 4 5 6 7 8 ','Anion':'9 10 11 12 13','Dump':'C H C H P O H C N S O C F D D D D D D D D D D', 'FixDrude':'C N C N C C C N C C C C C D D D D D D D D D D', 'Pair_style':'', 'Include':'','pairPath':'/projectnb/nonadmd/cedric17/proj2b_lammps/3-pair_P101-TFSI/'},
            'AC4DCAsaltDCA':{'Atoms':'1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19','Cores':'1 3 4 6 7 9 11 12 14 15 16 17 18', 'Drudes':'20 21 22 23 24 25 26 27 28 29 30 31 32','Cation':'1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 ','Anion':'16 17 18','Dump':'C H C C H N C H C H C C H C C N C N Li D D D D D D D D D D D D D', 'FixDrude':'C N C C N C C N C N C C N C C C C C N D D D D D D D D D D D D D', 'Pair_style':' coul/tt 4 12', 'Include':'include /projectnb/nonadmd/cedric17/proj2b_lammps/7-pair_AC4-DCA/1-LiDCA/pair-tt.lmp','pairPath':'/projectnb/nonadmd/cedric17/proj2b_lammps/7-pair_AC4-DCA/1-LiDCA/'},
            'P111DCAsaltDCA':{'Atoms':'1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17','Cores':'1 3 5 6 7 9 10 11 12 13 15 16 17', 'Drudes':'18 19 20 21 22 23 24 25 26 27 28 29 30','Cation':'1 2 3 4 5 6 7 ','Anion':'8 9 10','Dump':'C H C H P C C N C N Li D D D D D D D D', 'FixDrude':'C N C N C C C C C C N D D D D D D D D', 'Pair_style':' coul/tt 4 12', 'Include': 'include /projectnb/nonadmd/cedric17/proj2b_lammps/4-pair_P111-DCA/1-LiDCA/a-drude/pair-tt.lmp','pairPath':'/projectnb/nonadmd/cedric17/proj2b_lammps/4-pair_P111-DCA/1-LiDCA/a-drude/'},
            'P101TFSIsaltDCA':{'Atoms':'1 2 3 4 5 6 7 8 9 10 11','Cores':'1 3 5 6 7 8 9 10', 'Drudes':'12 13 14 15 16 17 18 19','Cation':'1 2 3 4 5 6 7 8','Anion':'9 10 11 12 13','Dump':'C H C H P O C H N S O C F Li N C N D D D D D D D D D D D D D', 'FixDrude':'C N C N C C C N C C C C C N C C C D D D D D D D D D D D D D', 'Pair_style':' coul/tt 4 12', 'Include': 'include /projectnb/nonadmd/cedric17/proj2b_lammps/3-pair_P101-TFSI/2-LiDCA/pair-tt.lmp','pairPath':'/projectnb/nonadmd/cedric17/proj2b_lammps/3-pair_P101-TFSI/2-LiDCA/'},
            'AC4DCAsaltTFSI':{'Atoms':'1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24','Cores':'1 3 4 6 7 9 11 12 14 15 16 17 18 20 21 22 23 24', 'Drudes':'25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42','Cation':'1 2 3 4 5 6 7 8 9 10 11 12 13 14 15','Anion':'16 17 18','Dump':'C H C C H N C H C H C C H C C N C N Li N S O C F D D D D D D D D D D D D D D D D D D', 'FixDrude':'C N C C N C C N C N C C N C C C C C N C C C C C D D D D D D D D D D D D D D D D D D', 'Pair_style':' coul/tt 4 12', 'Include':'include /projectnb/nonadmd/cedric17/proj2b_lammps/7-pair_AC4-DCA/2-LiTFSI/pair-tt.lmp','pairPath':'/projectnb/nonadmd/cedric17/proj2b_lammps/7-pair_AC4-DCA/2-LiTFSI/'},  
            'AC4DCAsaltPF6':{'Atoms': '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21','Cores': '1 3 4 6 7 9 11 12 14 15 16 17 18 20 21', 'Drudes':'22 23 24 25 26 27 28 29 30 31 32 33 34 35 36','Cation':'1 2 3 4 5 6 7 8 9 10 11 12 13 14 15','Anion':'16 17 18','Dump': 'C H C C H N C H C H C C H C C N C N Li F P D D D D D D D D D D D D D D D', 'FixDrude':'C N C C N C C N C N C C N C C C C C N C C D D D D D D D D D D D D D D D', 'Pair_style':' coul/tt 4 12', 'Include': 'include /projectnb/nonadmd/cedric17/proj2b_lammps/7-pair_AC4-DCA/3-LiPF6/pair-tt.lmp','pairPath':'/projectnb/nonadmd/cedric17/proj2b_lammps/7-pair_AC4-DCA/3-LiPF6/'},
            'AC4DCAsaltDCAhalf':{'Atoms':'1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19','Cores':'1 3 4 6 7 9 11 12 14 15 16 17 18', 'Drudes':'20 21 22 23 24 25 26 27 28 29 30 31 32','Cation':'1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 ','Anion':'16 17 18','Dump':'C H C C H N C H C H C C H C C N C N Li D D D D D D D D D D D D D', 'FixDrude':'C N C C N C C N C N C C N C C C C C N D D D D D D D D D D D D D', 'Pair_style':' coul/tt 4 12', 'Include':'include /projectnb/nonadmd/cedric17/proj2b_lammps/7-pair_AC4-DCA/1-LiDCA/pair-tt.lmp','pairPath':'/projectnb/nonadmd/cedric17/proj2b_lammps/7-pair_AC4-DCA/1-LiDCA/halfmolar/'},
            'AC4DCAsaltTFSIhalf':{'Atoms':'1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24','Cores':'1 3 4 6 7 9 11 12 14 15 16 17 18 20 21 22 23 24', 'Drudes':'25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42','Cation':'1 2 3 4 5 6 7 8 9 10 11 12 13 14 15','Anion':'16 17 18','Dump':'C H C C H N C H C H C C H C C N C N Li N S O C F D D D D D D D D D D D D D D D D D D', 'FixDrude':'C N C C N C C N C N C C N C C C C C N C C C C C D D D D D D D D D D D D D D D D D D', 'Pair_style':' coul/tt 4 12', 'Include':'include /projectnb/nonadmd/cedric17/proj2b_lammps/7-pair_AC4-DCA/2-LiTFSI/pair-tt.lmp','pairPath':'/projectnb/nonadmd/cedric17/proj2b_lammps/7-pair_AC4-DCA/2-LiTFSI/halfmolar/'},  
            'AC4DCAsaltPF6half':{'Atoms': '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21','Cores': '1 3 4 6 7 9 11 12 14 15 16 17 18 20 21', 'Drudes':'22 23 24 25 26 27 28 29 30 31 32 33 34 35 36','Cation':'1 2 3 4 5 6 7 8 9 10 11 12 13 14 15','Anion':'16 17 18','Dump': 'C H C C H N C H C H C C H C C N C N Li F P D D D D D D D D D D D D D D D', 'FixDrude':'C N C C N C C N C N C C N C C C C C N C C D D D D D D D D D D D D D D D', 'Pair_style':' coul/tt 4 12', 'Include': 'include /projectnb/nonadmd/cedric17/proj2b_lammps/7-pair_AC4-DCA/3-LiPF6/pair-tt.lmp','pairPath':'/projectnb/nonadmd/cedric17/proj2b_lammps/7-pair_AC4-DCA/3-LiPF6/halfmolar/'}}
 

replicaPath    = Pair_Dic[pair]['pairPath']+'replica/'
pairPath       = Pair_Dic[pair]['pairPath']

os.system("mkdir SingleTraj_"+pair)
os.chdir("SingleTraj_"+pair)

for i in range(0,len(temperatures),3):
    os.system("mkdir "+pair+"_"+repname+str(round(temperatures[i])))
    os.chdir(pair+'_'+repname+str(round(temperatures[i])))
    outfile_sh=open("lammpsArraySub_temperature"+str(round(temperatures[i]))+".sh",'w')
    outfile_sh.write("#!/bin/sh -l\n")
    outfile_sh.write("#$ -S /bin/bash\n")
    outfile_sh.write("#$ -V\n")
    outfile_sh.write("#$ -P nonadmd \n")
    outfile_sh.write("#$ -l h_rt="+hours+":00:00\n")
    outfile_sh.write("#$ -l avx\n")
    outfile_sh.write("#$ -N T"+str(round(temperatures[i]))+"\n")
    outfile_sh.write("#$ -M cedric17@bu.edu\n")
    outfile_sh.write("#$ -j y\n")
    outfile_sh.write("#$ -pe mpi_"+str(cores)+"_tasks_per_node "+str(cores)+"\n")
    outfile_sh.write("#$ -t 1-"+str(snaps)+"\n")
    outfile_sh.write("\n")
    outfile_sh.write("module purge\n")
    outfile_sh.write("module load openmpi/3.1.4_gnu-10.2.0\n")
    outfile_sh.write("module load lammps/29Sep2021\n")
    outfile_sh.write("\n")
    outfile_sh.write("export MPI_COMPILER='pgi'\n")
    outfile_sh.write("\n")
    outfile_sh.write("export OMP_NUM_THREADS=1\n")
    outfile_sh.write("\n")
    outfile_sh.write("inputs=(")
    for j in range(1,snaps+1):   #bring back to 3001
        filename   =repname+str(round(temperatures[i]))+name_middle+str(j)+"-doubleTraj"
        outfile_inp=open(filename+".inp","w")
        outfile_inp.write(" # created by Cedric Salame\n")
        outfile_inp.write("\n")
        outfile_inp.write("log log"+str(j)+".lammps\n")
        outfile_inp.write("units real\n")
        outfile_inp.write("boundary p p p\n")
        outfile_inp.write("\n")
        outfile_inp.write("atom_style full\n")
        outfile_inp.write("bond_style harmonic\n")
        outfile_inp.write("angle_style harmonic\n")
        outfile_inp.write("dihedral_style opls\n")
        outfile_inp.write("\n")
        outfile_inp.write("special_bonds lj/coul 0.0 0.0 0.5\n")
        outfile_inp.write("\n")
        outfile_inp.write("pair_style hybrid/overlay lj/cut/coul/long 12.0 12.0 coul/long/cs 12.0 thole 2.600 12.0"+Pair_Dic[pair]['Pair_style']+"\n")
        outfile_inp.write("pair_modify tail yes\n")
        outfile_inp.write("kspace_style pppm 1.0e-5\n")
        outfile_inp.write("\n")
        outfile_inp.write("read_data "+pairPath+"data.eq.lmp extra/special/per/atom 3\n")
        outfile_inp.write("\n")
        outfile_inp.write("read_dump "+replicaPath+"traj_reordered/dump.temper."+str(format(temperatures[i],'.2f'))+".lammpstrj.gz "+str(timesteps[j-1])+" x y z ix iy iz vx vy vz box yes replace yes wrapped yes\n")
        outfile_inp.write("include "+pairPath+"pair-sc.lmp\n")
        outfile_inp.write(Pair_Dic[pair]['Include']+"\n")
        outfile_inp.write("\n")
        outfile_inp.write("group ATOMS type "+Pair_Dic[pair]['Atoms']+"\n") #done for P111-DCA change depending on system
        outfile_inp.write("group CAT type "+Pair_Dic[pair]['Cation']+"\n")
        outfile_inp.write("group ANI type "+Pair_Dic[pair]['Anion']+"\n")
        outfile_inp.write("group CORES type "+Pair_Dic[pair]['Cores']+"\n")
        outfile_inp.write("group DRUDES type "+Pair_Dic[pair]['Drudes']+"\n")
        outfile_inp.write("\n")
        outfile_inp.write("fix DRUDE all drude "+Pair_Dic[pair]['FixDrude']+"\n")
        outfile_inp.write("\n")
        outfile_inp.write("comm_modify vel yes\n")
        outfile_inp.write("fix SHAKE ATOMS shake 0.0001 20 0 b 1\n")
        outfile_inp.write("\n")
        outfile_inp.write("neighbor 2.0 bin \n")
        outfile_inp.write("\n")
        outfile_inp.write("timestep 1.0\n")
        outfile_inp.write("\n")
        outfile_inp.write("variable TK equal "+ str(temperatures[i])+"\n")
        outfile_inp.write("variable TDK equal 1.0\n")
        outfile_inp.write("variable PBAR equal 1.0\n")
        outfile_inp.write("#velocity all create ${TK} 12345\n") # no need considering that we have the initial velos in the dump file 
        outfile_inp.write("\n")
        outfile_inp.write("fix DTDIR all drude/transform/direct\n")
        outfile_inp.write("fix TSTAT ATOMS nvt temp ${TK} ${TK} 200\n")
        outfile_inp.write("fix TSTDR DRUDES nvt temp ${TDK} ${TDK} 50\n")
        outfile_inp.write("fix DTINV all drude/transform/inverse\n")
        outfile_inp.write("\n")
        outfile_inp.write("fix ICECUBE all momentum 1000 linear 1 1 1\n")
        outfile_inp.write("\n")
        outfile_inp.write("run 5000")
        outfile_inp.write("\n")
        outfile_inp.write("reset_timestep 0\n")
        outfile_inp.write("\n")
        outfile_inp.write("compute TATOM ATOMS temp\n")
        outfile_inp.write("compute TDRUDE all temp/drude\n")
        outfile_inp.write("\n")
        outfile_inp.write("dump TRAJ all custom 10 dump"+str(j)+".lammpstrj id mol type element q x y z ix iy iz vx vy vz\n") # dumping freq
        outfile_inp.write("dump_modify TRAJ sort id &\n")
        outfile_inp.write("            element "+Pair_Dic[pair]['Dump']+"\n")
        outfile_inp.write("\n")
        outfile_inp.write("thermo_style custom step cpu time etotal pxy pxx pxz pyz pyy pzz press vol density c_TDRUDE[1] c_TDRUDE[2]\n")
        outfile_inp.write("thermo 10\n") #thermo freq
        outfile_inp.write("variable t equal time\n")
        outfile_inp.write("\n")
        outfile_inp.write("compute MSD1 CAT msd com yes\n")
        outfile_inp.write("variable msd1 equal c_MSD1[4]\n")
        outfile_inp.write("fix PRMSD1 CAT print 10 \"${t} ${msd1}\" file msd_cat"+str(j)+".lammps screen no\n")
        outfile_inp.write("\n")
        outfile_inp.write("compute MSD2 ANI msd com yes\n")
        outfile_inp.write("variable msd2 equal c_MSD2[4]\n")
        outfile_inp.write("fix PRMSD2 ANI print 10 \"${t} ${msd2}\" file msd_ani"+str(j)+".lammps screen no\n")
        outfile_inp.write("\n")
        outfile_inp.write("run 5010") #change run size, dumping freq,thermo printing, and MSD printing accordingly.
        outfile_inp.write("\n")
        outfile_inp.write("uncompute MSD1\n")
        outfile_inp.write("uncompute MSD2\n")
        outfile_inp.write("unfix PRMSD1\n")
        outfile_inp.write("unfix PRMSD2\n")
        outfile_inp.write("undump TRAJ\n")
        outfile_inp.write("reset_timestep 0\n")
        outfile_inp.write("\n")
        outfile_inp.write("dump TRAJ2 all custom 10 dump"+str(j+snaps)+".lammpstrj id mol type element q x y z ix iy iz vx vy vz\n") # dumping freq
        outfile_inp.write("dump_modify TRAJ2 sort id &\n")
        outfile_inp.write("            element "+Pair_Dic[pair]['Dump']+"\n")
        outfile_inp.write("\n")
        outfile_inp.write("compute MSD3 CAT msd com yes\n")
        outfile_inp.write("variable msd3 equal c_MSD3[4]\n")
        outfile_inp.write("fix PRMSD3 CAT print 10 \"${t} ${msd3}\" file msd_cat"+str(j+snaps)+".lammps screen no\n")
        outfile_inp.write("\n")
        outfile_inp.write("compute MSD4 ANI msd com yes\n")
        outfile_inp.write("variable msd4 equal c_MSD4[4]\n")
        outfile_inp.write("fix PRMSD4 ANI print 10 \"${t} ${msd4}\" file msd_ani"+str(j+snaps)+".lammps screen no\n")
        outfile_inp.write("run 5010\n")
        outfile_inp.write("\n")
        outfile_inp.close()
        outfile_sh.write(filename+".inp ")
    outfile_sh.write(")\n")
    outfile_sh.write("\n")
    outfile_sh.write("index=$(($SGE_TASK_ID-1))\n")
    outfile_sh.write("taskinput=${inputs[$index]}\n\n")
    outfile_sh.write("mpirun -np "+str(cores)+" lmp_mpi -in $taskinput\n")
    outfile_sh.write("\n")
    outfile_sh.close()
    os.chdir("../")
