"""The application's Globals object"""

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

import signal

from bemis100 import *

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self, config):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        self.cache = CacheManager(**parse_cache_config_options(config))
        
        self.bemis100 = Bemis100(config['device'], int(config['num_boards']), \
                                float(config['framerate']))
        
        signal.signal(signal.SIGTERM, self.cleanup)
                                
    def cleanup(self, signum, frame):
        print 'Caught shutdown, killing renderer'
        self.bemis100.quit()
    
