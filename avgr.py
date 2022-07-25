#Author: Cedric Salame
#Script Name: average g(r)
#Date Created: Jun 6th 2021
#Last Mod Date:
#Last Modification:

#Program: Python 3
import os
import numpy as np
import correlate_gofr as de
import argparse

hours          = "6"
repname        = "_temperature"
temperatures   = [300.0, 323.365, 348.55, 375.697, 404.958, 436.497]
name_middle    = "_snapshot" # 750 snapshots from each trajectory
grname         ='averagegr'
pair           = []
ani            =[]
cat            =[]
litani=[]
litcat=[]
litlit=[]
saltcat=[]
saltani=[]
saltlit=[]
saltsalt=[]
bins           = 200
snapshots_beg  = 1
snapshots_end  = 6001
timesteps      = 501
dist=[]
liquid="P111DCAneat" #change depending on the nature of the liquid

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


catatom        = pair_dic[liquid]["catatom"]
anatom         = pair_dic[liquid]["anatom"]
litatom        = pair_dic[liquid]["litatom"]
saltatom       = pair_dic[liquid]["saltatom"]
key            = pair_dic[liquid]["key"]

os.chdir("SingleTraj_"+liquid)

for temp in temperatures:
    out=open(grname+str(int(round(temp)))+'.dat','w')
    if key=="neat":
        out.write('Distance (A)    Cat-Ani    Ani-Ani    Cat-Cat\n')
        count=1
        file=open(liquid+repname+str(int(round(temp)))+"/gr1.dat",'r').readlines()
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
            file=open(liquid+repname+str(int(round(temp)))+"/gr"+str(i)+".dat",'r').readlines()
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

    if key=="same salt":
        out.write('Distance (A)    Cat-Ani    Ani-Ani    Cat-Cat    Li-Ani   Li-Cat   Li-Li\n')
        count=1
        file=open(liquid+repname+str(int(round(temp)))+"/gr1.dat",'r').readlines()
        for m in range(1,len(file)):
            pair.append(float(file[m].strip().split()[1]))
            ani.append(float(file[m].strip().split()[2]))
            cat.append(float(file[m].strip().split()[3]))
            litani.append(float(file[m].strip().split()[4]))
            litcat.append(float(file[m].strip().split()[5]))
            litlit.append(float(file[m].strip().split()[6]))
            dist.append(float(file[m].strip().split()[0]))
        sumpair=pair.copy()
        sumani=ani.copy()
        sumcat=cat.copy()
        sumlitani=litani.copy()
        sumlitcat=licat.copy()
        sumlitlit=litlit.copy()
        pair=[]
        cat=[]
        ani=[]
        litani=[]
        litcat=[]
        litlit=[]
        for i in range(2,snapshots_end):
            file=open(liquid+repname+str(int(round(temp)))+"/gr"+str(i)+".dat",'r').readlines()
            for f in range(1,len(file)):
                pair.append(float(file[f].strip().split()[1]))
                ani.append(float(file[f].strip().split()[2]))
                cat.append(float(file[f].strip().split()[3]))
                litani.append(float(file[m].strip().split()[4]))
                litcat.append(float(file[m].strip().split()[5]))
                litlit.append(float(file[m].strip().split()[6]))
            sumpair=pair.copy()
            sumani=ani.copy()
            sumcat=cat.copy()
            sumlitani=litani.copy()
            sumlitcat=licat.copy()
            sumlitlit=litlit.copy()
            pair=[]
            cat=[]
            ani=[]
            litani=[]
            litcat=[]
            litlit=[]
            count+=1

            print(count)
        for i in range(len(sumpair)):
            out.write(str(dist[i])+'    '+str(sumpair[i]/float(count))+'    '+str(sumani[i]/float(count))+'    '+str(sumcat[i]/float(count))+'   '+str(sumlitani[i]/float(count))+'   '+str(sumlitcat[i]/float(count))+'   '+str(sumlitlit[i]/float(count))+'\n')
        out.close()
        print('Done with '+str(temp))
        dist=[]

    if key=="diff salt":
        out.write('Distance (A)    Cat-Ani    Ani-Ani    Cat-Cat    Li-Ani   Li-Cat   Li-Li   Salt-Cat   Salt-Ani    Salt-Salt   Salt-Lit\n')
        count=1
        file=open(liquid+repname+str(int(round(temp)))+"/gr1.dat",'r').readlines()
        for m in range(1,len(file)):
            pair.append(float(file[m].strip().split()[1]))
            ani.append(float(file[m].strip().split()[2]))
            cat.append(float(file[m].strip().split()[3]))
            litani.append(float(file[m].strip().split()[4]))
            litcat.append(float(file[m].strip().split()[5]))
            litlit.append(float(file[m].strip().split()[6]))
            saltcat.append(float(file[m].strip().split()[7]))
            saltani.append(float(file[m].strip().split()[8]))
            saltsalt.append(float(file[m].strip().split()[9]))
            saltlitt.append(float(file[m].strip().split()[10]))
            dist.append(float(file[m].strip().split()[0]))
        sumpair=pair.copy()
        sumani=ani.copy()
        sumcat=cat.copy()
        sumlitani=litani.copy()
        sumlitcat=licat.copy()
        sumlitlit=litlit.copy()
        sumsaltcat=saltcat.copy()
        sumsaltani=saltani.copy()
        sumsaltsalt=saltsalt.copy()
        sumsaltlit=saltlit.copy()
        pair=[]
        cat=[]
        ani=[]
        litani=[]
        litcat=[]
        litlit=[]
        saltcat=[]
        saltani=[]
        saltlit=[]
        saltsalt=[]
        for i in range(2,snapshots_end):
            file=open(liquid+repname+str(int(round(temp)))+"/gr"+str(i)+".dat",'r').readlines()
            for f in range(1,len(file)):
                pair.append(float(file[f].strip().split()[1]))
                ani.append(float(file[f].strip().split()[2]))
                cat.append(float(file[f].strip().split()[3]))
                litani.append(float(file[m].strip().split()[4]))
                litcat.append(float(file[m].strip().split()[5]))
                litlit.append(float(file[m].strip().split()[6]))
                saltcat.append(float(file[m].strip().split()[7]))
                saltani.append(float(file[m].strip().split()[8]))
                saltsalt.append(float(file[m].strip().split()[9]))
                saltlitt.append(float(file[m].strip().split()[10]))
            sumpair=pair.copy()
            sumani=ani.copy()
            sumcat=cat.copy()
            sumlitani=litani.copy()
            sumlitcat=licat.copy()
            sumlitlit=litlit.copy()
            sumsaltcat=saltcat.copy()
            sumsaltani=saltani.copy()
            sumsaltsalt=saltsalt.copy()
            sumsaltlit=saltlit.copy()
            pair=[]
            cat=[]
            ani=[]
            litani=[]
            litcat=[]
            litlit=[]
            saltcat=[]
            saltani=[]
            saltlit=[]
            saltsalt=[]
            count+=1

            print(count)    
        for i in range(len(sumpair)):
            out.write(str(dist[i])+'    '+str(sumpair[i]/float(count))+'    '+str(sumani[i]/float(count))+'    '+str(sumcat[i]/float(count))+'   '+str(sumlitani[i]/float(count))+'   '+str(sumlitcat[i]/float(count))+'   '+str(sumlitlit[i]/float(count))+'   '+str(sumsaltcat[i]/float(count))+'   '+str(sumsaltani[i]/float(count))+'   '+str(sumsaltsalt[i]/float(count))+'   '+str(sumsaltlit[i]/float(count))+'\n')
        out.close()
        print('Done with '+str(temp))
        dist=[]
