%module numba_test
%{
%}
%include <complex.i>
//
%inline %{
  #include <iostream>
  #include <complex>      
  typedef int (*sample_func)(void **);

  class CallTest{
  protected:
    void *address_;
  public:
    CallTest(PyObject *input){
      PyObject *address = PyObject_GetAttrString(input, "address");
      void *ptr = PyLong_AsVoidPtr(address);
      Py_DECREF(address);
      address_ = ptr;
      return;
    }
    int calli(){
      void *data[3];

      int x = 3;
      //double y = 1.0;
      double y = 1000.;
      char z = 's';
      data[0] = &x;
      data[1] = &y;
      data[2] = &z;
      std::cout << data[0] << "\n";
      std::cout << data[1] << "\n";
      std::cout << data[2] << "\n";
      return ((int (*)(void **))address_)(data);
    }
    double calld(){
      void *data[3];

      int x = 3;
      //double y = 1.0;
      double y = 1000.;
      char z = 's';
      data[0] = &x;
      data[1] = &y;
      data[2] = &z;
      std::cout << data[0] << "\n";
      std::cout << data[1] << "\n";
      std::cout << data[2] << "\n";
      return ((double (*)(void **))address_)(data);
    }
   std::complex<double> callz(){
      void *data[3];

      int x = 3;
      //double y = 1.0;
      double y = 1000.;
      char z = 's';
      data[0] = &x;
      data[1] = &y;
      data[2] = &z;
      std::cout << data[0] << "\n";
      std::cout << data[1] << "\n";
      std::cout << data[2] << "\n";
      return ((std::complex<double> (*)(void **))address_)(data);
    }
  
 };
%}
 
