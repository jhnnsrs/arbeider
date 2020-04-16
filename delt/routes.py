
from rest_framework import routers
from delt.views import NodeViewSet, JobViewSet

router = routers.SimpleRouter()
router.register(r"nodes", NodeViewSet)
router.register(r"jobs", JobViewSet)