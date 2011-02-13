import logging

from pylons import app_globals, config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from ledweb.lib.base import BaseController, render

import os, os.path

from ledweb.lib.led.pattern import *
from ledweb.lib.led.beat import *

log = logging.getLogger(__name__)

class LedwebController(BaseController):

    def index(self):
        c.pattern_dir = config['pattern_dir']
        c.patterns = os.listdir(os.path.join('ledweb/public/', c.pattern_dir))
        return render('/ledweb.mako')
    
    @jsonify
    def play(self, format='html'):
        params = request.params
        if 'pattern' in params or 'beatpattern' in params:
            try:
                if 'pattern' in params:
                    pattern_name = request.params['pattern']
                    track_beat = 'beat' in params
                else:
                    pattern_name = params['beatpattern']
                    track_beat = True
                
                pattern_file = os.path.join('ledweb/public/', config['pattern_dir'],\
                                            pattern_name)
                
                p = Bemis100Pattern(pattern_file, int(config['num_boards']))
                
                if track_beat:
                    p = BeatPatternRMS(p)
                
                if 'num_times' in params:
                    n = int(params['num_times'])
                else:
                    n = -1
                
                app_globals.bemis100.add_pattern(p, n, name=pattern_name)
            
            except Exception as e:
                return dict(success=False, error=str(e))
        
        app_globals.bemis100.play()
        if format == 'json':
            return dict(success=True)
        else:
            redirect(url(controller='Ledweb', action='index'))

    @jsonify
    def queue(self):
        return dict(queue=[(p[0], p[2]) for p in app_globals.bemis100.get_queue()])
    
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
        
    
