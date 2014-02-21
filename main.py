# -*- coding: utf-8 -*-

from visual import *
from math import *
from time import time
from time import sleep

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

debug_vectors1=0
debug_vectors2=0
debug_vectors3=0
debug_vectors3_multiplier=10**6
#
#   Settings - End
#
#######################################

# Building scenes
scene = display(title='Helmholtz coin',width=Width, height=Height)
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

number_of_refs=5


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
OP_ref=[]
for n in range(number_of_refs):
    OP_ref.append(sphere (pos=(0,0,0), radius=.3, color=color.green, opacity=0.5))

OP_ref_spacing=5


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
    Bsum1=vdiv(Bsum1,1/constant)
    Bsum2=vdiv(Bsum2,1/constant)
    return Bsum


#Apply_contant(inte(P))
#MULTIPLY CONSTANTS!!!!


#print Bsum1
#print Bsum2,"\n"
#print Bsum


'''Bsum1=vdiv(Bsum1,1./debug_vectors3_multiplier)
Bsum2=vdiv(Bsum2,1./debug_vectors3_multiplier)
Bsum=vdiv(Bsum,1./debug_vectors3_multiplier)

if debug_vectors3==1:
    vec1=curve(color=color.yellow,pos=[(OP[0],OP[1],OP[2]),(OP[0]+Bsum1[0],OP[1]+Bsum1[1],OP[2]+Bsum1[2])])
    vec2=curve(color=color.green,pos=[(OP[0],OP[1],OP[2]),(OP[0]+Bsum2[0],OP[1]+Bsum2[1],OP[2]+Bsum2[2])])
    vec3=curve(color=color.red,pos=[(OP[0],OP[1],OP[2]),(OP[0]+Bsum[0],OP[1]+Bsum[1],OP[2]+Bsum[2])])
'''

i=0.
while 1:
    i+=1
    #OP=[0,2*cos(i/FPS),coiloffset*2*sin(i/FPS)]
    P=[]
    Bsum=[]
    rate(FPS)
    for n in range(number_of_refs):
        P.append([OP_ref_spacing*n-OP_ref_spacing*number_of_refs+20,5,coiloffset*4*cos((i)/FPS)])

        Bsum.append(Apply_contant(*inte(P[n])))
        Bsum[n]=vdiv(Bsum[n],1./debug_vectors3_multiplier)

        OP_ref[n].pos=(P[n][0],P[n][1],P[n][2])

        curve(color=color.red,pos=[(P[n][0],P[n][1],P[n][2]),(P[n][0]+Bsum[n][0],P[n][1]+Bsum[n][1],P[n][2]+Bsum[n][2])])


    if i/FPS>pi:
        for n in range(number_of_refs):
            OP_ref[n].opacity=0.15
        break





