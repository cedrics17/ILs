#Author: Cedric Salame
#Script Name: calc_cond.py
#Date Created: Jun 6th 2021
#Last Mod Date:
#Last Modification:

#Program: Python 3
import os
import numpy as np
import correlate_gofr as de

#Description: This script will calculate correlation functions for every temperature and trajectory and average it on a temperature basis. It also returns the conductivity
#temperatures   = [300.0, 307.595, 315.381, 323.365, 331.551, 339.945, 348.55, 357.374, 366.421, 375.697, 385.208, 394.959, 404.958, 415.209,425.72,436.497]
temperatures   = [300.0, 323.365, 348.55, 375.697, 404.958, 436.497]
step           = 10
liquid         ="P111DCAneat"


pair_dic={"AC4DCAneat":{"xlength":33.091155e-10},
          "P111DCAneat":{"xlength":33.6047e-10},
          "P101TFSIneat":{"xlength":5},
          "AC4DCAsaltDCA":{"xlength":33.8085e-10},
          "P111DCAsaltDCA":{"xlength":34.49496e-10},
          "P101TFSIsaltDCA":{"xlength":5},
          "AC4DCAsaltTFSI":{"xlength":9},
          "AC4DCAsaltPF6":{"xlength":9},
          "AC4DCAsaltDCAhalf":{"xlength":9},
          "AC4DCAsaltTFSIhalf":{"xlength":9},
          "AC4DCAsaltPF6half":{"xlength":9}}


Volume         = pair_dic[liquid]["xlength"]**3

os.chdir("SingleTraj_"+liquid+'/corr_functions')

out=open('conductivities'+'_'+liquid+'.dat','w')
out.write("Temp(K)   Cond(S/m)\n")
for temp in temperatures:
     cond=de.conductivity('corr'+str(round(temp))+'.dat',step,V,temp)
     out.write(str(round(temp))+"   "+str(cond)+"\n")
out.close()
