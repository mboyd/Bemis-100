from led.ledctl import LEDController
from led.ge import GEWriter
from led.bemis100 import Bemis100Writer

config = {'pattern_dir': 'static/patterns',
          'framerate': 30,
          'num_lights': 50}

controller = LEDController(framerate=config['framerate'])

writer_types = {'bemis100': {'class': Bemis100Writer,
                             'defaults': {'framerate': 30,
                                          'num_boards': 83}},
                'ge': {'class': GEWriter,
                       'defaults': {'framerate': 30,
                                    'num_lights': 50}}}
