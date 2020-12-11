from delt.selectors.base import BaseSelector
from delt.selectors.fields.generic import IntField


class PortSelector(BaseSelector):
    theint = IntField()
