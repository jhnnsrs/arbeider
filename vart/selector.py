
from delt.selectors.base import BaseSelector
from delt.selectors.fields.generic import IntField
from delt.selectors.fields.model import ModelField
from vart.models import Volunteer

class VartSelector(BaseSelector):
    theint = IntField(required=False)
    volunteer = ModelField(Volunteer, required=False)

