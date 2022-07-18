#Author: Cedric Salame
#Script Name: generate_singleTraj.py
#Date Created: Jun 6th 2021
#Last Mod Date:
#Last Modification:

#Program: Python 3 
import os
import numpy as np
import correlate_gofr as de  

#Description: This script will calculate correlation functions for every temperature and trajectory and average it on a temperature basis. It also returns the conductivity 
hours          = "6"
repname        = "_temperature"
temperatures   = [300.0, 323.365, 348.55, 375.697, 404.958, 436.497]
name_middle    = "_snapshot" # 750 snapshots from each trajectory
array          = []
sum_array      = []
time_array     = []
J              = []
snapshots      = 6000
timesteps      = 500
pair           ="AC4DCAsaltTFSI" #other options: AC4DCAneat,P111DCAneat,P101TFSIneat,AC4DCAsaltDCA,P111DCAsaltDCA,P101TFSIsaltDCA,AC4DCAsaltTFSI,AC4DCAsaltPF6,AC4DCAsaltDCAhalf,AC4DCAsaltTFSIhalf,AC4DCAsaltPF6half

os.chdir("SingleTraj_"+pair)
os.system("mkdir corr_functions")

for temp in temperatures:
        out=open('corr_functions/corr'+str(round(temp))+'.dat','w')
        out.write('Time (fs)   Javg ((e*Ang/fs)**2)\n')
        count=5
        print('currently working on '+str(temp))
        os.chdir(pair+repname+str(round(temp)))
        file=open('corr1_1.dat','r').readlines()
        for j in range(1,len(file)):
                array.append(float(file[j].strip().split()[1]))
                time_array.append(float(file[j].strip().split()[0]))
        sum_array=array.copy()
        array=[]
        for l in range(2,6):
                file=open("corr1_"+str(l)+".dat",'r').readlines()
                for m in range(1,len(file)):
                        array.append(float(file[m].strip().split()[1]))
                sum_array=np.sum([sum_array,array],axis=0)
                array=[]

        for i in range(2,snapshots+1):
#                os.chdir(repname+str(round(temp))+name_middle+str(i))
                for k in range(1,6):
                        file=open("corr"+str(i)+"_"+str(k)+".dat",'r').readlines()
                        for j in range(1,len(file)):
                                array.append(float(file[j].strip().split()[1]))
                        sum_array=np.sum([sum_array,array],axis=0)
                        array=[]
                        count+=1
        os.chdir('../')



        
                
         
         
        print(count)        
        for i in range(len(sum_array)):
                out.write(str(time_array[i])+'   '+str(sum_array[i]/float(count))+'\n')
        out.close()
        print('Done with '+str(temp))
        time_array=[]
