from delt.messages.base import MessageDataModel, MessageMetaModel, MessageMetaExtensionsModel, MessageModel
from pydantic import BaseModel
from typing import Optional
from delt.models import Assignation
from delt.messages.types import ASSIGNATION
class AssignationParams(BaseModel):
    pass

class AssignationMetaExtensionsModel(MessageMetaExtensionsModel):
    progress: Optional[str]

class AssignationMetaModel(MessageMetaModel):
    type: str
    extensions: Optional[AssignationMetaExtensionsModel]

class AssignationDataModel(MessageDataModel):
    id: int
    node: Optional[int] #TODO: Maybe not optional
    pod: Optional[int]
    template: Optional[int]
    reference: str
    callback: Optional[str]
    progress: Optional[str]

    inputs: dict
    outputs: Optional[dict]
    params: Optional[AssignationParams]


class AssignationMessage(MessageModel):
    data: AssignationDataModel
    meta: AssignationMetaModel

    @classmethod
    def fromAssignation(cls, assignation: Assignation, **extensions):
        
        data = {
            "reference": assignation.reference,
            "id" : assignation.id,
            "node": assignation.node.id,
            "template": assignation.template.id if assignation.template else None,
            "pod": assignation.pod.id if assignation.pod else None,
            "callback": assignation.callback,
            "progress": assignation.progress,
            "inputs": assignation.inputs or {},
            "params": {}
        }

        meta = {
            "type" : ASSIGNATION,
            "extensions": extensions
        }

        return cls(**{"data": data, "meta": meta})













