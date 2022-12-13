import numba
from numba import types, cfunc, njit
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

@njit(types.float64(types.int32, types.float64))
def inner(x, y):
    return x*y
@njit(types.complex128(types.complex128))
def inner_c(xy):
    return xy**2

f3_text = '''
def func3(x):
    xx = numba.carray(x[0], (1,), np.int32)
    yy = numba.carray(x[1], (1,), np.float64)
    return inner(xx[0], yy[0])
'''


f4_text = '''
def func4(x):
    xx = numba.carray(x[0], (1,), np.int32)
    yy = numba.carray(x[1], (1,), np.float64)

    input = xx[0] + 1j*yy[0]
    ret = inner_c(input)

    return ret.real
'''

f5_text = '''
def func5(x):
    xx = numba.carray(x[0], (1,), np.int32)
    yy = numba.carray(x[1], (1,), np.float64)

    input = xx[0] + 1j*yy[0]
    return inner_c(input)
'''


l = {}
g = {}
exec(f3_text)
exec(f4_text)
exec(f5_text)

func3 = cfunc(types.float64(types.CPointer(types.voidptr),))(func3)
func4 = cfunc(types.float64(types.CPointer(types.voidptr),))(func4)
func5 = cfunc(types.complex128(types.CPointer(types.voidptr),))(func5)


from numba_test import CallTest


obj = CallTest(func1)
print(obj.calli())
obj = CallTest(func2)
print(obj.calld())
obj = CallTest(func3)
print(obj.calld())             
obj = CallTest(func4)
print(obj.calld())
obj = CallTest(func5)
print(obj.callz())

print((3 + 1j*1000)**2)
