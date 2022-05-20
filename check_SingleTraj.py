#Author: Cedric Salame                                                                                                                                                                                                                                                                           \
                                                                                                                                                                                                                                                                                                  
#Script Name: Check_SingleTraj.py                                                                                                                                                                                                                                                                \
                                                                                                                                                                                                                                                                                                  
#Date Created:  May 20th 2022                                                                                                                                                                                                                                                                    \
                                                                                                                                                                                                                                                                                                  
#Last Mod Date:                                                                                                                                                                                                                                                                                  \
                                                                                                                                                                                                                                                                                                  
#Last Modification:                                                                                                                                                                                                                                                                              \
                                                                                                                                                                                                                                                                                                  

#Program: Python 3                                                                                                                                                                                                                                                                               \
                                                                                                                                                                                                                                                                                                  
import os
import numpy as np
#Description: This script will check if the Single Trajectory runs submitted with the array jobs ran and were correctly terminated.                                                                                                                                                              \
                                                                                                                                                                                                                                                                                                  
hours          = "6"
repname        = "temperature"
temperatures   = [300.0, 323.365, 348.55, 375.697, 404.958, 436.497]
name_middle    = "_snapshot" # 3000 snapshots from each trajectory                                                                                                                                                                                                                               \
                                                                                                                                                                                                                                                                                                  
ogpath         ="/projectnb/nonadmd/cedric17/proj2b_lammps/4-pair_P111-DCA/replica/SingleTraj_P111-DCA/"
checkMark      ='Total wall time:'
cores          = 8 # choose 4 8 16 28                                                                                                                                                                                                                                                            \
                                                                                                                                                                                                                                                                                                  
snaps          = 3000
pair = "AC4DCAsaltTFSI"
array  = []

for temp in temperatures:
    count=0
    os.chdir(pair+'_'+repname+str(round(temp)))
    outfile_sh=open("reSub_temperature"+str(round(temp))+".sh",'w')
    outfile_sh.write("#!/bin/sh -l\n")
    outfile_sh.write("#$ -S /bin/bash\n")
    outfile_sh.write("#$ -V\n")
    outfile_sh.write("#$ -P nonadmd \n")
    outfile_sh.write("#$ -l h_rt="+hours+":00:00\n")
    outfile_sh.write("#$ -l avx\n")
    outfile_sh.write("#$ -N reT"+str(round(temp))+"\n")
    outfile_sh.write("#$ -M cedric17@bu.edu\n")
    outfile_sh.write("#$ -j y\n")
    outfile_sh.write("#$ -pe mpi_"+str(cores)+"_tasks_per_node "+str(cores)+"\n")
    outfile_sh.write("\n")
    outfile_sh.write("inputs=(")
    for i in range(1, snaps+1):
        filename   =repname+str(round(temp))+name_middle+str(i)+"-doubleTraj.inp "
        lastline=open("log"+str(i)+".lammps","r").readlines()[-1]
        if checkMark not in lastline:
            outfile_sh.write(filename)
            count+=1       
    outfile_sh.write(")\n")
    outfile_sh.write("#$ -t 1-"+str(count)+"\n")
    outfile_sh.write("\n")
    outfile_sh.write("module purge\n")
    outfile_sh.write("module load openmpi/3.1.4_gnu-10.2.0\n")
    outfile_sh.write("module load lammps/29Sep2021\n")
    outfile_sh.write("\n")
    outfile_sh.write("export MPI_COMPILER='pgi'\n")
    outfile_sh.write("\n")
    outfile_sh.write("export OMP_NUM_THREADS=1\n")
    outfile_sh.write("\n")
    outfile_sh.write("index=$(($SGE_TASK_ID-1))\n")
    outfile_sh.write("taskinput=${inputs[$index]}\n\n")
    outfile_sh.write("mpirun -np "+str(cores)+" lmp_mpi -in $taskinput\n")
    outfile_sh.write("\n")
    outfile_sh.close()
    os.chdir("../")
