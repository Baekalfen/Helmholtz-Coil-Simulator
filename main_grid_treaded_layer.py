# -*- coding: utf-8 -*-
##from multiprocessing import Process
##from multiprocessing import Pool

from visual import *
from math import *
from sys import platform
import time

#######################################
#                                     #
#   Author: Mads Ynddal               #
#   All Rights Reserved 2012          #
#                                     #
#######################################


#######################################
#
#   Settings - Start
#

#Window setup:
Width=800               #Width of window
Height=750              #Height of window

### Tekniske specifikationer
FPS=60
cpu_threads=2  #Windows kan kun håndtere 1 tråd
defi=1.        #punkter pr. dm
grid_sizex=15
grid_sizey=15
grid_sizez=15



use_layers=1
active_layer=grid_sizey/2
OP_ref_spacing=3
coil_1=1
coil_2=1
max_blen=20
hue_multiplier=3/6.#3./6
strength_as_color=1
vector_pointers=1

debug_vectors3=0
debug_vectors3_multiplier=10**6
debug_offset=0
###

### Fysik og matematik
Vp=4*pi*10**-7
I=2
constant=Vp*I/(4*pi)
coiloffset=-15./2 #Distance from each coil divided by two
dm=15*8*2*pi    #Definitionsmængden for funktionen (rundes altid ned)
###

#
#   Settings - End
#
#######################################


#######################################
#
#   INITIALIZING - Start
#
scene = display(title='Helmholtz Coil',width=Width, height=Height,autoscale = False,scale=(0.03,0.03,0.03))
#scene.stereo = 'redcyan'
procent=0
vectors_threaded=[]
coil1=curve(pos=[])
coil2=curve(pos=[])
vectors=[]
col=0
P=[]
temp=[]
temp2=[]

if platform=="win32":
    print "WARNING! Windows can't run multiple threads!\nForcing cpu_threads to 1"
    cpu_threads=1

if cpu_threads>1:
    from multiprocessing import Process
    from multiprocessing import Pool
#
#   INITIALIZING - End
#
#######################################




#######################################
#       Optegner spoler ud fra funktionen
for tt in range(int(dm*defi)+1):
    t=tt/defi

    x=t*0.0005+15./2+debug_offset
    y=31.5/2*sin(t)
    z=31.5/2*cos(t)
    if coil_1==1:
        coil1.append((x,y,z))
    else:
        coil1.append((0,0,0))


    x=t*0.0005-15./2-debug_offset
    y=31.5/2*sin(t)
    z=31.5/2*cos(t)
    if coil_2:
        coil2.append((x,y,z))
    else:
        coil2.append((0,0,0))
#
#######################################

#######################################
#       Vektor regneregler
def vlen(a):
    return sqrt(a[0]**2+a[1]**2+a[2]**2)
    #Vector length

def vsub(a,b):
    return [a[0]-b[0],a[1]-b[1],a[2]-b[2]]
    #Substract vectors a,b

def vadd(a,b):
    return [a[0]+b[0],a[1]+b[1],a[2]+b[2]]
    #Add vectors a,b

def vdiv(a,b):
    return [a[0]/float(b),a[1]/float(b),a[2]/float(b)]
    #Divide vector by scalar b

def cprod(a,b):
    return [a[1]*b[2]-a[2]*b[1],
            a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0]]
    #Cross product
#
#######################################

#######################################
#       Biot-Savarts lov
def dlxrr3(dl,r):
    return vdiv(cprod(dl,r),vlen(r)**3)

def Apply_contant(Bsum1,Bsum2):
    Bsum=vdiv(vadd(Bsum1,Bsum2),1/constant)
    #Bsum=vdiv(vsub(Bsum1,Bsum2),1/constant)
    Bsum1=vdiv(Bsum1,1/constant)
    Bsum2=vdiv(Bsum2,1/constant)
    return Bsum

def inte(OP):
    global coiloffset,col
    Bsum1=[0,0,0]
    Bsum2=[0,0,0]

    #Første spole
    coiloffset*=-1
    for tt in range(int(dm*defi)):
        t=tt/float(defi)
        s1,s2=s1s2(t)
        dl=vsub(s2,s1)
        m=vdiv(vadd(s1,s2),2)
        r=vsub(OP,m)
        Bsum1=vadd(Bsum1,dlxrr3(dl,r))
        if not coil_1:
            Bsum1=[0,0,0]

    #Anden spole
    coiloffset*=-1
    for tt in range(int(dm*defi)):
        t=tt/float(defi)
        s1,s2=s1s2(t)
        dl=vsub(s2,s1)
        m=vdiv(vadd(s1,s2),2)
        r=vsub(OP,m)
        Bsum2=vadd(Bsum2,dlxrr3(dl,r))
        if not coil_2:
            Bsum2=[0,0,0]
    return Bsum1,Bsum2
#
#######################################

#######################################
#       Udregn funktionsværdi til tiden 't'
def s1s2(t1):
    s1=[t1*0.0005+coiloffset,31.5/2*sin(t1),31.5/2*cos(t1)]
    t2=t1+1/float(defi)
    s2=[t2*0.0005+coiloffset,31.5/2*sin(t2),31.5/2*cos(t2)]
    return s1,s2
#
#######################################

