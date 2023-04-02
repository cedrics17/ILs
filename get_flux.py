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
os.mkdir('fluxes')

for i in range(snapshots_beg,snapshots_end):
        outJ=open('flux'+str(i)+'.dat','w')
        outJcat=open('fluxes/fluxCat'+str(i)+'.dat','w')
        outJsalt=open('fluxes/fluxSalt'+str(i)+'.dat','w')
        outJani=open('fluxes/fluxAni'+str(i)+'.dat','w')
        outJlith=open('fluxes/fluxLith'+str(i)+'.dat','w')
        outJ.write('Time (fs)   Jx (e*Ang/fs)   Jy (e*Ang/fs)   Jz (e*Ang/fs)\n')
        outJcat.write('Time (fs)   Jx (e*Ang/fs)   Jy (e*Ang/fs)   Jz (e*Ang/fs)\n')
        outJani.write('Time (fs)   Jx (e*Ang/fs)   Jy (e*Ang/fs)   Jz (e*Ang/fs)\n')
        outJsalt.write('Time (fs)   Jx (e*Ang/fs)   Jy (e*Ang/fs)   Jz (e*Ang/fs)\n')
        ouJlith.write('Time (fs)   Jx (e*Ang/fs)   Jy (e*Ang/fs)   Jz (e*Ang/fs)\n')
        J,Jcat,Jani,Jsalt,Jlith=de.splitflux('dump'+str(i)+'.lammpstrj',key)
        J=np.array(J)
        Jcat=np.array(Jcat)
        Jani=np.array(Jani)
        Jsalt=np.array(Jsalt)
        Jlith=np.array(Jlith)
        print(len(J))
        for j in range(len(J)):
                outJ.write(str(time_array[j])+'    '+str(J[j,0])+'   '+str(J[j,1])+'   '+str(J[j,2])+'   \n')
                outJcat.write(str(time_array[j])+'    '+str(Jcat[j,0])+'   '+str(Jcat[j,1])+'   '+str(Jcat[j,2])+'   \n')
                outJani.write(str(time_array[j])+'    '+str(Jani[j,0])+'   '+str(Jani[j,1])+'   '+str(Jani[j,2])+'   \n')
                outJsalt.write(str(time_array[j])+'    '+str(Jsalt[j,0])+'   '+str(Jsalt[j,1])+'   '+str(Jsalt[j,2])+'   \n')
                outJlith.write(str(time_array[j])+'    '+str(Jlith[j,0])+'   '+str(Jlith[j,1])+'   '+str(Jlith[j,2])+'   \n')
        outJ.close()
        outJcat.close()
        outJani.close()
        outJsalt.close()
        outJlith.close()
        

