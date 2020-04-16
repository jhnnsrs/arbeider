from rest_framework import routers
from delt.views import NodeViewSet, JobViewSet

router = routers.DefaultRouter()
router.register(r"nodes", NodeViewSet)
router.register(r"jobs", JobViewSet)