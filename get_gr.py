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
temperatures   = [300.0, 323.365,348.55, 404.958, 436.497]
name_middle    = "_snapshot" # 750 snapshots from each trajectory
array          = []

bins           = 200
snapshots_beg  = int(args.begin)
snapshots_end  = int(args.end)
timesteps      = 501
temp           = float(args.temperature)
pair           =args.pair

pair_dic={"AC4DCAneat":{"catatom":9,"anatom":16,"litatom":0,"saltatom":0,"key":"neat"},
          "P111DCAneat":{"catatom":5,"anatom":8,"litatom":0"saltatom":0,"key":"neat"},
          "P101TFSIneat":{"catatom":5,"anatom":9,"litatom":0"saltatom":0},"key":"neat"},
          "AC4DCAsaltDCA":{"catatom":9,"anatom":16,"litatom":19,"saltatom":0,"key":"same salt"},
          "P111DCAsaltDCA":{"catatom":5,"anatom":8,"litatom":11,"saltatom":,"key":"same salt"},
          "P101TFSIsaltDCA":{"catatom":5,"anatom":9,"litatom":14,"saltatom":15,"key":"diff salt"},
          "AC4DCAsaltTFSI":{"catatom":9,"anatom":16,"litatom":19,"saltatom":20,"key":"diff salt"},
          "AC4DCAsaltPF6":{"catatom":9,"anatom":16,"litatom":19,"saltatom":21,"key":"diff salt"},
          "AC4DCAsaltDCAhalf":{"catatom":9,"anatom":16,"litatom":19,"saltatom":0,"key":"same salt"},
          "AC4DCAsaltTFSIhalf":{"catatom":9,"anatom":16,"litatom":19,"saltatom":20,"key":"diff salt"},
          "AC4DCAsaltPF6half":{"catatom":9,"anatom":16,"litatom":19,"saltatom":21,"key":"diff salt"}}


catatom        = pair_dic[pair]["catatom"]
anatom         = pair_dic[pair]["anatom"]
litatom        = pair_dic[pair]["litatom"]
saltatom       = pair_dic[pair]["saltatom"]
key            = pair_dic[pair]["key"]


os.chdir('../') #bring this back when running superscript


os.chdir(pair+repname+str(round(temp)))

for i in range(snapshots_beg,snapshots_end):
        out=open('gr'+str(i)+'.dat','w')
        out.write('Distance (A)    Cat-Ani    Ani-Ani    Cat-Cat\n')
        pair,ani,cat,litcat,litani,litlit,saltcat,saltani,saltsalt,saltlit,boxs,catcount,anicount,litcount,saltcount=de.gofr('dump'+str(i)+'.lammpstrj',catatom,anatom,litatom,saltatom,key)
        dr=0.5*boxs/bins
        pair=np.array(pair)
        ani=np.array(ani)
        cat=np.array(cat)
        litcat=np.array(litcat)
        litani=np.array(litani)
        litlit=np.array(litlit)
        gofrpair=np.sum(pair,axis=1)/timesteps
        gofrani=np.sum(ani,axis=1)/timesteps
        gofrcat=np.sum(cat,axis=1)/timesteps
        if key=="same salt":

                gofrlitcat=np.sum(litcat,axis=1)/timesteps
                gofrlitani=np.sum(litani,axis=1)/timesteps
                gofrlitlit=np.sum(litlit,axis=1)/timesteps
        elif key=="diff salt":
                gofrlitcat=np.sum(litcat,axis=1)/timesteps
                gofrlitani=np.sum(litani,axis=1)/timesteps
                gofrlitlit=np.sum(litlit,axis=1)/timesteps
                gofrsaltcat=np.sum(saltcat,axis=1)/timesteps
                gofrsaltani=np.sum(saltani,axis=1)/timesteps
                gofrsaltsalt=np.sum(saltsalt,axis=1)/timesteps
                gofrsaltlit=np.sum(saltlit,axis=1)/timesteps
        rvalues=np.zeros(bins)
        procpair=np.zeros(bins)
        procani=np.zeros(bins)
        proccat=np.zeros(bins)
        proclitcat=np.zeros(bins)
        proclitani=np.zeros(bins)
        proclitlit=np.zeros(bins)
        procsaltcat=np.zeros(bins)
        procsaltani=np.zeros(bins)
        procsaltsalt=np.zeros(bins)
        procsaltlit=np.zeros(bins)
        rhopair=anicount/boxs**3
        rhocatpair=catcount/boxs**3
        rhocat=(catcount-1)/boxs**3
        rhoani=(anicount-1)/boxs**3
        rhosaltind=(litcount-1)/boxs**3
        rhosaltpair=litcount/boxs**3
        print(rhopair)
        print(anicount)
        print(boxs**3)
        for j in range(bins):
                rvalues[j]=dr*j
                if j>=1:

                        procpair[j]=gofrpair[j]/4/np.pi/rvalues[j]**2/rhopair
                        procani[j]=gofrani[j]/4/np.pi/rvalues[j]**2/rhoani
                        proccat[j]=gofrcat[j]/4/np.pi/rvalues[j]**2/rhocat
                        if key=="same salt":

                                proclitcat[j]=gofrlitcat[j]/4/np.pi/rvalues[j]**2/rhocatpair
                                proclitani[j]=gofrlitani[j]/4/np.pi/rvalues[j]**2/rhopair
                                proclitlit[j]=gofrlitlit[j]/4/np.pi/rvalues[j]**2/rhosaltind

                        elif key=="diff salt":
                                proclitcat[j]=gofrlitcat[j]/4/np.pi/rvalues[j]**2/rhocatpair
                                proclitani[j]=gofrlitani[j]/4/np.pi/rvalues[j]**2/rhopair
                                proclitlit[j]=gofrlitlit[j]/4/np.pi/rvalues[j]**2/rhosaltind
                                procsaltcat[j]=gofrsaltcat[j]/4/np.pi/rvalues[j]**2/rhocatpair
                                procsaltani[j]=gofrsaltani[j]/4/np.pi/rvalues[j]**2/rhopair
                                procsaltsalt[j]=gofrsaltsalt[j]/4/np.pi/rvalues[j]**2/rhosaltind
                                procsaltlit[j]=gofrsaltlit[j]/4/np.pi/rvalues[j]**2/rhosaltpair
                out.write(str(rvalues[j])+'    '+str(procpair[j])+'    '+str(procani[j])+'    '+str(proccat[j])+'    '+str(proclitani[j])+'   '+str(proclitcat[j])+'   '+str(proclitlit[j])+'   '+str(procsaltcat[j])+'   '+ str(procsaltani[j])+'   '+str(procsaltsalt[j])+'   '+str(procsaltlit[j])+'   \n')
        out.close()

