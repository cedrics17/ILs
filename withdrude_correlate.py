##modules
import numpy as np

## MY DICT
mass_dic = {
	'C' : 11.611,
	'H' : 1.008,
	'N' : 13.607,
        'D' : 0.4,
        'P' : 30.974,
        'Li': 6.941
}
## my functions
def splitflux(filename,key): #filename is a variable that represents a string
        Ncat=100
        qcat=1
        Nani=100
        qani=-1
        Nlit=0
        count=0
        catarray=[]
        anaarray=[]
        saltanarray=[]
        litharray=[]
        start     =False
        J         =[]
        
        file=open(filename,'r').readlines()
        for f in file:
                if 'id' in f:
                        start=True 
                elif start:
                        array=f.strip().split()
                        if str(array[0])=="ITEM:":
                                start=False
                                anaarray=np.array(anaarray)
                                catarray=np.array(catarray)
                                litharray=np.array(litharray)
                                saltanarray=np.array(saltanarray)
                                [Jx_cat,Jy_cat,Jz_cat]=flux(catarray[:,0],catarray[:,1],catarray[:,2],catarray[:,3],Ncat,qcat)
                                [Jx_ani,Jy_ani,Jz_ani]=flux(anaarray[:,0],anaarray[:,1],anaarray[:,2],anaarray[:,3],Nani,qani)
                                if key=='diff salt' or key=="same salt":

                                        [Jx_salt,Jy_salt,Jz_salt]=flux(saltanarray[:,0],saltanarray[:,1],saltanarray[:,2],saltanarray[:,3],Nlit,qani)
                                        [Jx_lith,Jy_lith,Jz_lith]=flux(litharray[:,0],litharray[:,1],litharray[:,2],litharray[:,3],Nlit,qcat)
                                else:
                                        Jx_salt=0
                                        Jx_lith=0
                                        Jy_salt=0
                                        Jy_lith=0
                                        Jz_salt=0
                                        Jz_lith=0
                                
                                J.append([Jx_cat+Jx_ani+Jx_salt+Jx_lith, Jy_cat+Jy_ani+Jy_salt+Jy_lith, Jz_cat+Jz_ani+Jz_salt+Jz_lith])
                                catarray=[]
                                anaarray=[]
                                saltanarray=[]
                                Nlit=0
                                litharray=[]
                        elif int(array[1])<=100:
                                temp=[mass_dic[array[3]],float(array[11]),float(array[12]),float(array[13])]
                                catarray.append(temp)
                        elif int(array[1])>100 and int(array[1])<=200:
                                temp=[mass_dic[array[3]],float(array[11]),float(array[12]),float(array[13])]
                                anaarray.append(temp)        
                        elif int(array[1])>200 and array[3]!="Li":
                                temp=[mass_dic[array[3]],float(array[11]),float(array[12]),float(array[13])]
                                saltanarray.append(temp)
                        elif array[3]=="Li":
                                temp=[mass_dic[array[3]],float(array[11]),float(array[12]),float(array[13])]
                                litharray.append(temp)
                                Nlit+=1
                        else:
                                print("Error in the order of the ions and the formatting of the dump files")
        return J

def grabtime(filename):
        timestart=False
        time     =[]
        file=open(filename,'r').readlines()
        for f in file:
                if len(f.split())==2 and f.split()[0]=="ITEM:":
                        timestart=True
                
                elif timestart:
                        time.append(float(f.split()[0]))
                        timestart=False
        return time

def flux(mass,vx,vy,vz,N,q):
        totmass=np.sum(mass)
        weighted_vx=np.dot(mass,vx)/totmass	
        weighted_vy=np.dot(mass,vy)/totmass
        weighted_vz=np.dot(mass,vz)/totmass
        Jx=weighted_vx*N*q
        Jy=weighted_vy*N*q
        Jz=weighted_vz*N*q
        return Jx,Jy,Jz
        
