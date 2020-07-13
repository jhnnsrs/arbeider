import logging
import uuid

from balder.subscriptions.base import BaseSubscription, SubscriptionError
from delt.bouncers.context import BouncerContext
from delt.models import Job, Pod
from delt.node import NodeConfig
from delt.orchestrator import get_orchestrator
from delt.pipes import assign_inputs_pipe
from delt.serializers import JobSerializer

logger = logging.getLogger(__name__)
 

class BaseJobSubscription(BaseSubscription):
    """Simple GraphQL subscription."""
    # Subscription payload.
    config: NodeConfig = None

    class Arguments:
        abstract = True

    @classmethod
    def subscribe(cls, root, info, *args, **kwargs):
        """Called when user subscribes."""
        reference = kwargs.pop("reference") if "reference" in kwargs else uuid.uuid4()
        pod = kwargs.pop("pod") if "pod" in kwargs else None
        node = cls.config.get_node()

        try:
            job = Job.objects.get(reference=reference)
            if job.pod.node == node:
                logger.info("Reconnecting to already configured Job")
                return [f'job_{reference}']
            else:
                raise Exception("This job already exists is another configuration. Cannot re-assign! Please use different refernce (UUID)")
        
        except Job.DoesNotExist:
            logger.info("We are trying to create a new Job")
            if pod is not None:
                try:
                    pod = Pod.objects.get(id=pod)
                    if pod.node == node:
                        context = BouncerContext(info=info)
                        logger.info("Pod exists, continue to assigning")
                        assign_inputs_pipe(reference, pod, kwargs, context)
                        return [f"job_{reference}"]
                    else:
                        raise Exception("This pod belongs not to this node!")
                except Pod.DoesNotExist:
                    raise Exception("We have not implemented that yet")    
            
        

    @classmethod
    def publish(cls, payload, info, *arg, **kwargs):
        """Called to notify the client."""
        # Here `payload` contains the `payload` from the `broadcast()`
        # invocation (see below). You can return `MySubscription.SKIP`
        # if you wish to suppress the notification to a particular
        # client. For example, this allows to avoid notifications for
        # the actions made by this particular client.
        serialized = JobSerializer(data=payload)
        if serialized.is_valid():
            serialized = {**serialized.validated_data}

            inputs = None
            if "inputs" in serialized:
                inelements = cls.config.inputs(data=serialized.pop("inputs"))
                if inelements.is_valid():
                    inputs = inelements.validated_data              
                        
            outputs = None
            if "outputs" in serialized:
                elements = cls.config.outputs(data=serialized.pop("outputs"))
                if elements.is_valid():
                    outputs = elements.validated_data

            return cls(**serialized, outputs=outputs, inputs=inputs)