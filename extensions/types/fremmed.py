from balder.types import BalderObjectType
from fremmed.models import FrontendPod


class FrontendPodType(BalderObjectType):

    class Meta:
        model = FrontendPod