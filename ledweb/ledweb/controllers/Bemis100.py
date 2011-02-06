import logging

from pylons import app_globals, config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from ledweb.lib.base import BaseController, render

import os, os.path

from ledweb.lib.pattern import *

log = logging.getLogger(__name__)

class Bemis100Controller(BaseController):

    def index(self):
        c.pattern_dir = config['pattern_dir']
        c.patterns = os.listdir(os.path.join('ledweb/public/', c.pattern_dir))
        return render('/Bemis100.mako')
    
    @jsonify
    def play(self):
        if request.params.has_key('pattern'):
            pattern_file = os.path.join('ledweb/public/', config['pattern_dir'],\
                                        request.params['pattern'])
        else:
            return dict(success=False, error='No pattern specified')
        
        try:
            num_times = int(request.params['num_times'])
        except Exception:
            num_times = -1
        
        try:
            p = Bemis100Pattern(pattern_file, int(config['num_boards']))
            app_globals.bemis100.draw_pattern(p, num_times)
            return dict(success=True)
        except Exception, e:
            return dict(success=False, error=str(e))
    
    @jsonify
    def status(self):
        return dict(status=app_globals.bemis100.status())
    
    @jsonify
    def pause(self):
        app_globals.bemis100.pause()
        return dict(success=True)
        
    