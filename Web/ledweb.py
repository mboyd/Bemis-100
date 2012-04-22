import tornado
import tornado.httpserver

import os, os.path, shutil, sys, re, json

sys.path.append('..')

print "Running the import"
from app_globals import bemis100, config

from led.ledctl import WebsocketWriter
from led.pattern import Bemis100Pattern
from led.beat import BeatPatternRMS, BeatPattern
from led.graphEq import GraphEqPattern
from led.wave import WavePattern
from led.new_wave import NewWavePattern


websockets = []

# g = {'config' : config, 'type' : type, 'path_join' : os.path.join}
# render = web.template.render('templates/', base='layout', globals=g)

def show_patterns(patterns):
    s = ''
    for e in patterns:
        if type(e) is tuple:
            s += '<div class="pattern_folder">' + \
                    '<h3>' + e[0] + '</h3>' + \
                    show_patterns(e[1]) + \
                  '</div>'
        else:
            s += show_pattern(e)
    return s

def show_pattern(p):
    s = '<a href="/play?pattern='+p+'">\n' + \
        '\t<img class="pattern" data-pattern="'+p+'" alt="pattern" ' + \
        'src="'+os.path.join(config['pattern_dir'],p)+'">\n' + \
        '</a>\n'
    return s

class ClientSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        bemis100.add_writer(WebsocketWriter(config['framerate'], self))
        print "WebSocket opened"

    def on_close(self):
        print "WebSocket closed"

class Home(tornado.web.RequestHandler):
    def get(self):
        
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


        patterns_html = show_patterns(patterns)
        self.render("layout.html", title="Bemis100", patterns_html=patterns_html)

class Add(tornado.web.RequestHandler):
    def get(self):
        params = self.request.arguments
        print params
        if 'pattern' in params or 'beatpattern' in params \
                or 'grapheqpattern' in params:
            try:
                if 'pattern' in params:
                    pattern_name = params['pattern'][0]
                    track_beat = 'beat' in params
                    graph_eq = 'grapheq' in params
                
                p = None
                if pattern_name.startswith("Specials"):
                    if "new_wave" in pattern_name:
                        p = NewWavePattern(num_lights = config['num_lights'])
                    elif "wave" in pattern_name:
                        p = WavePattern(num_lights = config['num_lights'])
                else:
                    pattern_path = os.path.join(config['pattern_dir'], pattern_name)
                    if os.path.exists(pattern_path):
                        p = Bemis100Pattern(pattern_path, config['num_lights'])

                if p is not None:
                    if track_beat:
                        p = BeatPattern(p)
                    elif graph_eq:
                        p = GraphEqPattern(p)
                    
                    if 'num_times' in params:
                        n = int(params['num_times'])
                    else:
                        n = -1
                    
                    bemis100.add_pattern(p, n, name=pattern_name)
                    print "Added pattern:", pattern_name
                else:
                    print "Invalid pattern name:", pattern_name
            
            except Exception as e:
                print "caught error in Play"
                self.write(json.dumps(dict(success=False, error=str(e))))
        
        # bemis100.play()
        self.write(json.dumps(dict(success=True)))
        

class Queue(tornado.web.RequestHandler):
    
    def get(self):
        current_pattern = bemis100.get_current_pattern()
        if current_pattern is not None:
            current = [current_pattern['name'],
                       current_pattern['num_times']]
        else:
            current = ['', 0]
        self.write(json.dumps(dict(queue=[(p[0], p[2]) for p in bemis100.get_queue()],
                                   current=current)))

class Status(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(dict(status=bemis100.status())))

class Pause(tornado.web.RequestHandler):
    def get(self):
        bemis100.pause()
        self.write(json.dumps(dict(success=True)))

class Play(tornado.web.RequestHandler):
    def get(self):
        bemis100.play()
        self.write(json.dumps(dict(success=True)))

class Next(tornado.web.RequestHandler):
    def get(self):
        bemis100.next()
        self.write(json.dumps(dict(success=True)))

# class Upload(tornado.web.RequestHandler):
#     def post(self):
#         try:
#             i = web.input(pattern={})
#             f = i['pattern']
#             fn = f.filename
#             if '/' in fn:
#                 fn = fn[fn.rfind('/')+1:]
                
#             base_path = config['pattern_dir']
#             path = os.path.join(base_path, fn)
            
#             new_f = open(path, 'w')
#             shutil.copyfileobj(f.file, new_f)
#             f.file.close()
#             new_f.close()
#         except Exception:
#             raise
        
#         raise web.Found('/')

if __name__ == '__main__':
    handlers = [(r'/', Home),
        (r'/play', Play),
        (r'/add', Add),
        (r'/queue', Queue),
        (r'/pause', Pause),
        (r'/next', Next),
        # (r'/upload', Upload),
            (r"/socket", ClientSocket)]
    application = tornado.web.Application(handlers=handlers, static_path='static')
    server = tornado.httpserver.HTTPServer(application)
    server.listen(5000)

    # application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
    sys.exit()

