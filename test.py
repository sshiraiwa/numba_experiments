import numba
from numba import types, cfunc
import numpy as np

@cfunc(types.int32(types.CPointer(types.voidptr),))
def func1(x):
    #print(x[0]
    xx = numba.carray(x[0], (1,), types.int32)
    #yy = numba.carray(x[1], (1,), np.float64)
    return xx[0]

@cfunc(types.float64(types.CPointer(types.voidptr),))
def func2(x):
    #print(x[0]
    #xx = numba.carray(x[0], (1,), types.int32)
    yy = numba.carray(x[1], (1,), np.float64)
    ##yy = numba.types.float64(x[1])
    return yy[0]


from numba_test import CallTest


obj = CallTest(func1)
print(obj.calli())
obj = CallTest(func2)
print(obj.calld())
             
