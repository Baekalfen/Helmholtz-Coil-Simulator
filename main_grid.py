# -*- coding: utf-8 -*-

from visual import *
from math import *
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

#Wireframe: 1 wire, 2 faces, 3 both
wireframe=2

#Floor: 1 on, 0 off
Floor=0

#Window setup:
Width=800               #Width of window
Height=750              #Height of window
Center=(0,70,0)         #Point for the camera to look
AOI=(25,40,1)           #Area of Interest, for the camera to cover
Backcolor=(.5,.5,.5)    #Background color
FOV=pi/9.0              #Field of view in radians
Allowspin=1             #Allow or disallow spinning the scene
Scrresx=1280            #input screen resolution

#Animation
D2=0                    #2D True/False
Sides=20                #Number of sides on 3D model to render
Definition=20           #Number of rows vertically to render

#Debug
Debug=0                 #If enabled a wireframe and faces scene will de drawn

FPS=60

strength_as_color=1

debug_vectors1=0
debug_vectors2=0
debug_vectors3=0
debug_vectors3_multiplier=10**6
#
#   Settings - End
#
#######################################

# Building scenes
scene = display(title='Helmholtz coin',width=Width, height=Height,autoscale = False,scale=(0.03,0.03,0.03))
#scene1 = display(title='Solid of Revolution',width=Width, height=Height,center=Center, background=Backcolor,x=Scrresx-Width,y=0,fov=FOV,userspin=Allowspin)

coil1=curve(pos=[])
coil2=curve(pos=[])
vectors=[]
col=0
debug_offset=0
Vp=4*pi*10**-7
I=1
constant=Vp*I/(4*pi)

d=1
#P=[7.5,1*10**-10,1*10**-10]
#P=[0,3,3]
P=[]
#OP=P
coiloffset=-15./2 #Distance from each coil divided by two

#dm=2*pi
dm=15*8*2*pi    #Definitionsmængden for funktionen (rundes op)
defi=1.        #punkter pr. dm

grid_sizex=12
grid_sizey=3   #3
grid_sizez=12

max_blen=20
hue_multiplier=1./3

for tt in range(int(dm*defi)+1): #+1 da den sidste mangler
                                 #her tages 1 ad gangen, i udregningener tages 2...
    t=tt/defi
    #print t

    x=t*0.0005+15./2+debug_offset
    y=31.5/2*sin(t)
    z=31.5/2*cos(t)
    coil1.append((x,y,z))

    x=t*0.0005-15./2-debug_offset
    y=31.5/2*sin(t)
    z=31.5/2*cos(t)
    coil2.append((x,y,z))

ball = sphere (pos=(0,0,0), radius=1, color=color.red, opacity=0.5)

OP_ref_spacing=4


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

def dlxrr3(dl,r):
    return vdiv(cprod(dl,r),vlen(r)**3)

