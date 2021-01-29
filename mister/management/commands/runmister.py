from earl.models import PeasentPod
from balder.subscriptions.assignation.assign import AssignSubscription
from delt.messages.assignation import AssignationMessage
import re
from delt.messages.assignation_request import AssignationRequestMessage
from typing import Generic, Optional, TypeVar

from oauth2_provider.models import AccessToken
from delt.registries.handler import get_handler_registry
from delt.registries.additionals import get_additionals_registry
from delt.orchestrator import get_orchestrator
import logging
import asyncio
from channels import DEFAULT_CHANNEL_LAYER
from channels.layers import get_channel_layer
from channels.routing import get_default_application
from channels.worker import Worker
from django.core.management import BaseCommand, CommandError
import aiormq
from delt.discover import autodiscover_pods
from delt.handlers.channels import ChannelHandler
import json
from delt.models import Assignation, Pod
from asgiref.sync import sync_to_async
from mister.utils import assignationRequestWrapper, assignationWrapper
logger = logging.getLogger(__name__)
from pydantic import BaseModel



@sync_to_async
def create_assignation_from_request(request: AssignationRequestMessage):

    try:
        return Assignation.objects.get(reference=request.data.reference)
    except Assignation.DoesNotExist:

    
        auth = AccessToken.objects.get(token=request.meta.auth.token)
        #TODO: check for scopes


        # We are dealing with a Backend Application
        user = auth.user if auth.user else auth.application.user
        
        assignation = Assignation.objects.create(**{
            "inputs": request.data.inputs,
            "node_id": request.data.node,
            "pod_id":request.data.pod,
            "template_id": request.data.template,
            "creator": user,
            "callback": request.data.callback,
            "progress": request.data.progress,
            "reference": request.data.reference
        }
        )
        print(assignation)

        return assignation



@sync_to_async
def find_templates_for_assignation(assignation):
    assert assignation, "Please first create an Assignation"
    templates = [ template for template in assignation.node.templates.all() ]
    return templates


@sync_to_async
def find_pod_channels_for_assignation(assignation: AssignationMessage):
    assert assignation, "Please first create an Assignation"
    channels = [pod.channel for pod in PeasentPod.objects.filter(template__node_id=assignation.data.node) ]
    return channels




class RabbitMyFriend():

    def __init__(self) -> None:
        pass

    async def connect(self):
        # Perform connection
        self.connection = await aiormq.connect(f"amqp://guest:guest@mister/")
        self.channel = await self.connection.channel()


        self.assignation_request_in = await self.channel.queue_declare('assignation_request')

        # This queue gets called from the HTTP backend (so GraphQL Postman request) with an already created Assignation
        self.assignation_in = await self.channel.queue_declare("assignation_in")


        # We will get Results here
        self.assignation_done = await self.channel.queue_declare("assignation_done")

        # Start listening the queue with name 'hello'
        await self.channel.basic_consume(self.assignation_request_in.queue, self.on_assignation_request_in)
        await self.channel.basic_consume(self.assignation_done.queue, self.on_assignation_done)
        await self.channel.basic_consume(self.assignation_in.queue, self.on_assignation_in)

    @assignationWrapper.unwrapped()
    async def on_assignation_in(self, assignation: AssignationMessage, message: aiormq.types.DeliveredMessage):
        logger.info(f"Received Assignation {str(message.body.decode())}")


        channels = await find_pod_channels_for_assignation(assignation)
        # We are routing it to Pod One / This Pod will then reply to
        logger.info("Found the Following Pods we can assign too!")
        logger.error(channels)
        if len(channels) >= 1:
            await message.channel.basic_publish(
                message.body, routing_key=channels[0], # Lets take the first best one
                properties=aiormq.spec.Basic.Properties(
                    correlation_id=assignation.data.reference,
                    reply_to=self.assignation_done.queue
                )
            )

        # This should then expand this to an assignation message that can be delivered to the Providers
        await message.channel.basic_ack(message.delivery.delivery_tag)


    @assignationWrapper.unwrapped()
    async def on_assignation_done(self, assignation: AssignationMessage, message: aiormq.types.DeliveredMessage):
        logger.info(f"Assignation Done {str(message.body.decode())}")


        if assignation.data.callback == "gateway_done":
            await AssignSubscription.broadcast_async(group=f"assign_{assignation.data.reference}", payload=assignation.dict())


        # We are routing it to Pod One / This Pod will then reply to
        await message.channel.basic_publish(
            message.body, routing_key=assignation.data.callback,
            properties=aiormq.spec.Basic.Properties(
                correlation_id=assignation.data.reference,
            )
        )

        # This should then expand this to an assignation message that can be delivered to the Providers
        await message.channel.basic_ack(message.delivery.delivery_tag)



    @assignationRequestWrapper.unwrapped()
    async def on_assignation_request_in(self, assignation_request: AssignationRequestMessage, message: aiormq.types.DeliveredMessage):
        assignation = await create_assignation_from_request(assignation_request)


        if assignation_request.meta.extensions.progress:
                print("Updating Progress")
                await message.channel.basic_publish(
                "Assigning".encode(), routing_key=assignation_request.data.progress,
                properties=aiormq.spec.Basic.Properties(
                    correlation_id=assignation.reference
                )

            )

        

        assignation_message = await sync_to_async(AssignationMessage.fromAssignation)(assignation)

        # We have created an assignation and are passing this to the proper authorities
        await message.channel.basic_publish(
            assignation_message.to_message(), routing_key="assignation_in",
            properties=aiormq.spec.Basic.Properties(
                correlation_id=assignation.reference, # TODO: Check if we shouldnt use message.header.properties.correlation_id
                reply_to=assignation.callback,
            )
        )

        await message.channel.basic_ack(message.delivery.delivery_tag)


    async def on_message(self, message:aiormq.types.DeliveredMessage):

        assignation_message = AssignationMessage.fromMessage(message=message)

        try:
            assignation = await create_assignation_from_request(assignation_message)

            templates = await find_templates_for_assignation(assignation)
            pods = await find_pods_for_assignation(assignation)


            print(templates, pods)


            if  assignation_message.meta.extensions.progress:
                print("Updating Progress")
                await message.channel.basic_publish(
                "Assigning".encode(), routing_key=assignation_message.meta.extensions.progress,
                properties=aiormq.spec.Basic.Properties(
                    correlation_id=assignation.reference
                ),

            )

            # We are routing it to Pod One / This Pod will then reply to
            await message.channel.basic_publish(
                message.body, routing_key="pod_two",
                properties=aiormq.spec.Basic.Properties(
                    correlation_id=assignation.reference,
                    reply_to=message.header.properties.reply_to
                )
            )

        
        except Exception as e:
            logger.error(e)

        await message.channel.basic_ack(message.delivery.delivery_tag)
        print(f'Request complete for {assignation_message.reference}')


    async def on_pod_done(self, message:aiormq.types.DeliveredMessage):

        print(message)




async def main(rabbit):
    # Perform connection
    await rabbit.connect()



class Command(BaseCommand):

    leave_locale_alone = True
    worker_class = Worker

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            "--layer",
            action="store",
            dest="layer",
            default=DEFAULT_CHANNEL_LAYER,
            help="Channel layer alias to use, if not the default.",
        )


    def handle(self, *args, **options):

        rabbit = RabbitMyFriend()
        # Get the backend to use
        
        loop = asyncio.get_event_loop()
        loop.create_task(main(rabbit))

        # we enter a never-ending loop that waits for data
        # and runs callbacks whenever necessary.
        print(" [x] Awaiting RPC requests")
        loop.run_forever()
