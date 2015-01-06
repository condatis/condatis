#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

def point(x,y):
    return np.array([x]),np.array([y])    

def circle(x,y,r):
    twopi=2.0*np.pi
    xx=[]
    yy=[]

    for i in np.arange(r):
        xx.append(x)
        yy.append(y+i)
        xx.append(x)
        yy.append(y-i)

    for j in np.arange(r)+1:
        Ni=int(np.sqrt(r**2-j**2))
        for i in np.arange(Ni):
            xx.append(x-j)
            yy.append(y-i)
            xx.append(x-j)
            yy.append(y+i)

            xx.append(x+j)
            yy.append(y-i)
            xx.append(x+j)
            yy.append(y+i)
    return np.array(xx),np.array(yy)

def star(x,y,r,N):
    xx=[]
    yy=[]
    sc=np.sin(45/360.0*2*np.pi)
    for i in np.arange(N)*r/N:
        xx.append(x)
        yy.append(y+i)
        xx.append(x)
        yy.append(y-i)

        xx.append(x+i)
        yy.append(y)
        xx.append(x-i)
        yy.append(y)

        ii=i*sc
        xx.append(x+ii)
        yy.append(y+ii)
        xx.append(x+ii)
        yy.append(y-ii)

        xx.append(x-ii)
        yy.append(y-ii)
        xx.append(x-ii)
        yy.append(y+ii)
    return np.array(xx),np.array(yy)

def uniformSquare(x,y,r,N):
    xx=np.random.random_integers(-r,r,N)
    yy=np.random.random_integers(-r,r,N)
    return x+xx,y+yy

def uniform(x,y,r,N):
    x,y=circle(x,y,r)
    i=np.random.random_integers(0,x.size,N)
    xx=x[i]
    yy=y[i]
    return xx.astype(int),yy.astype(int)

def normal(x,y,r,N):
    xx=np.random.normal(x,r,N)
    yy=np.random.normal(x,r,N)
    return xx.astype(int),yy.astype(int)

def testpat(r):
    a=np.zeros((100,100))
    x,y=point(10,12)
    a[x,y]=.8
    x,y=circle(70,70,r)
    a[x,y]=.7

    x,y=star(30,70,r,5)
    a[x,y]=.5

    x,y=uniform(25,25,r,40)
    a[x,y]=.95

    x,y=normal(60,60,r,4000)
    a[x,y]=.2

    plt.clf()
    plt.imshow(a)
