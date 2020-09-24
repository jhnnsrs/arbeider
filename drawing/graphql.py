from drawing.nodes import DrawerConfig


#@register_subscription("drawer", description="Make a Request to the Drawer")
class DrawerWrapper(object):
    config = DrawerConfig
