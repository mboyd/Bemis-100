#!/usr/bin/env python2.6
import sys
sys.path.append('..')

from led import ddf
import optparse, sys, os

if __name__ == '__main__':
    p = optparse.OptionParser("Usage: python %prog module1 module2 ...")
    
    (options, args) = p.parse_args()
    
    if len(args) < 1:
        p.print_help()
        sys.exit(1)
    
    modules = []
    for m in args:
        #try:
            w = ddf.DDFWriter(0, m, 1)
            w.open_port()
            modules.append(w)
        #except Exception, e:
        #    print "Error opening module %s: %s" % (m, str(e))
    
    expert = False  # Allow evaluation of arbitrary python expressions
    
    while True:
        cmd = raw_input("ddf_debug> ")
        
        if 'red'.startswith(cmd):
            map(lambda m: m.red(), modules)
        
        elif 'green'.startswith(cmd):
            map(lambda m: m.green(), modules)
        
        elif 'blue'.startswith(cmd):
            map(lambda m: m.blue(), modules)
            
        elif 'flash'.startswith(cmd):
            for i in range(50):
                map(lambda m: m.red(), modules)
                map(lambda m: m.green(), modules)
                map(lambda m: m.blue(), modules)
        
        elif 'off'.startswith(cmd):
            map(lambda m: m.blank(), modules)
        
        elif 'quit'.startswith(cmd):
            break
        
        elif 'expert'.startswith(cmd):
            expert = True
        
        else:
            if expert:
                try:
                    print eval(cmd, globals(), locals())
                except Exception, e:
                    print e
            else:
                print "Valid commands are red, green, blue, off, and quit"
    
    map(lambda m: m.close_port(), modules)
    