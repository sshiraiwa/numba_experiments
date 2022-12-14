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

#setting = {"output": 2,
#           "iscomplex": (2, 2),
#           "kinds": (0, 1),
#           "sizes": (1, 2),}
           
#def c12(ptx, density, E):
#    density = density + 1
#    return ptx[1] * (density * E[0].real + 1j*density * E[0].imag)

setting = {"output": 2,
           "iscomplex": (2, ),
           "kinds": (1, ),
           "sizes": (2, ),}
def c12(ptx, density):
    ptx[0] = 0
    ptx[1] = 3
    ptx[2] = 10
    return density[0]

#setting = {"input": (),
#           "output" 2}
#def c12(ptx):
#    return ptx[1] + ptx[1]*1j

def generate_caller_text(settings):
    text = ['def c12_caller(ptx, data):']

    count = 0

    params_line = '    params = ('        
    for s in settings["input"]:
        if s == 2:
            t = '    arr'+str(count) + ' = data[' + str(count) + ']+1j*data[' + str(count) +'+1]'
            params_line += 'arr'+str(count)+','
            count = count + 2
        else:
            t = '    arr'+str(count) + ' = data[' + str(count) + ']'
            params_line += 'arr'+str(count)+','
            count = count + 1
        text.append(t)
    params_line += ')'

    text.append(params_line)
    text.append("    return (inner_func(ptx, *params))")
    return '\n'.join(text)

c12_caller = '''
def c12_caller(ptx, data):
    ptx = numba.carray(ptx, (3,), np.float64)
    arr0r = numba.carray(data[0], (1,), np.float64)
    arr0i = numba.carray(data[0], (1,), np.float64)
    arr0 = arr0r[0]+1j*arr0i[0]
    
    arr3r = numba.carray(data[0], (2,), np.float64)
    arr3i = numba.carray(data[0], (2,), np.float64)
    arr3 = arr3r + 1j*arr3i

    params = (arr3,)
    return (inner_func(ptx, *params))
'''

#c12_caller = generate_caller_text(setting)
print(c12_caller)
exec(c12_caller)

def generate_signature(setting):

    sig = ''
    if setting['output'] == 1:
        sig += 'types.float64(types.double[:], '
    else:
        sig += 'types.complex128(types.double[:], '

    for s, kind, size in zip(setting['iscomplex'], setting['kinds'], setting['sizes']):
        if s == 1:
            if kind == 0:
                sig += 'types.double,'
            else:
                sig += 'types.double[:], '
        else:
            if kind == 0:
                sig += 'types.complex128,'
            else:
                sig += 'types.complex128[:], '

    sig = sig + ")"
    return sig
        
sig = generate_signature(setting)
print(sig)
inner_func = njit(sig)(c12)


        


l = {}
g = {}
exec(f3_text)
exec(f4_text)
exec(f5_text)


func3 = cfunc(types.float64(types.CPointer(types.voidptr),))(func3)
func4 = cfunc(types.float64(types.CPointer(types.voidptr),))(func4)
func5 = cfunc(types.complex128(types.CPointer(types.voidptr),))(func5)


def _copy_func_and_apply_params(f, params):
    import copy
    import types
    import functools
  
    """Based on https://stackoverflow.com/a/13503277/2988730 (@unutbu)"""
    globals = f.__globals__.copy()
    for k in params:
       globals[k] = params[k]
    g = types.FunctionType(f.__code__, globals, name=f.__name__,
                                   argdefs=f.__defaults__, closure=f.__closure__)
    g = functools.update_wrapper(g, f)
    g.__module__ = f.__module__
    g.__kwdefaults__ = copy.copy(f.__kwdefaults__)
    return g

c12_caller = _copy_func_and_apply_params(c12_caller, {'inner_func': inner_func})

c12_caller = cfunc(types.complex128(types.CPointer(types.double), types.CPointer(types.voidptr)))(c12_caller)

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

print("here")
obj = CallTest(c12_caller)
print(obj.callptx())
                     
