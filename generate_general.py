
#Author: Cedric Salame
#Script Name: generate_singleTraj.py
#Date Created: May 25th 2021
#Last Mod Date:
#Last Modification:

#Program: Python 3
import os
import numpy as np


#Description: This script will generate the input files and submission scripts for LAMMPS single trajectory post REMD runs to run on SCC.

hours          = "6"
repname        = "temperature"
#temperatures   = [300.0, 307.595, 315.381, 323.365, 331.551, 339.945, 348.55, 357.374, 366.421, 375.697, 385.208, 394.959, 404.958, 415.209,425.72,436.497]
temperatures   = [300.0, 323.365, 348.55, 375.697, 404.958, 436.497]
name_middle    = "_snapshot" 
ogpath         =""
bundle_count   =0
input_array    =[]
batch_count    =16 #or 28 or 32
chunkSize      =10
condaEnv       = "electro"
pair           ="AC4DCAsaltTFSI" #other options: AC4DCAneat,P111DCAneat,P101TFSIneat,AC4DCAsaltDCA,P111DCAsaltDCA,P101TFSIsaltDCA,AC4DCAsaltTFSI,AC4DCAsaltPF6,AC4DCAsaltDCAhalf,AC4DCAsaltTFSIhalf,AC4DCAsaltPF6half
runs           =6000

os.chdir("SingleTraj_"+pair)
os.system('mkdir bundles_'+pair)
os.chdir('bundles_'+pair)

for temp in temperatures:
    for j in range(1,runs+1,50):  
        input_array.append([str(temp),str(round(temp)),str(j)]) 

length    =len(input_array)
end_count =length - batch_count

for i in range(0,length, batch_count):
    outfile_sh=open("bundle"+str(bundle_count)+".sh", "w")
    outfile_sh.write("#!/bin/sh -l\n")
    outfile_sh.write("#$ -S /bin/bash\n")
    outfile_sh.write("#$ -V\n")
    outfile_sh.write("#$ -P nonadmd \n")
    outfile_sh.write("#$ -l h_rt="+hours+":00:00\n")
    outfile_sh.write("#$ -N B"+str(bundle_count)+"\n")
    outfile_sh.write("#$ -M cedric17@bu.edu\n")
    outfile_sh.write("#$ -j y\n")
    outfile_sh.write("#$ -cwd\n") # fix this to be working in ~PyLat
    outfile_sh.write("#$ -pe mpi_"+str(batch_count)+"_tasks_per_node "+str(batch_count)+"\n") # choose 28, 32, 16 only 12 hours for 32.
    outfile_sh.write("\n")
    outfile_sh.write("module purge\n")
    outfile_sh.write("module load miniconda/4.9.2\n")
    outfile_sh.write("\n")
    outfile_sh.write("conda activate "+condaEnv+"\n")
    outfile_sh.write('\n')
    if bundle_count%chunkSize==0:  
        for j in range(chunkSize):
            outfile_sh.write("qsub bundle"+str(bundle_count+j+1)+".sh\n")
    if i >= end_count:
        for z in range(i,length):
            outfile_sh.write("python ../../get_gr.py -p " +pair+" -b "+input_array[z][2]+" -e "+str(int(input_array[z][2])+50)+" -T "+input_array[z][0]+' &\n')
    else:     
        for k in range(batch_count):
            outfile_sh.write("python ../../get_gr.py -p " +pair+" -b "+input_array[k+i][2]+" -e "+str(int(input_array[k+i][2])+50)+" -T "+input_array[k+i][0]+' &\n')
    outfile_sh.write("\n")
    outfile_sh.write("wait\n")
    if i >= end_count:
        for z in range(i,length):
            outfile_sh.write("python ../../get_flux.py -p " +pair+" -b "+input_array[z][2]+" -e "+str(int(input_array[z][2])+50)+" -T "+input_array[z][0]+' &\n')
    else:
        for k in range(batch_count):
            outfile_sh.write("python ../../get_flux.py -p " +pair+" -b "+input_array[k+i][2]+" -e "+str(int(input_array[k+i][2])+50)+" -T "+input_array[k+i][0]+' &\n')
    outfile_sh.write("\n")
    outfile_sh.write("wait\n")
    outfile_sh.write("exit 0\n")
    bundle_count+=1



