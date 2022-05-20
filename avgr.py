#Author: Cedric Salame
#Script Name: average g(r)
#Date Created: Jun 6th 2021
#Last Mod Date:
#Last Modification:

#Program: Python 3
import os
import numpy as np
import withdrude_correlate as de
import argparse

hours          = "6"
repname        = "temperature"
temperatures   = [300.0, 323.365, 348.55, 375.697, 404.958, 436.497]
name_middle    = "_snapshot" # 750 snapshots from each trajectory
ogpath         ='/projectnb/nonadmd/cedric17/proj2b_lammps/4-pair_P111-DCA/replica/SingleTraj_P111-DCA/'
grname         ='averagegr'
pair           = []
ani            =[]
cat            =[]
catatom        = 5 #change for cation reference atom
anatom         = 8 #change for anion reference atom
bins           = 200
snapshots_beg  = 1
snapshots_end  = 6001
timesteps      = 501
dist=[]

for temp in temperatures:
    out=open(ogpath+grname+str(int(round(temp)))+'.dat','w')
    out.write('Distance (A)    Cat-Ani    Ani-Ani    Cat-Cat\n')
    count=1
    file=open(ogpath+repname+str(int(round(temp)))+"/gr1.dat",'r').readlines()
    for m in range(1,len(file)):
        pair.append(float(file[m].strip().split()[1]))
        ani.append(float(file[m].strip().split()[2]))
        cat.append(float(file[m].strip().split()[3]))
        dist.append(float(file[m].strip().split()[0]))
    sumpair=pair.copy()
    sumani=ani.copy()
    sumcat=cat.copy()
    pair=[]
    cat=[]
    ani=[]
    for i in range(2,snapshots_end):
        file=open(ogpath+repname+str(int(round(temp)))+"/gr"+str(i)+".dat",'r').readlines()
        for f in range(1,len(file)):
            pair.append(float(file[f].strip().split()[1]))
            ani.append(float(file[f].strip().split()[2]))
            cat.append(float(file[f].strip().split()[3]))
        sumpair=np.sum([sumpair,pair],axis=0)
        sumani=np.sum([sumani,ani],axis=0)
        sumcat=np.sum([sumcat,cat],axis=0)
        cat=[]
        ani=[]
        pair=[]
        count+=1

        print(count)
    for i in range(len(sumpair)):
        out.write(str(dist[i])+'    '+str(sumpair[i]/float(count))+'    '+str(sumani[i]/float(count))+'    '+str(sumcat[i]/float(count))+'\n')
    out.close()
    print('Done with '+str(temp))
    dist=[]
