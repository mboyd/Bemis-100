import tornado.web
import tornado.ioloop
import threading
import os
import re
import json
import platform

import sys
sys.path.append('..')
from app_globals import controller, config, writer_types
from led.pattern import Bemis100Pattern
from led.beat import BeatPatternRMS, BeatPattern
from led.graphEq import GraphEqPattern
from led.wave import WavePattern
from led.new_wave import NewWavePattern
from led.ge import GEWriter
from led.mix import MixPattern
from led.bemis100 import Bemis100Writer
from led.utils import find_patterns

if platform.system() == "Windows":
    import _winreg as winreg
    import itertools

    def list_com_ports():
        """ Uses the Win32 registry to return an
            iterator of serial (COM) ports
            existing on this computer.
        """
        path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
        except WindowsError:
            raise IterationError

        for i in itertools.count():
            try:
                val = winreg.EnumValue(key, i)
                yield str(val[1])
            except EnvironmentError:
                break
else:
    from serial.tools.list_ports import comports

    def list_com_ports():
        return sorted([i[0] for i in comports()],key=lambda x: 'usbmodem' in x, reverse=True)

def show_patterns(patterns):
    s = ''
    for e in patterns:
        if type(e) is tuple:
            s += '<div class="pattern_folder">' + \
                 '<h3>' + e[0] + \
                 '&rarr;  <span class="shuffle"><a folder="' + e[0] + '" href="/play?folder=' + e[0] + '">Shuffle</a></span></h3>' + \
                 show_patterns(e[1]) + \
                 '</div>'
        else:
            s += show_pattern(e)
    return s

def get_preview_path(pat):
    return os.path.join(config['build_dir'], 'previews', re.sub(r'\.[^.]*$', '.gif', pat))

def show_pattern(p):
    s = '<a href="/play?pattern='+p+'">\n' + \
        '\t<div class="pattern-block"> ' + \
        '\t<img class="pattern-image" data-pattern="'+p+'"' + \
        'src="'+os.path.join(config['pattern_dir'],p)+'">\n' + \
        '\t<img class="pattern-preview" data-pattern="'+p+'"' + \
        'src="'+ get_preview_path(p) +'">\n' + \
        '</div>\n' + \
        '</a>\n'
    return s

class Home(tornado.web.RequestHandler):
    def get(self):
        patterns = find_patterns(config['pattern_dir'])

        patterns_html = show_patterns(patterns)
        self.render("layout.html", title="Bemis100", patterns_html=patterns_html)

class AddPattern(tornado.web.RequestHandler):
    def get(self):
        params = self.request.arguments
        if 'pattern' in params or 'beatpattern' in params \
                or 'grapheqpattern' in params or 'folder' in params:
            p = None
            track_beat = 'beat' in params
            graph_eq = 'grapheq' in params
            if 'pattern' in params:
                pattern_name = params['pattern'][0]
                if pattern_name.startswith("Specials"):
                    if "new_wave" in pattern_name:
                        p = NewWavePattern(num_lights=config['num_lights'])
                    elif "wave" in pattern_name:
                        p = WavePattern(num_lights=config['num_lights'])
                else:
                    pattern_path = os.path.join(config['pattern_dir'], pattern_name)
                    if os.path.exists(pattern_path):
                        p = Bemis100Pattern(pattern_path, config['num_lights'])
            elif 'folder' in params:
                folder = params['folder'][0]
                pattern_path = os.path.join(config['pattern_dir'], folder)
                pattern_name = folder
                p = MixPattern(pattern_path, config['num_lights'])

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
        self.write(json.dumps(dict(success=True)))


class Queue(tornado.web.RequestHandler):

    def get(self):
        if controller.current is None:
            self.write(json.dumps(dict(queue=[], current=dict(name='',reps=0,id=-1,is_folder=False))))
        else:
            self.write(json.dumps(dict(
                       queue=[dict(name=p.name,
                                   reps=p.reps,
                                   id=p.id,
                                   is_folder=isinstance(p.pattern, MixPattern))
                              for p in controller.queue],
                       current=dict(name=controller.current.name,
                                    reps=controller.current.reps,
                                    id=controller.current.id,
                                    is_folder=isinstance(controller.current.pattern, MixPattern)))))


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
        ports = list(list_com_ports())
        print ports
        self.write(json.dumps({'writers':writers, 'ports':ports}))

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
                ]

    application = tornado.web.Application(handlers=handlers, static_path='static')

    try:
        # server = tornadio2.SocketServer(application)
        application.listen(5000)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print 'Exiting...'
        controller.quit()
        print 'controller exit'
        sys.exit()
