import sys, json
sys.path.append('..')

from led.bemis100 import Bemis100
from led.ge import GEController

config = {'pattern_dir' : 'static/patterns',
            'device' : 'sim',
            'num_boards' : 25,
            'framerate' : 30}
# 
# bemis100 = Bemis100('/dev/tty.usbserial', num_boards=83, \
#     framerate=30)

bemis100 = GEController('/dev/tty.usbmodemfd141', num_boards = 25, framerate=30)

def jsonify(f):
    def json_f(*args, **kwargs):
        return json.dumps(f(*args, **kwargs))
    return json_f
