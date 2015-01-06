#import conductance as cnd
import geoimport
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import dwwspatial as sp

def load(name='l_m_1.tif'):
    return geoimport.genIPfromGeo(name,'source.tif','sink.tif')

# def calcV(ip,dispersal=4.0, R=100.0):
#     s  = cnd.ipvSolve(cnd.ipv(ip,dispersal,R))
#     return s
    
def grabLscape(V0, vs, n):
    print "Grabbing landscape: Lower, %7.4f | Upper, %7.4f" % (vs[n], vs[n+1])
    ind=np.where((V0 >= vs[n]) & (V0  < vs[n+1]))
    return ind

def plotSortVoltage(sV0):
    plt.ylabel("Voltage / V")
    plt.xlabel("Habitat cell (sorted)")
    plt.title('Sorted node Voltages')
    plt.plot(sV0,'black')


def plotColPatches(V0,vs,x,y):
    ls=np.zeros([265,265])
    cols=['white','black', 'DarkRed',
          'OliveDrab', 'DodgerBlue', 
          'GoldenRod','PowderBlue',
          'DarkSlateBlue','red','DarkGray']
    for i in range(7+1):
        inds=grabLscape(V0,vs,i)
        meanV=np.mean(V0[inds])
        print "%3d %6d %7.5f %7.5f %7.5f %s" % (i+1, inds[0].size, 
                                                vs[i], vs[i+1],meanV,cols[i+1])
        ls+=sp.xyv22d(x[inds],y[inds],265)*(i+1)

    cmap = mpl.colors.ListedColormap(cols)
    bounds=range(11)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    img = plt.imshow(ls, interpolation='nearest', 
        cmap=cmap, norm=norm)
    plt.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=bounds)


def plotVPatches(V0,vs,x,y):
    ls=np.zeros([265,265])
    for i in range(7+1):
        inds=grabLscape(V0,vs,i)
        meanV=np.mean(V0[inds])
        ls+=sp.xyv22d(x[inds],y[inds],265)*meanV

    my_cmap = plt.cm.get_cmap('Paired')
    my_cmap.set_under('w')
    plt.imshow(ls,vmin=1e-50,vmax=1, cmap=my_cmap)
    plt.colorbar()

def splitLevels(V0,N=7):
    sV0=np.sort(V0)   # Sorted voltages
    dsV0=np.diff(sV0) # Differences in sortd voltages
    tdsV0=np.argsort(dsV0)[-N:] # Top N differences

    #Voltages (lower) for each layer
    qsV0=np.sort(sV0[tdsV0])
    vs=np.zeros(N+2)
    vs[N+1]=1.2
    vs[0]=-.2
    vs[1:N+1]=qsV0
    return vs


def colourN(name='l_m_1.tif',dispersal=4.0, R=100.0):
    N=7
    ip=load(name=name)
    s=calcV(ip,dispersal,R)
    V0,I0,M0,I,x,y,Iij=s

    vs=splitLevels(V0,N)
    
    plt.figure(0)
    plt.clf()
    plotSortVoltage(np.sort(V0))

    plt.figure(1)
    plt.clf()
    plotColPatches(V0,vs,x,y)

    plt.figure(2)
    plt.clf()
    plotVPatches(V0,vs,x,y)

def rect(v,N):
    M=v.shape[0]
    return np.tile(v,N).reshape(N,M)

def closest_new(la1,la2,x,y):
    xd=x[la1]-x[la2][:,np.newaxis]
    yd=y[la1]-y[la2][:,np.newaxis]
    r=np.sqrt(xd**2 + yd**2)
    mn=np.where(r==np.min(r))
    return xx1,yy1,xx2,yy2


def closestComb(la1,la2,x,y):
    print ">Making m1"
    m1=rect(la1,la2.shape[0])
    print ">Making m2"
    m2=np.transpose(rect(la2,la1.shape[0]))

    print ">Making x1,x2,y1,y2"
    x1=x[m1]
    y1=y[m1]
    x2=x[m2]
    y2=y[m2]
    print ">making r"    
    r=np.sqrt((x1-x2)**2 + (y1-y2)**2)
    print ">Doing where"
    mn=np.where(r==np.min(r))
    print ">Assigning"
    xx1=x1[mn[0],mn[1]][0]
    xx2=x2[mn[0],mn[1]][0]
    yy1=y1[mn[0],mn[1]][0]
    yy2=y2[mn[0],mn[1]][0]

    xx1m=m1[mn[0],mn[1]]
    xx2m=m2[mn[0],mn[1]]

    print ">returning"
    return xx1,yy1,xx2,yy2,xx1m,xx2m

