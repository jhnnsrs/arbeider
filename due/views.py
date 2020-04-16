from due.utils import UUIDEncoder
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from rest_framework.serializers import Serializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
import json

import logging
channel_layer = get_channel_layer()

logger = logging.getLogger(__name__)


class PublishingModelViewSet(viewsets.ModelViewSet):
    publishers = None

    def publish(self, serializer, method):

        serializedData = serializer.data
        serializedData = json.loads(json.dumps(serializedData, cls=UUIDEncoder)) #Shit workaround to get UUID to be string

        if self.publishers is not None:
            logger.info(f"Publishers {self.publishers}")
            for el in self.publishers:
                modelfield = "empty"
                try:
                    path = ""
                    for modelfield in el:
                        try:
                            value = serializedData[modelfield]
                            path += "{0}_{1}_".format(str(modelfield), str(value))
                        except KeyError as e:
                            logger.info("Modelfield {0} does not exist on {1}".format(str(el), str(self.serializer_class.__name__)))
                            logger.info("Publishing to String {0}".format(modelfield))
                            path += "{0}_".format(str(modelfield))
                    path = path[:-1]
                    logger.info("Publishing to Models {0}".format(path))
                    stream = str(serializer.Meta.model.__name__)
                    async_to_sync(channel_layer.group_send)(path, {"type": "stream", "stream": stream, "room": path,
                                                                   "method": method, "data": serializedData})
                except KeyError as e:
                    logger.info("Error Babe !!!".format(str(el), str(self.serializer_class.__name__)))


    def perform_create(self, serializer):
        super().perform_create(serializer)
        logger.info("CALLED create")
        self.publish(serializer, "create")

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self.publish(serializer, "update")

    def perform_destroy(self, instance):
        serialized = self.serializer_class(instance)
        self.publish(serialized, "delete")
        super().perform_destroy(instance)
