%module swig_blink
%{
#include <wiringPi.h>
extern int blink(int x);
extern int set_color(int led, int intensity, int r, int g, int b);
extern int fill_color(int begin, int count, int intensity, int r, int g, int b);
%}

extern int blink(int x);
extern int set_color(int led, int intensity, int r, int g, int b);
extern int fill_color(int begin, int count, int intensity, int r, int g, int b);