def closest(la1,la2,x,y):
    print ">Making m1"
    m1=rect(la1,la2.shape[0])
    print ">Making m2"
    m2=np.transpose(rect(la2,la1.shape[0]))

    print ">Making x1,x2,y1,y2"
    x1=x[m1]
    y1=y[m1]
    x2=x[m2]
    y2=y[m2]
    print ">making r"    
    r=np.sqrt((x1-x2)**2 + (y1-y2)**2)
    print ">Doing where"
    mn=np.where(r==np.min(r))
    print ">Assigning"
    xx1=x1[mn[0],mn[1]][0]
    xx2=x2[mn[0],mn[1]][0]
    yy1=y1[mn[0],mn[1]][0]
    yy2=y2[mn[0],mn[1]][0]

    print ">returning"
    return xx1,yy1,xx2,yy2

def closestInd(la1,la2,x,y):
    # Can I use meshgrid for this?
#    print ">Making m1"
    m1=rect(la1,la2.shape[0])
#    print ">Making m2"
    m2=np.transpose(rect(la2,la1.shape[0]))

#    print ">Making x1,x2,y1,y2"
    x1=x[m1]
    y1=y[m1]
    x2=x[m2]
    y2=y[m2]
#    print ">making r"
    r=np.sqrt((x1-x2)**2 + (y1-y2)**2)
#    expr=tables.Expr('sqrt(xx**2+yy**2)')

#    print ">Doing where"
    mn=np.where(r==np.min(r))
#    print ">Assigning"
    xx1=m1[mn[0],mn[1]]
    xx2=m2[mn[0],mn[1]]
    yy1=m1[mn[0],mn[1]]
    yy2=m2[mn[0],mn[1]]
#    print ">returning"
    return xx1,xx2
    
def closest_(la1,la2,x,y):
    print ">Making m1"
    m1=rect(la1,la2.shape[0])
    print ">Making m2"
    m2=np.transpose(rect(la2,la1.shape[0]))

    print ">Making x1,x2,y1,y2"
    x1=x[m1]
    y1=y[m1]
    x2=x[m2]
    y2=y[m2]
    xx=x1-x2
    yy=y1-y2
    print ">making r"
    
    r=np.sqrt(xx**2 + yy**2)
    print ">Doing where"
    mn=np.where(r==np.min(r))
    print ">Assigning"
    xx1=x1[mn[0],mn[1]][0]
    xx2=x2[mn[0],mn[1]][0]
    yy1=y1[mn[0],mn[1]][0]
    yy2=y2[mn[0],mn[1]][0]

    print ">returning"
    return xx1,yy1,xx2,yy2


def closest_(la1,la2,x,y):
    m1=rect(la1,la2.shape[0])
    m2=np.transpose(rect(la2,la1.shape[0]))

    x1=x[m1]
    y1=y[m1]
    x2=x[m2]
    y2=y[m2]
    xx=x1-x2
    yy=y1-y2
    r=np.sqrt(xx**2 + yy**2)

    mn=np.where(r==np.min(r))

    xx1=x1[mn[0],mn[1]][0]
    xx2=x2[mn[0],mn[1]][0]
    yy1=y1[mn[0],mn[1]][0]
    yy2=y2[mn[0],mn[1]][0]

    return xx1,yy1,xx2,yy2

def getClosest(L1,L2,s):
    V0,I0,M0,I,x,y,Iij=s
    vs=splitLevels(V0,N)
    la1=grabLscape(V0,vs,L1)[0]
    la2=grabLscape(V0,vs,L2)[0]
    return closest(la1,la2,s)

def tstclosest(i1,i2,name='l_m_1.tif',dispersal=4.0, R=100.0):
    N=7
    ip=load(name=name)
    s=calcV(ip,dispersal,R)
    V0,I0,M0,I,x,y,Iij=s

    vs=splitLevels(V0,N)
    la1=grabLscape(V0,vs,i1)[0]
    la2=grabLscape(V0,vs,i2)[0]

    xx1,yy1,xx2,yy2=getClosest(la1,la2,s)

    plt.figure(2)
    plt.clf()
    plt.plot(y[la1],x[la1],'ro')
    plt.plot(y[la2],x[la2],'bo')
    plt.axis((0,265,265,0))

    plt.plot(yy1,xx1,'co')
    plt.plot(yy2,xx2,'yo')