def s1s2(t1):
    
    s1=[t1*0.0005+coiloffset,31.5/2*sin(t1),31.5/2*cos(t1)]
    t2=t1+1/float(defi)
    #print t1,t2
    s2=[t2*0.0005+coiloffset,31.5/2*sin(t2),31.5/2*cos(t2)]

    #sleep(4)

    return s1,s2

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
        #print "vlen:",vlen(dl) - Tjek
        m=vdiv(vadd(s1,s2),2) #S1-S2 eller S1+S2 ???
        r=vsub(OP,m)
        #print "t",t,"s1",s1,"s2",s2,"dl",dl,"m",m,"r",r

        if debug_vectors1==1:
            if col==0:
                vectors.append(curve(color=color.red,pos=   [
                                                            (0,0,0),
                                                            (m[0],m[1],m[2]),
                                                            (r[0]+m[0],r[1]+m[1],r[2]+m[2]),
                                                            (0,0,0)
                                                            ]))
                col=1
            else:
                vectors.append(curve(color=color.green,pos=   [
                                                            (0,0,0),
                                                            (m[0],m[1],m[2]),
                                                            (r[0]+m[0],r[1]+m[1],r[2]+m[2]),
                                                            (0,0,0)
                                                            ]))
                col=0

        #a=raw_input()
        Bsum1=vadd(Bsum1,dlxrr3(dl,r))
        #sleep(4)

    coiloffset*=-1
    #Anden spole
    for tt in range(int(dm*defi)):
        t=tt/float(defi)
        s1,s2=s1s2(t)
        dl=vsub(s2,s1)
        m=vdiv(vadd(s1,s2),2)
        r=vsub(OP,m)
        if debug_vectors2==1:
            if col==0:
                vectors.append(curve(color=color.red,pos=   [
                                                            (0,0,0),
                                                            (m[0],m[1],m[2]),
                                                            (r[0]+m[0],r[1]+m[1],r[2]+m[2]),
                                                            (0,0,0)
                                                            ]))
                col=1
            else:
                vectors.append(curve(color=color.green,pos=   [
                                                            (0,0,0),
                                                            (m[0],m[1],m[2]),
                                                            (r[0]+m[0],r[1]+m[1],r[2]+m[2]),
                                                            (0,0,0)
                                                            ]))
                col=0

        Bsum2=vadd(Bsum2,dlxrr3(dl,r))
    return Bsum1,Bsum2


def Apply_contant(Bsum1,Bsum2):
    Bsum=vdiv(vadd(Bsum1,Bsum2),1/constant)
    #Bsum=vdiv(vsub(Bsum1,Bsum2),1/constant)
    Bsum1=vdiv(Bsum1,1/constant)
    Bsum2=vdiv(Bsum2,1/constant)
    return Bsum


P=[]
Bsum=[]
#rate(FPS)
time_stamp=time.time()
for xx in range(grid_sizex):
    #print str(xx+1)+"/"+str(grid_sizex),"\t",time.time()-time_stamp
    #time_stamp=time.time()
    for yy in range(grid_sizey):
        for zz in range(grid_sizez):
            P=[xx*OP_ref_spacing-((grid_sizex-1)*OP_ref_spacing)/2,yy*OP_ref_spacing-((grid_sizey-1)*OP_ref_spacing)/2,zz*OP_ref_spacing-((grid_sizez-1)*OP_ref_spacing)/2]
            n=xx+yy+zz
            #print n
            #Bsum.append()
            Bsum=vdiv(Apply_contant(*inte(P)),1./debug_vectors3_multiplier)
            Blen=vlen(Bsum)

            if strength_as_color==1:
                Blen=vlen(Bsum)
                #print (Blen*1./(max_blen/2)*hue_multiplier)
                vcolor=color.hsv_to_rgb((1./4-(Blen*1./(max_blen/2)*hue_multiplier),1,1))
                Bsum=vdiv(Bsum,Blen)
            else:
                vcolor=color.red
            if Blen<max_blen:
                curve(color=vcolor,pos=[(P[0],P[1],P[2]),(P[0]+Bsum[0],P[1]+Bsum[1],P[2]+Bsum[2])])

#if i/FPS>pi:
    #for n in range(number_of_refs):
    #    OP_ref[n].opacity=0.15
print time.time()-time_stamp
print "done"
#print scene.forward
scene.forward=(0,-1,0)

particle = sphere (pos=(20,0,-12), radius=1, color=color.green, opacity=0.4)
speed = label() # initially blank text

i=0.
auto_rotate=1
while(1):
    i+=1
    rate(FPS)
    if auto_rotate==1:
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

    


    if scene.kb.keys: # is there an event waiting to be processed?
        c = scene.kb.getkey() # obtain keyboard information
        if c=="r":
            particle.pos=(20,0,-12)
        if c=="w":
            auto_rotate=0
            scene.forward=(0,-1,0)
        if c=="s":
            auto_rotate=0
            scene.forward=(-1,0,0)
        if c=="a":
            auto_rotate=0
            scene.forward=(0,0,-1)
        if c=="d":
            if auto_rotate==0:
                auto_rotate=1
            else:
                auto_rotate=0




