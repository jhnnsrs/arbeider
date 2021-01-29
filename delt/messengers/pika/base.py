from delt.messengers.base import BaseMessenger
import pika
import json
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class PikaMessenger(BaseMessenger):
    baseModel = None
    pack = "data"

    def __init__(self, exchange="") -> None:#
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters('mister',
                                            5672,
                                            '/',
                                            credentials)

        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        self.channel = channel
        self.exchange = exchange
        super().__init__(channel)

    def contact(self, routing_key: str, data: str, correlation_id = None, reply_to = None):
        assert isinstance(data, BaseModel), "This Messenger uses a BaseModel as a serializer please provide an instance of it"

        properties = {}
        if correlation_id is not None: properties["correlation_id"] = correlation_id
        if reply_to is not None: properties["reply_to"] = reply_to


        self.channel.basic_publish(exchange=self.exchange,routing_key=routing_key,
                      body=json.dumps(data.dict()).encode(),
                      properties=pika.BasicProperties(
                          content_type="application/json",**properties
                      )
        )

    
    def receive(self, baseModel = None):
        baseModel = baseModel or self.baseModel
        
        def real_decorator(function):

            def wrapper(cls, message):
                function(cls, message)

            return wrapper

        return real_decorator