from delt.messages.base import MessageModel
from delt.messages.exceptions.base import ExceptionMessage
from typing import Generic, Type, TypeVar
import pydantic
import json
import logging
import aiormq
from delt.enums import ExceptionType
T = TypeVar("T")
import logging

logger = logging.getLogger(__name__)

class Wrapper(Generic[T]):


    def __init__(self, baseModelClass: Type[T]) -> None:
        assert issubclass(baseModelClass, MessageModel), "Needs to subclass MessageModel"
        self.baseModelClass = baseModelClass
        pass


    def wrap(self, baseModel: T) -> bytes:
        return json.dumps(baseModel.dict()).encode()

    def unwrapped(self, ):

        def real_decorator(function):

            async def wrapper(cls, message: aiormq.types.DeliveredMessage):
                unwrapped = None
                try:
                    unwrapped = self.baseModelClass(**json.loads(message.body.decode()))
                    logger.info(f"Received {unwrapped}")

                except Exception as e:
                    logger.error(f"Client Error here {str(e)}")

                    backmessage = ExceptionMessage(data={
                        "type" : ExceptionType.CLIENT,
                        "base": "MalformedError",
                        "message": str(e)
                    })
                    
                    await message.channel.basic_publish(
                        backmessage.to_message(), routing_key=message.header.properties.reply_to,
                        properties=aiormq.spec.Basic.Properties(
                            correlation_id=message.header.properties.correlation_id
                        ),
                    )

                if unwrapped:
                    try:
                        return await function(cls, unwrapped, message = message)

                    except Exception as e:
                        logger.error(f"Inside Error here {str(e)}")

                        backmessage = ExceptionMessage(data={
                        "type" : ExceptionType.ARNHEIM,
                        "base": e.__class__.__name__,
                        "message": str(e)
                        })
                    
                        await message.channel.basic_publish(
                            backmessage.to_message(), routing_key=message.header.properties.reply_to,
                            properties=aiormq.spec.Basic.Properties(
                                correlation_id=message.header.properties.correlation_id
                            ),
                        )

                        raise e

            return  wrapper

        return real_decorator


    def unwrap(self, message: aiormq.types.DeliveredMessage) -> T:
        return self.baseModelClass(**json.loads(message.body.decode()))