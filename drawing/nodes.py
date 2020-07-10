from konfig.backend import register_konfig_node
from drawing.configs.drawer import DrawerConfig
from drawing.configs.liner import LinerKonfig

@register_konfig_node(DrawerConfig)
class Drawer(object):
    pass

@register_konfig_node(LinerKonfig)
class Line(object):
    pass