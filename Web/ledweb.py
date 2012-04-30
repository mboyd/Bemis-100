import tornado
import tornadio2
import tornado.httpserver

import threading
import os, os.path, shutil, sys, re, json
import serial.tools.list_ports

sys.path.append('..')

from app_globals import controller, config, writer_types

from led.ledctl import WebsocketWriter
from led.pattern import Bemis100Pattern
from led.beat import BeatPatternRMS, BeatPattern
from led.graphEq import GraphEqPattern
from led.wave import WavePattern
from led.new_wave import NewWavePattern
from led.ge import GEWriter
from led.bemis100 import Bemis100Writer


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

class ClientSocket(tornadio2.SocketConnection):
    writers = {}
    
    def on_open(self, request):
        w = WebsocketWriter(config['framerate'], self)
        self.writers[self] = w
        controller.add_writer(w)
        print "WebSocket opened"
        return True
    
    def on_message(self, message):
        print "Socket.IO message: " + message

    def on_close(self):
        print "WebSocket closed"
        controller.remove_writer(self.writers[self])
        del self.writers[self]

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

class AddPattern(tornado.web.RequestHandler):
    def get(self):
        params = self.request.arguments
        print params
        if 'pattern' in params or 'beatpattern' in params \
                or 'grapheqpattern' in params:
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
                
                controller.add_pattern(p, n, name=pattern_name)
                print "Added pattern:", pattern_name
            else:
                print "Invalid pattern name:", pattern_name
        # controller.play()
        self.write(json.dumps(dict(success=True)))
        

class Queue(tornado.web.RequestHandler):
    
    def get(self):
        current_pattern = controller.get_current_pattern()
        if current_pattern is not None:
            current = [current_pattern['name'],
                       current_pattern['num_times']]
        else:
            current = ['', 0]
        self.write(json.dumps(dict(queue=[(p[0], p[2]) for p in controller.get_queue()],
                                   current=current)))

class Status(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(dict(status=controller.status())))

class Pause(tornado.web.RequestHandler):
    def get(self):
        controller.pause()
        self.write(json.dumps(dict(success=True)))

class Play(tornado.web.RequestHandler):
    def get(self):
        controller.play()
        self.write(json.dumps(dict(success=True)))

class Next(tornado.web.RequestHandler):
    def get(self):
        controller.next()
        self.write(json.dumps(dict(success=True)))

class GetWriters(tornado.web.RequestHandler):
    def get(self):
        writer_list = []
        for writer in controller.writers:
            if not isinstance(writer, WebsocketWriter):
                writer_list.append('%s on device %s' % (writer.__class__.__name__, writer.device))
        self.write(json.dumps(writer_list))

class AddWriter(tornado.web.RequestHandler):
    def get(self):
        params = self.request.arguments
        writer_class = writer_types[params['writer_type'][0]]['class']
        writer_params = writer_types[params['writer_type'][0]]['defaults']
        device = params['port'][0]
        new_writer = writer_class(device, **writer_params)
        print "Adding writer", new_writer
        controller.add_writer(new_writer)

class DeviceList(tornado.web.RequestHandler):
    """
    List serial devices which are available for attaching hardware.
    """
    def get(self):
        writers = writer_types.keys()
        ports = [port[0] for port in serial.tools.list_ports.comports()]
        self.write(json.dumps({'writers':writers, 'ports':ports}))

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
        (r'/add', AddPattern),
        (r'/queue', Queue),
        (r'/pause', Pause),
        (r'/next', Next),
        (r'/add_writer', AddWriter),
        (r'/device_list', DeviceList),
        (r'/get_writers', GetWriters)
        # (r'/upload', Upload)
        ] + tornadio2.TornadioRouter(ClientSocket).urls
    
    application = tornado.web.Application(handlers=handlers, static_path='static', socket_io_port=5000)

    try:
        server = tornadio2.SocketServer(application)
    except KeyboardInterrupt:
        print 'Exiting...'
        controller.quit()
        print 'controller exit'
        print "active threads", threading._active
        sys.exit()


