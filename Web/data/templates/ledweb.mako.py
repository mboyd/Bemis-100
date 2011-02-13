from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1297568613.5678511
_template_filename='/Users/merritt/Dev/Bemis 100/Web/ledweb/templates/ledweb.mako'
_template_uri='/ledweb.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = []


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, '/base.mako', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u"\n<div id='header'>\n  <h1>Bemis 100</h1>\n</div>\n\n<div id='liveview'>\n  <canvas id='canvas' width='830' height='50'></canvas>\n  <div id='controls'>\n    <a class='pause' href='#'>Pause</a> &nbsp;&nbsp;|&nbsp;&nbsp;\n    <a class='next' href='#'>Next</a>\n  </div>\n</div>\n\n<div id='queue'>\n\t<h2>Queue</h2>\n\t<ul>\n\t</ul>\n</div>\n\n<div id='patterns'>\n\t<h2>Patterns</h2>\n\t")
        # SOURCE LINE 22
        __M_writer(h.show_patterns(c.patterns) )
        __M_writer(u'\n</div>\n\n<div id=\'upload\'>\n  <form action=\'/upload\' method=\'post\' enctype="multipart/form-data">\n    <label for=\'pattern\'>Upload a pattern</label>\n    <input type=\'file\' name=\'pattern\'>\n    <input type=\'submit\' value=\'Upload\'>\n  </form>\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


