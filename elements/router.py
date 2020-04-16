from django.utils.safestring import mark_safe
from rest_framework import routers

from elements.views import (AnimalViewSet, AntibodyViewSet,
                            ExperimentalGroupViewSet, ExperimentViewSet,
                            FileMatchStringViewSet, RepresentationViewSet,
                            RoiViewSet, SampleViewSet)


class ElementsRootView(routers.APIRootView):
    """
    Controls appearance of the API root view
    """

    def get_view_name(self) -> str:
        return "Elements"



class ElementsRouter(routers.DefaultRouter):
    APIRootView = ElementsRootView
    include_format_suffixes = False

router = ElementsRouter()
router.register(r"antibodies", AntibodyViewSet)
router.register(r"experiments", ExperimentViewSet)
router.register(r"experimentalgroups", ExperimentalGroupViewSet)
router.register(r"animals", AnimalViewSet)
router.register(r"filematchstrings", FileMatchStringViewSet) #TODO: Maybe factor this out and not accesible?

router.register(r"rois", RoiViewSet)
router.register(r"samples", SampleViewSet)
router.register(r"experiments", ExperimentViewSet)
router.register(r"representations", RepresentationViewSet)
