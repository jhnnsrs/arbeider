from balder.register import register_subscription
from balder.wrappers import NodeSubscriptionWrapper
from drawing.nodes import DrawerConfig


@register_subscription("drawer", description="Make a Request to the Drawer")
class DrawerWrapper(NodeSubscriptionWrapper):
    config = DrawerConfig
