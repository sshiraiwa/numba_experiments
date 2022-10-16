swig -Wall -c++ -python -fastproxy -olddefs -keyword numba_test.i
python setup.py install
python test.py