#######################################
#       Udregn vektorstyrke og retning
def cal_vectors(xx,yy,zz):
    global vectors_threaded,procent
    procent+=1
    #print procent
    P=[xx*OP_ref_spacing-((grid_sizex-1)*OP_ref_spacing)/2,yy*OP_ref_spacing-((grid_sizey-1)*OP_ref_spacing)/2,zz*OP_ref_spacing-((grid_sizez-1)*OP_ref_spacing)/2]
    n=xx+yy+zz
    Bsum=vdiv(Apply_contant(*inte(P)),1./debug_vectors3_multiplier)
    Blen=vlen(Bsum)
    return (P,Bsum,Blen)
#
#######################################


#######################################
#       Distribuerer opgaver til CPU-kerner
if cpu_threads>1:
    pool = Pool(processes=cpu_threads)# start 4 worker processes
result=[]
P=[]
Bsum=[]
time_stamp=time.time()
for yy in range(grid_sizey):
    for xx in range(grid_sizex):
        for zz in range(grid_sizez):
            if cpu_threads>1:
                result.append(pool.apply_async(cal_vectors, [xx,yy,zz]))
            else:
                vectors_threaded.append(cal_vectors(xx,yy,zz))

### Indsamler svar fra CPU-kerner
if cpu_threads>1:
    for n in range(grid_sizex*grid_sizey*grid_sizez):
        vectors_threaded.append(result[n].get())
#
#######################################

#######################################
#       Vektorfelt bliver rendereret
for n in range(len(vectors_threaded)):
    P,Bsum,Blen=vectors_threaded[n]
    if strength_as_color==1:
        Blen=vlen(Bsum)
        vcolor=color.hsv_to_rgb((1./4-(Blen*1./(max_blen/2)*hue_multiplier),1,1))
        Bsum=vdiv(Bsum,Blen)
    else:
        vcolor=color.red
    if Blen<max_blen:
        layer=int(n/(len(vectors_threaded)/float(grid_sizey)))
        #print layer

        for i in range(grid_sizey):
            temp.append([])
            temp2.append([])

        #a=raw_input()
        temp[layer].append(curve(visible=False,color=vcolor,pos=[(P[0],P[1],P[2]),(P[0]+Bsum[0],P[1]+Bsum[1],P[2]+Bsum[2])]))
        if vector_pointers==1:
            temp2[layer].append(sphere(visible=False,os=(P[0]+Bsum[0],P[1]+Bsum[1],P[2]+Bsum[2]), radius=0.1, color=color.white, opacity=1))
#
#######################################

print "Processing lasted: "+str(time.time()-time_stamp)[0:5],"sec\nUtilizing",cpu_threads,"processor threads, to animate:",grid_sizez*grid_sizey*grid_sizex,"vectors"

#######################################
#       Indsætter partikel og
#       indstiller kamera
center_point = sphere (pos=(0,0,0), radius=1, color=color.red, opacity=0.5)
particle = sphere (pos=(0,0,-12), radius=1, color=color.green, opacity=0.4)
speed = label()
label(pos=(10,0,0),text=("x"))
label(pos=(0,10,0),text=("y"))
label(pos=(0,0,10),text=("z"))

def toggle_layer(l):
    if temp[l][0].visible==True:
        for n in range(len(temp[l])):
                temp[l][n].visible=False
                if vector_pointers==1:
                    temp2[l][n].visible=False
    elif temp[l][0].visible==False:
        for n in range(len(temp[l])):
                temp[l][n].visible=True
                if vector_pointers==1:
                    temp2[l][n].visible=True

if use_layers==1:
    toggle_layer(active_layer)
else:
    for n in range(grid_sizey):
        toggle_layer(n)

i=0.
auto_rotate=1
while(1):
    rate(FPS)
    if auto_rotate==1:
        i+=1
        scene.forward=(-1*sin(i/FPS/5),-1,-1*cos(i/FPS/5))

    #Particle
    Bsum=vdiv(Apply_contant(*inte(particle.pos)),1./debug_vectors3_multiplier)
    particle.pos.x+=Bsum[0]/30.
    particle.pos.y+=Bsum[1]/30.
    particle.pos.z+=Bsum[2]/30.
    speed.pos=particle.pos
    speed.pos.x+=4
    speed.text=str(vlen(Bsum))[0:3]
    #Particle

### Bruger input
    if scene.kb.keys: # is there an event waiting to be processed?
        c = scene.kb.getkey() # obtain keyboard information
        if c=="up":
            if not active_layer+1==grid_sizey:
                toggle_layer(active_layer)
                active_layer+=1
                toggle_layer(active_layer)

        if c=="down":
            if not active_layer==0:
                toggle_layer(active_layer)
                active_layer-=1
                toggle_layer(active_layer)

        if c=="r":
            particle.pos=(20,0,-12)
        if c=="t":
            particle.pos=(0,0,-12)
        if c=="y":
            particle.pos=(5,0,-13)
        if c=="u":
            particle.pos=(14,0,-15)
        if c=="w":
            auto_rotate=0
            scene.forward=(0,-1,0)
        if c=="s":
            auto_rotate=0
            scene.forward=(-1,0,0)
        if c=="a":
            auto_rotate=0
            scene.forward=(0,0,-1)
        if c=="q":
            auto_rotate=0
            scene.forward=(-1,-1,-1)
        if c=="d":
            if auto_rotate==0:
                auto_rotate=1
            else:
                auto_rotate=0
#
#######################################