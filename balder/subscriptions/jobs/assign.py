import logging
import uuid

import graphene
from graphene.types.generic import GenericScalar

from balder.subscriptions.jobs.base import BaseAssignationSubscription
from delt.models import Job, Pod, Assignation
from delt.pipes import (assign_inputs_pipe, provision_pod_pipe,
                        republish_provision_pipe)

logger = logging.getLogger(__name__)

class AssignSubscription(BaseAssignationSubscription):

    class Arguments:
        pod = graphene.ID(required=True, description="The pods id")
        reference = graphene.String(required=False, description="The pods id")
        inputs = GenericScalar(required=True, description="The Inputs for this Pod")


    @classmethod
    def accept(cls, context, root, info, *args, **kwargs):

        reference = kwargs.pop("reference") if "reference" in kwargs else uuid.uuid4()
        inputs = kwargs.pop("inputs") if "inputs" in kwargs else None
        pod = kwargs.pop("pod") if "pod" in kwargs else None
       
        try:
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
            provision = assign_inputs_pipe(context, reference, pod, inputs)

        
        return [f"{reference}"]
