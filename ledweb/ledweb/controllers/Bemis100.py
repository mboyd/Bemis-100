import logging

from pylons import app_globals, config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from ledweb.lib.base import BaseController, render

import os, os.path

from ledweb.lib.led.pattern import *
from ledweb.lib.led.beat import *

log = logging.getLogger(__name__)

class Bemis100Controller(BaseController):

    def index(self):
        c.pattern_dir = config['pattern_dir']
        c.patterns = os.listdir(os.path.join('ledweb/public/', c.pattern_dir))
        return render('/Bemis100.mako')
    
    @jsonify
    def play(self):
        if request.params.has_key('pattern'):
            try:
                pattern_file = os.path.join('ledweb/public/', config['pattern_dir'],\
                                            request.params['pattern'])
                p = Bemis100Pattern(pattern_file, int(config['num_boards']))
                
                if request.params.has_key('num_times'):
                    n = request.params['num_times']
                else:
                    n = -1
                
                app_globals.bemis100.add_pattern(p, n)
            
            except Exception, e:
                return dict(success=False, error=str(e))
        
        app_globals.bemis100.play()
        return dict(success=True)
        elif request.params.has_key('beatpattern'):
            try:
                pattern_file =
                os.path.join('ledweb/public/',config['pattern_dir'],\
                        request.params['beatpattern'])
                base = Bemis100Pattern(pattern_file, int(config['num_boards']))
                p = BeatPatternRMS(base)
                if request.params.has_key('num_times'):
                    n = request.params['num_times']
                else:
                    n = -1
                
                app_globals.bemis100.add_pattern(p, n)
            
            except Exception, e:
                return dict(success=False, error=str(e))
        
        app_globals.bemis100.play()
        return dict(success=True)


    
    @jsonify
    def queue(self):
        return dict(queue=[p[0] for p in app_globals.bemis100.get_queue()])
    
    @jsonify
    def status(self):
        return dict(status=app_globals.bemis100.status())
    
    @jsonify
    def pause(self):
        app_globals.bemis100.pause()
        return dict(success=True)
    
    @jsonify
    def next(self):
        app_globals.bemis100.next()
        return dict(success=True)
        
    
