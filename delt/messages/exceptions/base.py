from delt.messages.base import MessageDataModel, MessageMetaModel, MessageModel
from typing import Optional
from pydantic import BaseModel
from enum import Enum
from delt.messages.types import EXCEPTION
from delt.enums import ExceptionType



class ExceptionMetaMessage(MessageMetaModel):
    type: str = EXCEPTION


class ExceptionDataMessage(MessageDataModel):
    type: ExceptionType
    base: str
    message: str
    traceback: Optional[str] 

class ExceptionMessage(MessageModel):
    data: ExceptionDataMessage
    meta: ExceptionMetaMessage = { "type" : EXCEPTION}
