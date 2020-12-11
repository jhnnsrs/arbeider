from rest_framework import routers
from delt.views import NodeViewSet,PodViewSet, ProvisionViewSet

router = routers.DefaultRouter()
router.register(r"nodes", NodeViewSet)
router.register(r"pods", PodViewSet)
router.register(r"provisions", ProvisionViewSet)