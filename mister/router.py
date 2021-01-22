from rest_framework import routers
from mister.views import *

class MisterRootView(routers.APIRootView):
    """
    Controls appearance of the API root view
    """

    def get_view_name(self) -> str:
        return "mister"



class MisterRouter(routers.DefaultRouter):
    APIRootView = MisterRootView
    include_format_suffixes = False


misterrouter = MisterRouter()
misterrouter.register("user", UserPathViewSet, basename="userpath")
misterrouter.register("vhost", VHostPathViewSet, basename="vhostpath")
misterrouter.register("resource", ResourcePathViewSet, basename="resourcepath")
misterrouter.register("topic", TopicPathViewSet, basename="topicpath")