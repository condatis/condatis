import numpy as np
import tables
import logging

def sumax1(M,chunk=1024L,r=None):
    N=M.shape[0]
    steps=int(np.ceil(N*1.0/chunk))
    if not r:
        r=np.empty(N)
    for i in range(steps):
        start=i*chunk
        end=(i+1)*chunk
        ss=np.sum(M[start:end,:],axis=1)
        r[start:end]=ss
    return r

def sumax0(M,chunk=1024L,r=None):
    N=M.shape[1]
    steps=int(np.ceil(N*1.0/chunk))
    if not r:
        r=np.empty(N)
    for i in range(steps):
        start=i*chunk
        end=(i+1)*chunk
        ss=np.sum(M[:,start:end],axis=0)
        r[start:end]=ss
    return r

def sumax(M,chunk=1024L,axis=None,r=None):
    logging.info("Outer sum")
    if axis==0:
        return sumax0(M,chunk=chunk,r=r)
    if axis==1:
        return sumax1(M,chunk=chunk,r=r)
    return np.sum(sumax0(M,chunk=chunk,r=r))

def outersum(a,b,chunk=1024L):
    N=a.shape[0]
    steps=int(np.ceil(N*1.0/chunk))
    r=np.empty((b.shape[0],a.shape[0]))
    for i in range(steps+1):
        start=i*chunk
        end=(i+1)*chunk
        os=a+b[start:end]
        r[start:end,:]=os
    return r

def outerdiff(a,b,chunk=1024L,r=None):
    logging.info("Outer diff")
    N=a.shape[0]
    steps=int(np.ceil(N*1.0/chunk))
    if not r:
        r=np.empty((b.shape[0],a.shape[0]))
    for i in range(steps+1):
        start=i*chunk
        end=(i+1)*chunk
#        print "i: %d, start: %d, end: %d" % (i,start,end)
        logging.debug("i: %d, start: %d, end: %d",i,start,end)
        os=a-b[start:end]
        r[start:end,:]=os
    return r

def outerprod(a,b,chunk=1024L,r=None):
    logging.info("Outer product")
    N=a.shape[0]
    steps=int(np.ceil(N*1.0/chunk))
    if not r:
        r=np.empty((b.shape[0],a.shape[0]))
    for i in range(steps+1):
        start=i*chunk
        end=(i+1)*chunk
        logging.debug("i: %d, start: %d, end: %d",i,start,end)
        os=a*b[start:end]
        r[start:end,:]=os
    return r


def tod(a,b,chunk=4096):
    print "On disk"
    s=outerdiff(a,b,chunk=chunk)
    print s

    print "In memory"
    ss=a-b
    print ss

    print "Difference"
    print s-ss

    print "Sum difference"
    print np.sum(s-ss)
    

def test_outerdiff(X=10,Y=6,chunk=4094):
    a=np.arange(X)
    b=np.arange(Y)[:,np.newaxis]
    
    print "On disk"
    s=outerdiff(a,b,chunk=chunk)
    print s

    print "In memory"
    ss=a-b
    print ss

    print "Difference"
    print s-ss

    print "Sum difference"
    print np.sum(s-ss)

def test_sumax():
    a=np.arange(100)
    b=np.arange(60)[:,np.newaxis]+100
    c=a+b

    s=sumax(c,axis=0)
    print s
    ss=np.sum(c,axis=0)
    print ss
    print s-ss

    s=sumax(c,axis=1)
    print s
    ss=np.sum(c,axis=1)
    print ss
    print s-ss

    s=sumax(c)
    print s
    ss=np.sum(c)
    print s

def test_sumax1():
    a=np.arange(100)
    b=np.arange(60)[:,np.newaxis]+100
    c=a+b
    shape=(c.shape[0],)

    h5=tables.openFile('ch.h5',"w")
    cf=h5.create_array('/','c',c)
    of=h5.create_carray('/','o',tables.Float64Atom(),shape)
    s=sumax1(c,r=of)
    print "On disk"
    print s
    ss=np.sum(c,axis=1)
    print "In memory"
    print ss
    print "Difference"
    print s-ss
    return h5

