#Author: Cedric Salame
#Script Name: generate_singleTraj.py
#Date Created: Jun 6th 2021
#Last Mod Date:
#Last Modification:

#Program: Python 3 
import os
import numpy as np
import correlate_gofr as de  
import argparse

#Description: This script will calculate correlation functions for a bundle of trajectories determined by the input flags.

parser         = argparse.ArgumentParser()

# -b Begin -e End -t initial timestep -T temperature                                                                                  
parser.add_argument("-p","--pair",dest="pair", help="pair")
parser.add_argument("-b","--begin", dest= "begin", help=" First Snapshot")
parser.add_argument("-e","--end", dest="end", help="last Snapshot")
parser.add_argument("-T","--temperature",dest="temperature",help="temperature")

args           = parser.parse_args()
hours          = "6"
repname        = "_temperature"
#temperatures   = [300.0, 307.595, 315.381, 323.365, 331.551, 339.945, 348.55, 357.374, 366.421, 375.697, 385.208, 394.959, 404.958, 415.209,425.72,436.497]                                                                                                                                      
temperatures   = [300.0, 323.365, 348.55, 375.697, 404.958, 436.497]
name_middle    = "_snapshot" # 750 snapshots from each trajectory
array          = []
sum_array      = []
time_array     = []
J              = []
snapshots_beg  = int(args.begin)
snapshots_end  = int(args.end)
timesteps      = 500
temp           = float(args.temperature)
pair           = args.pair

pair_dic={"AC4DCAneat":{"catatom":9,"anatom":16,"litatom":0,"saltatom":0,"key":"neat"},
          "P111DCAneat":{"catatom":5,"anatom":8,"litatom":0,"saltatom":0,"key":"neat"},
          "P101TFSIneat":{"catatom":5,"anatom":9,"litatom":0,"saltatom":0,"key":"neat"},
          "AC4DCAsaltDCA":{"catatom":9,"anatom":16,"litatom":19,"saltatom":0,"key":"same salt"},
          "P111DCAsaltDCA":{"catatom":5,"anatom":8,"litatom":11,"saltatom":0,"key":"same salt"},
          "P101TFSIsaltDCA":{"catatom":5,"anatom":9,"litatom":14,"saltatom":15,"key":"diff salt"},
          "AC4DCAsaltTFSI":{"catatom":9,"anatom":16,"litatom":19,"saltatom":20,"key":"diff salt"},
          "AC4DCAsaltPF6":{"catatom":9,"anatom":16,"litatom":19,"saltatom":21,"key":"diff salt"},
          "AC4DCAsaltDCAhalf":{"catatom":9,"anatom":16,"litatom":19,"saltatom":0,"key":"same salt"},
          "AC4DCAsaltTFSIhalf":{"catatom":9,"anatom":16,"litatom":19,"saltatom":20,"key":"diff salt"},
          "AC4DCAsaltPF6half":{"catatom":9,"anatom":16,"litatom":19,"saltatom":21,"key":"diff salt"}}



key     =pair_dic[pair]['key']


os.chdir('../') #bring this back when running superscript

time_array=de.grabtime(pair+repname+str(round(temp))+'/'+'dump'+str(snapshots_beg)+'.lammpstrj')
os.chdir(pair+repname+str(round(temp)))

for i in range(snapshots_beg,snapshots_end):
        out=open('flux'+str(i)+'.dat','w')
        out.write('Time (fs)   Jx (e*Ang/fs)   Jy (e*Ang/fs)   Jz (e*Ang/fs)\n')

        J=de.splitflux('dump'+str(i)+'.lammpstrj',key)
        J=np.array(J)
        print(len(J))
        for j in range(len(J)):
                out.write(str(time_array[j])+'    '+str(J[j,0])+'   '+str(J[j,1])+'   '+str(J[j,2])+'   \n')
        out.close()
        

