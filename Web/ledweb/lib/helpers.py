"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
from pylons import config
import os.path

# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password
from webhelpers.html.tags import stylesheet_link

def show_patterns(patterns):
    s = ''
    for e in patterns:
        if type(e) is list:
            s += show_patterns(e)
        else:
            s += show_pattern(e)
    return s

def show_pattern(p):
    s = '<a href="/play?pattern='+p+'">\n' + \
        '\t<img class="pattern" data-pattern="'+p+'" alt="pattern" ' + \
        'src="'+os.path.join(config['pattern_dir'], p)+'">\n' + \
        '</a>\n'
    return s