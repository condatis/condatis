import numpy as np
import geofiles


def genIPfromGeo(habname, sourcename, sinkname):
    hab=np.where(geofiles.file2np(habname))
    src=np.where(geofiles.file2np(sourcename))
    snk=np.where(geofiles.file2np(sinkname))
    return hab[0],hab[1],src[0],src[1],snk[0],snk[1],1,1.0
#    return hab[0],hab[1],src[0],src[1],snk[0],snk[1],np.ones(1024),1.0
