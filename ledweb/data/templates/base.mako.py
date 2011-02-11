# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1297407246.8205659
_template_filename=u'/Users/robindeits/Documents/Projects/Bemis100/Bemis-100/ledweb/ledweb/templates/base.mako'
_template_uri=u'/base.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        h = context.get('h', UNDEFINED)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!DOCTYPE html>\n<html>\n<head>\n  <title>LEDWeb Alpha</title>\n  ')
        # SOURCE LINE 5
        __M_writer(escape(h.stylesheet_link('/stylesheets/bemis100.css')))
        __M_writer(u"\n  <link href='http://fonts.googleapis.com/css?family=Droid+Sans' rel='stylesheet' type='text/css'>\n  <script src='/javascripts/bemis100_canvas.js'></script>\n</head>\n\n<body>\n  <div id='header'>\n    <h1>Bemis 100</h1>\n  </div>\n  \n  <canvas id='canvas' width='830' height='50'></canvas>\n  \n  <div id='content'>\n    ")
        # SOURCE LINE 18
        __M_writer(escape(self.body()))
        __M_writer(u'\n  </div>\n\n</body>\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