def correlate(J):
        corr=np.zeros(len(J))
        J=np.array(J)
        n=1
        for key in range(len(J)-1):
                Jo  =J[key]
                if n > 1 :
                        J[key-1]=0
                rollJ= np.roll(J,len(J)-key,axis=0)
                corr+=np.dot(Jo,rollJ.T)
                n+=1
        for rekey in range(n):
                corr[rekey]=corr[rekey]/(n-rekey)
        return corr
	
def conductivity(filename,dt,V,T):
        integral=[]
        J       =[]
        k = 1.38e-23
        el = 1.60217e-19
        f=open(filename,'r').readlines()
        for i in range(1,len(f)):
                J.append(float(f[i].strip().split()[1]))
        integral=np.trapz(J,dx=dt)
        cond = integral/3/k/T/V*el**2/10**5
        return cond

def gofr(filename,catatom,anatom,litatom,saltatom,key):
        catarray=[]
        anarray=[]
        litarray=[]
        saltarray=[]
        start=False
        ts=0
        bins=200
        anicount=0
        catcount=0
        saltcount=0
        litcount=0
        grpair=np.zeros((bins,501))
        grani=np.zeros((bins,501))
        grcat=np.zeros((bins,501))
        grlitcat=np.zeros((bins,501))
        grlitani=np.zeros((bins,501))
        grlitlit=np.zeros((bins,501))
        grsaltcat=np.zeros((bins,501))
        grsaltani=np.zeros((bins,501))
        grsaltsalt=np.zeros((bins,501))
        grsaltlit=np.zeros((bins,501))
        file=open(filename,'r').readlines()
        boxs=float(file[6].strip().split()[1])-float(file[6].strip().split()[0])
        if key=="diff salt":
                for f in file:
                        if 'id' in f:
                                start=True
                                anicount=0
                                catcount=0
                                saltcount=0
                                litcount=0
                        elif start: 
                                array=f.strip().split()
                                if str(array[0])=="ITEM:":
                                        print(ts)
                                        start=False
                                        anarray=np.array(anarray)
                                        catarray=np.array(catarray)
                                        litarray=np.array(litarray)
                                        grani[:,ts]=cal_ind(anarray,boxs,bins)
                                        grcat[:,ts]=cal_ind(catarray,boxs,bins)
                                        grpair[:,ts]=cal_gr(catarray,anarray,boxs,bins)
                                        grlitcat[:,ts]=cal_gr(litarray,catarray,boxs,bins)
                                        grlitani[:,ts]=cal_gr(litarray,anarray,boxs,bins)
                                        grlitlit[:,ts]=cal_ind(litarray,boxs,bins)
                                        grsaltcat[:,ts]=cal_gr(saltarray,catarray,boxs,bins)
                                        grsaltani[:,ts]=cal_gr(saltarray,anarray,boxs,bins)
                                        grsaltsalt[:,ts]=cal_ind(saltarray,boxs,bins)
                                        grsaltlit[:,ts]=cal_gr(litarray,saltarray,boxs,bins)
                                        ts+=1
                                        catarray=[]
                                        anarray=[]
                                        saltarray=[]
                                        litarray=[]
                                elif int(array[2])==catatom:
                                        catcount+=1
                                        catarray.append([float(array[5]),float(array[6]),float(array[7])])
                                elif int(array[2])==anatom:
                                        anicount+=1
                                        anarray.append([float(array[5]),float(array[6]),float(array[7])])
                                elif int(array[2])==litatom:
                                        litcount+=1
                                        litarray.append([float(array[5]),float(array[6]),float(array[7])])
                                elif int(array[2])==saltatom:
                                        saltcount+=1
                                        saltarray.append([float(array[5]),float(array[6]),float(array[7])])
        elif key=="same salt":
                for f in file:
                        if 'id' in f:
                                start=True
                                anicount=0
                                catcount=0
                                litcount=0
                        elif start: 
                                array=f.strip().split()
                                if str(array[0])=="ITEM:":
                                        print(ts)
                                        start=False
                                        anarray=np.array(anarray)
                                        catarray=np.array(catarray)
                                        litarray=np.array(litarray)
                                        grani[:,ts]=cal_ind(anarray,boxs,bins)
                                        grcat[:,ts]=cal_ind(catarray,boxs,bins)
                                        grpair[:,ts]=cal_gr(catarray,anarray,boxs,bins)
                                        grlitcat[:,ts]=cal_gr(litarray,catarray,boxs,bins)
                                        grlitani[:,ts]=cal_gr(litarray,anarray,boxs,bins)
                                        grlitlit[:,ts]=cal_ind(litarray,boxs,bins)
                                        ts+=1
                                        catarray=[]
                                        anarray=[]
                                        saltarray=[]
                                        litarray=[]
                                elif int(array[2])==catatom:
                                        catcount+=1
                                        catarray.append([float(array[5]),float(array[6]),float(array[7])])
                                elif int(array[2])==anatom:
                                        anicount+=1
                                        anarray.append([float(array[5]),float(array[6]),float(array[7])])
                                elif int(array[2])==litatom:
                                        litcount+=1
                                        litarray.append([float(array[5]),float(array[6]),float(array[7])])
        elif key=="neat":
                for f in file:
                        if 'id' in f:
                                start=True
                                anicount=0
                                catcount=0
                        elif start: 
                                array=f.strip().split()
                                if str(array[0])=="ITEM:":
                                        print(ts)
                                        start=False
                                        anarray=np.array(anarray)
                                        catarray=np.array(catarray)
                                        litarray=np.array(litarray)
                                        grani[:,ts]=cal_ind(anarray,boxs,bins)
                                        grcat[:,ts]=cal_ind(catarray,boxs,bins)
                                        grpair[:,ts]=cal_gr(catarray,anarray,boxs,bins)
                                        ts+=1
                                        catarray=[]
                                        anarray=[]
                                        saltarray=[]
                                        litarray=[]


                                elif int(array[2])==catatom:
                                        catcount+=1
                                        catarray.append([float(array[5]),float(array[6]),float(array[7])])
                                elif int(array[2])==anatom:
                                        anicount+=1
                                        anarray.append([float(array[5]),float(array[6]),float(array[7])])

        return grpair, grani, grcat, grlitcat, grlitani, grlitlit, grsaltcat, grsaltani, grsaltsalt, grsaltlit, boxs, catcount, anicount, litcount, saltcount

