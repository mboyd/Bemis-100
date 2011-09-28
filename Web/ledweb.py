#!/usr/bin/env python2.6
import web

import os, os.path, shutil, sys, re

sys.path.append('..')

from app_globals import bemis100, config, jsonify

from led.bemis100 import Bemis100
from led.ge import GEController
from led.pattern import Bemis100Pattern
from led.beat import BeatPatternRMS, BeatPattern
from led.graphEq import GraphEqPattern
from led.wave import WavePattern

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
            patterns = []

            for root, dirs, files in os.walk(d):
                disp_root = os.path.relpath(root, d)
                if disp_root == '.':
                    disp_root = ''
                p = []
                for f in files:
                    if re.match('^[^\.]+\.(gif|png|jpg|jpeg|tiff|bmp)$', f, re.I):
                        p.append(os.path.join(disp_root, f))
                patterns.append((disp_root, p))
            
            patterns[:1] = patterns[0][1]    # Don't return relpath for root dir
            
            return patterns
        
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
        if 'pattern' in params or 'beatpattern' in params \
                or 'grapheqpattern' in params:
            try:
                if 'pattern' in params:
                    pattern_name = params['pattern']
                    track_beat = 'beat' in params
                    graph_eq = False
                elif 'beatpattern' in params:
                    pattern_name = params['beatpattern']
                    track_beat = True
                    graph_eq = False
                elif 'grapheqpattern' in params:
                    pattern_name = params['grapheqpattern']
                    track_beat = False
                    graph_eq = True
                
                pattern_file = os.path.join(config['pattern_dir'], pattern_name)
                
                p = Bemis100Pattern(pattern_file, config['num_boards'])
                #p = WavePattern(config['num_boards'])
                
                if track_beat:
                    p = BeatPattern(p)
                elif graph_eq:
                    p = GraphEqPattern(p)
                
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
