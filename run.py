#!/usr/bin/env python2.6
from __future__ import division

from led import bemis100, pattern, ledctl, ge, spectrogram, beat, wave, new_wave
import optparse, sys, os

if __name__ == '__main__':
    p = optparse.OptionParser("Usage: python %prog [pattern | pattern_dir | wave] [options]")
    
    p.add_option('-n', type="int", action='store', dest='num_boards', 
                    default='83', help='Number of boards (default 83)')
    
    p.add_option('-d', action="store", dest="device", default="", 
                    help="Device path")
    
    p.add_option('-f', type='int', action='store', dest='framerate', 
                    default='30', help='Framerate (Hz, default 30)')
                    
    p.add_option('-r', action='store_true', dest='repeat', default=False,
                    help="Repeat pattern[s] forever")
    
    p.add_option('-c', type='int', action='store', dest='count',
                    default='-1', 
                    help='Repetition count (exit when done, default is to loop forever)')
    
    p.add_option('-s','--sim', action='store_true', dest='sim',default=False,
                    help='Simulate the Bemis100 only')

    p.add_option('-b','--beat', action='store_true', dest='beat',default=False,
            help='Beat pattern')

    p.add_option('-w','--wave', action='store_true',dest='wave',default=False,
                 help='Wave beat pattern')

    p.add_option('-g', '--gelights', action='store_true', dest='ge', default=False,
            help="Use GE ColorEffects lights instead of Bemis100")
    
    (options, args) = p.parse_args()

    
    if len(args) < 1:
        p.print_help()
        sys.exit(1)    
    
    print "Opening port...",

    if not options.sim:
        if options.device == '':
            devices = filter(os.path.exists, ['/dev/tty.usbserial', '/dev/ttyUSB0', '/dev/tty.usbmodemfd141'])
            if len(devices) > 0:
                options.device = devices[0]
        if options.ge:
            print "GE Lights selected"
            b = ge.GEController(options.device, num_boards=options.num_boards, framerate=options.framerate)
        else:
            b = bemis100.Bemis100(options.device, num_boards=options.num_boards, framerate=options.framerate)
    else:
        b = ledctl.LEDController(options.num_boards, options.framerate)
        
    print "done\nLoading patterns...",

        
    patterns = []

    for fn in args:
        if os.path.isfile(fn):
            if options.beat:
                new_pattern = beat.BeatPattern(pattern.Bemis100Pattern(fn,
                    options.num_boards))
            else:
                new_pattern = pattern.Bemis100Pattern(fn,options.num_boards)
            patterns.append(new_pattern)
        elif os.path.isdir(fn):
            names = [os.path.join(fn, f) for f in os.listdir(fn)]
            patterns.extend([pattern.Bemis100Pattern(f, options.num_boards) for f in names])
        elif fn == 'wave':
            patterns.append(wave.WavePattern(num_boards = options.num_boards))
        elif fn == 'new_wave':
            patterns.append(new_wave.NewWavePattern(num_boards = options.num_boards))
        else:
            print "Not a pattern file or directory: %s\n\n" % fn 
    
    print "done\nPlaying...",
    sys.stdout.flush()
    
    b.play()
    
    while True:
        for p in patterns:
            try:
                b.add_pattern(p, num_times=options.count, async=True)
                print "added pattern"
            except (KeyboardInterrupt, SystemExit):
                options.repeat = False
                break
            
        if not options.repeat:
            break
    
    b.quit()
    print 'done'
