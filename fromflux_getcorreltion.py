#Author: Cedric Salame
#Script Name: generate_singleTraj.py
#Date Created: Jun 6th 2021
#Last Mod Date:
#Last Modification:

#Program: Python 3 
import os
import numpy as np
import withdrude_correlate as de  
import argparse

#Description: This script will calculate correlation functions for a bundle of trajectories determined by the input flags.

parser         = argparse.ArgumentParser()

# -b Begin -e End -t initial timestep -T temperature                                                                                  
parser.add_argument("-b","--begin", dest= "begin", help=" First Snapshot")
parser.add_argument("-e","--end", dest="end", help="last Snapshot")
#parser.add_argument("-T","--temperature",dest="temperature",help="temperature")
args           = parser.parse_args()
hours          = "6"
repname        = "temperature"
#temperatures   = [300.0, 307.595, 315.381, 323.365, 331.551, 339.945, 348.55, 357.374, 366.421, 375.697, 385.208, 394.959, 404.958, 415.209,425.72,436.497]                                                                                                                                      
#temperatures   = [323.365, 348.55, 375.697, 404.958, 436.497]
temperatures   =[300.0]
name_middle    = "_snapshot" # 750 snapshots from each trajectory
array          = []
sum_array      = []
time_array     = []
J              = []
snapshots_beg  = int(args.begin)
snapshots_end  = int(args.end)
timesteps      = 101
ogpath         ='/projectnb/nonadmd/cedric17/proj2b_lammps/4-pair_P111-DCA/replica/SingleTraj_P111-DCA/'

time_array=np.arange(0,1010,10).T
                

for temp in temperatures:
        os.chdir(repname+str(round(temp)))
        for k in range(snapshots_beg,snapshots_end):
                file=open("flux"+str(k)+".dat",'r').readlines()
                count=1
                for j in range(0,500,100):
                        out=open(ogpath+repname+str(round(temp))+'/corr'+str(k)+"_"+str(count)+'.dat','w')
                        
                        out.write('Time (fs)   J0.Jt ((e*Ang/fs)**2)\n')
                        corr=np.zeros((timesteps,1))
                        for i in range(j+1,j+102):
                                J.append([float(file[i].strip().split()[1]),float(file[i].strip().split()[2]),float(file[i].strip().split()[3])])
                        corr[:,0]=de.correlate(J)
                        count+=1
                        J=[]
                        for l in range(len(corr)):
                                out.write(str(time_array[l])+'   '+str(corr[l,0])+'\n')
                        out.close()
                        print(k)
        os.chdir('../')
        
