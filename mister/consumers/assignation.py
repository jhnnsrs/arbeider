from delt.messengers.assignation import AssignationMessenger
from channels.consumer import AsyncConsumer, SyncConsumer
import aiormq
import asyncio
import pika
import json

messenger = AssignationMessenger("mister")


credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('mister',
                                       5672,
                                       '/',
                                       credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()


class AssignationConsumer(SyncConsumer):

    def __init__(self):
        self.setuped = False
        super().__init__()

    @messenger.receive()
    def assign_to_node(self, assignation):

        message = {
            "data": {
                "node": assignation.node.id,
                "inputs": assignation.inputs,  
                **dict({}),
            },
            "meta": {
                "type" : "assignation",
                "extensions": {}
            }
        }  

        channel.basic_publish(exchange="",routing_key='my_queue',
                      body=str(json.dumps(message)).encode(),
                      properties=pika.BasicProperties(
                          content_type="application/json",
                          correlation_id=assignation.reference,
                          reply_to="gateway_in"
                      )
        )
