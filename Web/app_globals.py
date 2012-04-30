from led.ledctl import LEDController
from led.ge import GEWriter
from led.bemis100 import Bemis100Writer

config = {'pattern_dir' : 'static/patterns',
          'framerate': 30,
          'num_lights': 50}

controller = LEDController(framerate=config['framerate'])
# ge_writer = GEWriter(device='/dev/tty.usbmodemfa1331',
#                      framerate=config['framerate'])
# controller.add_writer(ge_writer)
# bemis100_writer = Bemis100Writer(device='/dev/tty.usbserial-A400gmfr',
#                                  num_boards=83,
#                                  framerate=config['framerate'])
# controller.add_writer(bemis100_writer)

writer_types = {'bemis100': {'class': Bemis100Writer,
                             'defaults': {'framerate': 30,
                                          'num_boards': 83}},
                'ge': {'class': GEWriter,
                       'defaults': {'framerate': 30,
                                    'num_lights': 50}}}

