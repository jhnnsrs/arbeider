from balder.types import BalderObjectType
from earl.models import Peasent, PeasentTemplate

class PeasentType(BalderObjectType):

    class Meta:
        model = Peasent



class PeasentTemplateType(BalderObjectType):

    class Meta:
        model = PeasentTemplate
