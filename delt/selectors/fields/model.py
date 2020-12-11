from delt.selectors.fields.base import FieldMixin
from rest_framework.relations import PrimaryKeyRelatedField
from delt.widgets.widgets.model import ModelWidget


class ModelFieldMixin(FieldMixin):

    def __init__(self, model, querybuilder= lambda x: x.objects.all(), **kwargs) -> None:
        self.portidentifer = model.__name__
        super().__init__(queryset=querybuilder(model),**kwargs)


    
    def params(self, key, depth=0):
        return {
            "identifier": self.portidentifer
        }

    @classmethod
    def paramTypes(cls):
        return {
            "identifier": str
        }



class ModelField(ModelFieldMixin, PrimaryKeyRelatedField):
    type= "model"
    widget = ModelWidget()
    description="This is a Model Port"