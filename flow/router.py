
from rest_framework import routers

from flow.views import GraphViewSet

router = routers.DefaultRouter()
router.register(r"graphs", GraphViewSet)