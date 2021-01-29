from balder.scalars.models import NodeID
import logging
import uuid

import graphene
from graphene.types.generic import GenericScalar
from graphql.language.ast import IntValue, StringValue

from balder.subscriptions.assignation.base import BaseAssignationSubscription
from delt.models import Node, Pod, Assignation
from delt.pipes import (assign_inputs_pipe, assign_inputs_to_node_pipe)
import pika


logger = logging.getLogger(__name__)


class AssignSubscription(BaseAssignationSubscription):

    class Arguments:
        node = NodeID(required=False, description="The node id")
        pod = graphene.ID(required=False, description="The pod id")
        template = graphene.ID(required=False, description="The template id")
        reference = graphene.String(required=True, description="The pods id")
        inputs = GenericScalar(required=True, description="The Inputs for this Pod")
        extensions = GenericScalar(description="Extensions to the Assignment Protocol")
        progress = graphene.Boolean(required=False, default_value=False)



    @classmethod
    def accept(cls, context, root, info, *args, **kwargs):

        reference = kwargs.pop("reference") if "reference" in kwargs else uuid.uuid4()
        inputs = kwargs.pop("inputs") if "inputs" in kwargs else None
        podid = kwargs.pop("pod") if "pod" in kwargs else None
        node = kwargs.pop("node") if "node" in kwargs else None
        templateid = kwargs.get("template", None)
        progress = kwargs.get("progress")



        if node:
            print(node)
            assign_inputs_to_node_pipe(context, reference, inputs, node, progress=progress)

        if podid:
            try:
                pod = Pod.objects.get(id=podid)
            except Pod.DoesNotExist:
                raise Exception("The pod you specified does not exist!")
        
        
        return [f"assign_{reference}"]
       
       
        """ try:
            pod = Pod.objects.get(id=pod)
        except Pod.DoesNotExist:
            raise Exception("The pod you specified does not exist!")

        try:
            assignation = Assignation.objects.get(reference=reference)
            if assignation.pod == pod:
                logger.info("Reconnecting to already configured Job")
                return [f'{reference}']
            else:
                raise Exception("This provision already exists is another configuration. Cannot re-assign! Please use different refernce (UUID)")
        except Assignation.DoesNotExist:

            logger.info("We are trying to create a new Pod through this Provision")
            assignation = assign_inputs_pipe(context, reference, pod, inputs)

        
        return [f"{reference}"] """
