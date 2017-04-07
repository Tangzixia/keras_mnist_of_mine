import gzip
import cPickle
import sys
import numpy as np

def load_data(path="mnist.pkl.gz"):
    f=gzip.open(path,'rb')
    if sys.version_info<(3,):
        data=cPickle.load(f)
    else:
        data=cPickle.load(f,encoding="bytes")
    f.close()
    return data