import numpy as np
import matplotlib.pyplot as plt

def square(v):
    N=v.shape[0]
    return np.tile(v,N).reshape(N,N)

def diag(v):
    return np.identity(v.shape[0])*v

def outer_s_old(vx,vy):
    return square(vx)-square(vy).transpose()

def outer_s(vx,vy):
    m=np.meshgrid(vx,vy)
    return m[0]-m[1]

def xyv22d_old(x,y,size, val=1,zval=0):
    im=np.zeros([size,size])+zval
    im[x,y]=val
    return im

def xyv22d(x,y,sizex, sizey, val=1,zval=0):
    # print "In xyv22d"
    # print "sizex: %d, sizey: %d" % (sizex, sizey)
    # print "max x: %d, max y: %d" % (np.max(x), np.max(y))
    im=np.zeros([sizex,sizey])+zval
    im[x,y]=val
    return im

def xyv22d_old(x,y,sizex, val=1,zval=0):
    if sizey==0:
        sizey=sizex
    im=np.zeros([size,size])+zval
    im[x,y]=val
    return im

def dist(x,y):
    N=x.shape[0]
    xx1=np.tile(x,N).reshape(N,N)
    yy1=np.tile(y,N).reshape(N,N)

    xx=xx1-xx1.transpose()
    yy=yy1-yy1.transpose()

#    print "type of xx in dist is ", type(xx[0])
#    print "type of yy in dist is ", type(yy[0])

    return np.sqrt(xx**2 + yy**2)

def nearest_old(x,y,x0,y0):
    xd=x-x0
    yd=y-y0
    d=dist(xd,yd)
    print "d shape: ", d.shape
    print "d min: ",np.min(d)
    plt.figure(6)
    plt.imshow(d)
    sd=np.sort(d)
    
    return np.where(d==np.min(d))
    


def nearest(x,y,x0,y0):
    xd=x-x0
    yd=y-y0
    r=np.sqrt(xd**2 + yd**2)
    ir=np.where(r==min(r))
    return ir
