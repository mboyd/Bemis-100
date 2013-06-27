%module swig_blink
%{
#include <wiringPi.h>
extern int blink(int x);
%}

extern int blink(int x);
