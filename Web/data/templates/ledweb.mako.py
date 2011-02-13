from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1297560901.0672629
_template_filename='/Users/merritt/Dev/Bemis 100/ledweb/ledweb/templates/ledweb.mako'
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
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u"\n\n<div id='queue'>\n\t<h2>Queue</h2>\n\t<ul>\n\t</ul>\n</div>\n\n<div id='patterns'>\n\t<h2>Patterns</h2>\n")
        # SOURCE LINE 11
        for p in c.patterns:
            # SOURCE LINE 12
            __M_writer(u"\t  <a href='/play?pattern=")
            __M_writer(escape(p))
            __M_writer(u"'>\n\t\t<img class='pattern' data-pattern='")
            # SOURCE LINE 13
            __M_writer(escape(p))
            __M_writer(u"' alt='pattern' src='")
            __M_writer(escape(c.pattern_dir))
            __M_writer(u'/')
            __M_writer(escape(p))
            __M_writer(u"'>\n\t\t</a>\n")
        # SOURCE LINE 16
        __M_writer(u'</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


