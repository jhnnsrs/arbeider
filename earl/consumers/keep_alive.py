# chat/consumers.py
from delt.models import Pod
from delt.enums import PodStatus
import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import logging
from earl.models import Peasent, PeasentPod, PeasentTemplate
import aiormq
from delt.messages.assignation import AssignationMessage




logger = logging.getLogger(__name__)

@sync_to_async
def activatePeasentPods(peasent_name, channel):
    for peasent_template in PeasentTemplate.objects.filter(peasent__name=peasent_name):
        print(peasent_template)

        PeasentPod.objects.create(
            template = peasent_template,
            status = PodStatus.ACTIVE.value,
            channel = channel
        )


@sync_to_async
def deactivatePeasentPods(peasent_name):
    for peasent_template in PeasentTemplate.objects.filter(peasent__name=peasent_name):
        for pod in peasent_template.pods.all():
            pod.delete()





class KeepPeasentAliveConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        logger.error("Connecting")
        self.auth = self.scope["auth"]
        print(self.auth.application)
        if not self.auth:
            await self.close()


        await self.accept()
        self.peasent_name = self.scope['url_route']['kwargs']['peasent_name']


        self.channel_name = await self.connect_to_rabbit()
        await activatePeasentPods(self.peasent_name, self.channel_name)

    async def connect_to_rabbit(self):
        # Perform connection
        self.connection = await aiormq.connect(f"amqp://guest:guest@mister/")
        self.channel = await self.connection.channel()
        # Declaring queue
        self.assignment_queue = await self.channel.queue_declare()

        # Start listening the queue with name 'hello'
        await self.channel.basic_consume(self.assignment_queue.queue, self.on_message)
        return self.assignment_queue.queue
        
    async def on_message(self, message):
        print(message)
        await self.send(text_data=message.body.decode()) # No need to go through pydantic???
        await message.channel.basic_ack(message.delivery.delivery_tag)


    async def disconnect(self, close_code):
        self.peasent_name = self.scope['url_route']['kwargs']['peasent_name']
        logger.info("Disconnecting Client")
        await deactivatePeasentPods(self.peasent_name)
        await self.connection.close()

    async def receive(self, text_data):
        assignation = AssignationMessage.from_channels(text_data)

        await self.channel.basic_publish(
            assignation.to_message(), routing_key="assignation_done",
            properties=aiormq.spec.Basic.Properties(
                correlation_id=assignation.data.reference
        )
        )