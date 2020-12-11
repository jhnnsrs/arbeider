import json
from slacko.api.channel import post_message_to_slack
from delt.handlers.exceptions import HandlerException
from slacko.models import SlackChannel, SlackoPublisher, SlackoPublisherTemplate, SlackoSettings
from vart.serializers import HostSubscriptionMessageSerializer
from vart.subscriptions.host import HostSubscription
from vart.subscriptions.queue import QueueSubscription, QueueSubscriptionMessageSerializer
from logging import Logger
from delt.selector import Selector
from delt.models import Assignation, Node, Pod
from delt.handlers.newbase import BaseHandler
from delt.handlers.env import BaseHandlerEnvironment
from typing import Protocol
from balder.delt.enums import PodStatus
import logging
from slacko.selector import SlackoSelector

logger = logging.getLogger(__name__)

class VartProtocol(Protocol):
    pass

class SlackoHandlerEnv(BaseHandlerEnvironment[SlackoSettings, SlackoSelector]):
    settingsModel = SlackoSettings
    selectorClass = SlackoSelector


class SlackoHandler(BaseHandler):
    env = SlackoHandlerEnv("slacko")

    def provide(self, node: Node, selector: Selector) -> Pod:

        if "channel" in selector:
            channel = selector["channel"]

            template, created = SlackoPublisherTemplate.objects.get_or_create(
                channel = channel,
                node = node,
                provider = self.env.getProvider()

            )
            if created: logger.warn("Created new channel template")

            pod = SlackoPublisher.objects.create(
                template = template,
            )

            return pod

        else:
            raise HandlerException("No idea how to deal with this")


    def assign(self, assignation: Assignation) -> bool:
        
        try:
            channel: SlackChannel = assignation.pod.template.slackopublishertemplate.channel

            print(channel.channel)

            answer = post_message_to_slack(channel.channel, json.dumps(assignation.inputs), token=channel.slack_bot_token)
            print(answer)
        except Exception as e:
            logger.error(e)

        return True 