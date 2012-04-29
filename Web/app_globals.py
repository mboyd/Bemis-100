from led.bemis100 import Bemis100
from led.ge import GEController

config = {'pattern_dir' : 'static/patterns',
          'framerate': 40,
          'num_lights': 50}

bemis100_config = {'device': '/dev/tty.usbserial-A400gmfr',
                   'num_boards': 83,
                   'framerate': 40}

bemis100 = Bemis100(**bemis100_config)
#bemis100 = GEController(device=config['device'],
#                        framerate=config['framerate'],
#                        num_lights=config['num_lights'])

# def jsonify(f):
#     def json_f(*args, **kwargs):
#         return json.dumps(f(*args, **kwargs))
#     return json_f
