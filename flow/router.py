
from rest_framework import routers

from flow.views import FlowViewSet, GraphViewSet

router = routers.DefaultRouter()
router.register(r"flows", FlowViewSet)
router.register(r"graphs", GraphViewSet)