def cal_gr(catarray,anarray,boxs,bins):
        rmax=0.5*boxs
        rmax2=rmax**2
        dr=rmax/bins
        hist=np.zeros(bins)
        for ipart in (catarray):
                        
                for jpart in (anarray):
                        xr = ipart[0]-jpart[0]
                        yr=ipart[1]-jpart[1]
                        zr=ipart[2]-jpart[2]
                        xr-= boxs*int(round(xr/boxs))
                        yr-= boxs*int(round(xr/boxs))
                        zr-= boxs*int(round(xr/boxs))
                        
                        r2 = xr**2+yr**2+zr**2
                               
                        if r2 < rmax2:
                               r=np.sqrt(r2)
                               n=int(r/dr)
                               hist[n] += 1
        return hist
        
def cal_ind(catarray,boxs,bins):
        rmax=0.5*boxs
        rmax2=rmax**2
        dr=rmax/bins
        hist=np.zeros(bins)
        for ipart in catarray:
                for jpart in catarray[1:]:
                        xr = ipart[0]-jpart[0]
                        yr=ipart[1]-jpart[1]
                        zr=ipart[2]-jpart[2]
                        xr-= boxs*int(round(xr/boxs))
                        yr-= boxs*int(round(xr/boxs))
                        zr-= boxs*int(round(xr/boxs))
                        r2 = xr**2+yr**2+zr**2

                        if r2 < rmax2:
                               r=np.sqrt(r2)
                               n=int(r/dr)
                               hist[n] += 1
        return hist




