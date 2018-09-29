from vpython import *
from sys import platform
import numpy as np
import scipy.linalg
import time

#######################################
#                                     #
#   Author: Mads Ynddal               #
#   All Rights Reserved 2018          #
#                                     #
#######################################


#######################################
#
#   Settings - Start
#

Width=800               #Width of window
Height=750              #Height of window

FPS=60
grid_sizex=12
grid_sizey=12
grid_sizez=12


auto_rotate=0
OP_ref_spacing=3
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
scene = canvas(title='Helmholtz Coil',width=Width, height=Height,autoscale = False,scale=(0.03,0.03,0.03))
vectors_threaded=[]
vectors=[]
col=0
P=[]
temp=[]
temp2=[]

#
#   INITIALIZING - End
#
#######################################


#######################################
#       Calculate vectors


number_of_coils = 2

coils = np.empty(shape=(number_of_coils, int(dm*1)+1, 3))
coils[:, :, 0] = (np.arange(number_of_coils).reshape(number_of_coils,1)*2-1)*coiloffset # Coil placement
coils[:, :, 0] += np.arange(int(dm*1)+1) * 0.0005
coils[:, :, 1] = 31.5/2*np.sin(np.arange(int(dm)+1))
coils[:, :, 2] = 31.5/2*np.cos(np.arange(int(dm)+1))

coils_ = []
for n in range(number_of_coils):
    coils_.append(curve(pos=[[y for y in x] for x in coils[n]]))

# Biot-Savart's law
# https://en.wikipedia.org/wiki/Biot–Savart_law
# Finds the electromagnetic force of a point
def force(OP):
    AR = OP-(coils[:,:-1, :] + coils[:,1:, :])/2
    return np.sum(np.sum(np.cross(coils[:,1:, :] - coils[:,:-1, :], AR, axis=2) / np.linalg.norm(AR, axis=2).reshape(number_of_coils,int(dm),1)**3, axis=1),axis=0) / (1/constant) / (1./debug_vectors3_multiplier)


def cal_vectors(xx,yy,zz):
    global vectors_threaded

    P=np.asarray([
        xx*OP_ref_spacing-((grid_sizex-1)*OP_ref_spacing)/2,
        yy*OP_ref_spacing-((grid_sizey-1)*OP_ref_spacing)/2,
        zz*OP_ref_spacing-((grid_sizez-1)*OP_ref_spacing)/2
    ])

    Bsum=force(P)
    Blen=np.linalg.norm(Bsum)
    return (P,Bsum,Blen)

result=[]
P=[]
Bsum=[]
time_stamp=time.time()
for yy in range(grid_sizey):
    for xx in range(grid_sizex):
        for zz in range(grid_sizez):
            vectors_threaded.append(cal_vectors(xx,yy,zz))


#######################################
#       Vectorfield rendering
from collections import namedtuple
Color = namedtuple('Color', 'x y z')
for n in range(len(vectors_threaded)):
    P,Bsum,Blen=vectors_threaded[n]
    if strength_as_color==1:
        Blen=np.linalg.norm(Bsum)
        vcolor=color.hsv_to_rgb(Color(1./4-(Blen*1./(max_blen/2)*hue_multiplier),1,1))
        Bsum=np.asarray(Bsum) / Blen
    else:
        vcolor=color.red
    if True:
    # if Blen<max_blen:
        layer=int(n/(len(vectors_threaded)/float(grid_sizey)))
        #print layer

        for i in range(grid_sizey):
            temp.append([])
            temp2.append([])

        temp[layer].append(curve(visible=True,color=vcolor,pos=[(P[0],P[1],P[2]),(P[0]+Bsum[0],P[1]+Bsum[1],P[2]+Bsum[2])]))
        if vector_pointers==1:
            temp2[layer].append(sphere(visible=True,os=(P[0]+Bsum[0],P[1]+Bsum[1],P[2]+Bsum[2]), radius=0.1, color=color.white, opacity=1))

print("Processing lasted: "+str(time.time()-time_stamp)[0:5],"sec\n to animate:",grid_sizez*grid_sizey*grid_sizex,"vectors")

center_point = sphere (pos=vector(0,0,0), radius=1, color=color.red, opacity=0.5)
particle = sphere (pos=vector(0,0,-12), radius=1, color=color.green, opacity=0.4)
speed = label()
label(pos=vector(10,0,0),text=("x"))
label(pos=vector(0,10,0),text=("y"))
label(pos=vector(0,0,10),text=("z"))

def vec2tup(v):
    return (v.x, v.y, v.z)

i=0.
while(1):
    rate(FPS)
    if auto_rotate==1:
        i+=1
        scene.forward=vector(-1*sin(i/FPS/5),-1,-1*cos(i/FPS/5))

    #Particle
    Bsum=force(vec2tup(particle.pos))
    particle.pos.x+=Bsum[0]/30.
    particle.pos.y+=Bsum[1]/30.
    particle.pos.z+=Bsum[2]/30.
    speed.pos=particle.pos
    speed.pos.x+=4
    speed.text=str(np.linalg.norm(Bsum))[0:3]

