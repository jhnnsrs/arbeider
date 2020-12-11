from delt.selectors.base import BaseSelector
from delt.selectors.fields.model import ModelField
from slacko.models import SlackChannel

class SlackoSelector(BaseSelector):
    channel = ModelField(SlackChannel)

    def has_channel(self):
        return self.channel is not None