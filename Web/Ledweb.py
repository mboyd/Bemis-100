#!/usr/bin/env python2.6
import web

import os, os.path, shutil, sys, re

sys.path.append('..')

from app_globals import bemis100, config, jsonify

from led.bemis100 import Bemis100
from led.pattern import Bemis100Pattern
from led.beat import BeatPatternRMS, BeatPattern

urls = ('/', 'Home',
        '/play', 'Play',
        '/queue', 'Queue',
        '/pause', 'Pause',
        '/next', 'Next',
        '/upload', 'Upload')

g = {'config' : config, 'type' : type, 'path_join' : os.path.join}
render = web.template.render('templates/', base='layout', globals=g)

class Home(object):

    def GET(self):
        
        def find_patterns(d):
            l = os.listdir(d)
            files = []
            dirs = []
            for e in l:
                if os.path.isfile(os.path.join(d, e)):
                    if re.match('^[^\.]+\.(gif|png|jpg|jpeg)$', e):
                        files.append(e)
                else:
                    dirs.append(e)
            
            if len(dirs) == 0:
                return files
            else:
                return files.extend([find_patterns(os.path.join(d, sd)) for sd in dirs])
        
        patterns = find_patterns(config['pattern_dir'])
        return render.home(patterns)

class Play:
    @jsonify
    def GET(self):
        if re.match('application/json|text/javascript', web.ctx.environ['HTTP_ACCEPT']):
            format_json = True
        else:
            format_json = False
        
        params = web.input()
        if 'pattern' in params or 'beatpattern' in params:
            try:
                if 'pattern' in params:
                    pattern_name = params['pattern']
                    track_beat = 'beat' in params
                else:
                    pattern_name = params['beatpattern']
                    track_beat = True
                
                pattern_file = os.path.join(config['pattern_dir'], pattern_name)
                
                p = Bemis100Pattern(pattern_file, config['num_boards'])
                
                if track_beat:
                    p = BeatPattern(p)
                
                if 'num_times' in params:
                    n = int(params['num_times'])
                else:
                    n = -1
                
                bemis100.add_pattern(p, n, name=pattern_name)
            
            except Exception as e:
                return dict(success=False, error=str(e))
        
        bemis100.play()
        
        if format_json:
            return dict(success=True)
        else:
            raise web.Found('/')

class Queue(object):
    @jsonify
    def GET(self):
        return dict(queue=[(p[0], p[2]) for p in bemis100.get_queue()])

class Status(object):
    @jsonify
    def GET(self):
        return dict(status=bemis100.status())

class Pause(object):
    @jsonify
    def GET(self):
        bemis100.pause()
        return dict(success=True)

class Next(object):
    @jsonify
    def GET(self):
        bemis100.next()
        return dict(success=True)

class Upload(object):
    def POST(self):
        try:
            i = web.input(pattern={})
            f = i['pattern']
            fn = f.filename
            if '/' in fn:
                fn = fn[fn.rfind('/')+1:]
                
            base_path = config['pattern_dir']
            path = os.path.join(base_path, fn)
            
            new_f = open(path, 'w')
            shutil.copyfileobj(f.file, new_f)
            f.file.close()
            new_f.close()
        except Exception:
            raise
        
        raise web.Found('/')

if __name__ == '__main__':
    sys.argv.append('5000')     # Set port
    app = web.application(urls, globals())
    app.run()
