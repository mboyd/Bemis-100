# import sys, json
# sys.path.append('..')

from led.bemis100 import Bemis100
from led.ge import GEController

config = {'pattern_dir' : 'static/patterns',
               # 'device' : 'sim',
               'device' : '/dev/tty.usbmodemfa131',
               # 'device' : '/dev/tty.usbmodemfd121',
               # 'device': 'COM5',
           'num_lights' : 50,
            'framerate' : 40 }

# bemis100 = Bemis100(config['device'], num_boards=83, \
#         framerate=config['framerate'])
print "creating controller"
bemis100 = GEController(device=config['device'],
                        framerate=config['framerate'],
                        num_lights=config['num_lights'])
print "made controller"

# def jsonify(f):
#     def json_f(*args, **kwargs):
#         return json.dumps(f(*args, **kwargs))
#     return json_f
