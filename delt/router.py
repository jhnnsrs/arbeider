from rest_framework import routers
from delt.views import NodeViewSet, JobViewSet, PodViewSet, ProvisionViewSet

router = routers.DefaultRouter()
router.register(r"nodes", NodeViewSet)
router.register(r"jobs", JobViewSet)
router.register(r"pods", PodViewSet)
router.register(r"provisions", ProvisionViewSet)