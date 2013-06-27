all: _swig_blink.so

swig_blink_wrap.c: swig_blink.i
	swig2.0 -python swig_blink.i

swig_blink.o: swig_blink.c swig_blink_wrap.c
	gcc -c swig_blink.c swig_blink_wrap.c -I/usr/include/python2.7 -lwiringPi

swig_blink_wrap.o: swig_blink.c swig_blink_wrap.c
	gcc -c swig_blink.c swig_blink_wrap.c -I/usr/include/python2.7 -lwiringPi

_swig_blink.so: swig_blink.o swig_blink_wrap.o
	ld -shared swig_blink.o swig_blink_wrap.o -o _swig_blink.so -lwiringPi