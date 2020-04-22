import channels_graphql_ws
import graphene
from graphene.types import generic

class JobSubscription(channels_graphql_ws.Subscription):
    """Simple GraphQL subscription."""

    # Subscription payload.
    event = graphene.String()
    args = generic.GenericScalar()

    class Arguments:
        """That is how subscription arguments are defined."""
        podid = graphene.Int()
        instanceid = graphene.Int()

    @staticmethod
    def subscribe(root, info, podid, instanceid):
        """Called when user subscribes."""

        # Return the list of subscription group names.
        print(podid)
        print(info.context.user)
        return ['pod_'+str(podid)]

    @staticmethod
    def publish(payload, info, podid, instanceid):
        """Called to notify the client."""

        # Here `payload` contains the `payload` from the `broadcast()`
        # invocation (see below). You can return `MySubscription.SKIP`
        # if you wish to suppress the notification to a particular
        # client. For example, this allows to avoid notifications for
        # the actions made by this particular client.
        print(info.context)
        print("Hallo"+str(payload))

        return JobSubscription(event='Something has happened!', args=payload["args"])



class SendJobToPodSubscription(channels_graphql_ws.Subscription):
    """Simple GraphQL subscription."""

    # Subscription payload.
    event = graphene.String()
    args = generic.GenericScalar()

    class Arguments:
        """That is how subscription arguments are defined."""
        args = generic.GenericScalar()
        node = graphene.Int()
        instanceid = graphene.Int()

    @staticmethod
    def subscribe(root, info, args, instanceid):
        """Called when user subscribes."""

        # Return the list of subscription group names.
        print(podid)

        job = Job.objects.create(
                args=inputs,
                creator= request.user,
                node = self.node,
                pod = pod,
                instance= serializer.validated_data["instance"],
                )
            
        return ['pod_'+str(podid)]

    @staticmethod
    def publish(payload, info, podid, instanceid):
        """Called to notify the client."""

        # Here `payload` contains the `payload` from the `broadcast()`
        # invocation (see below). You can return `MySubscription.SKIP`
        # if you wish to suppress the notification to a particular
        # client. For example, this allows to avoid notifications for
        # the actions made by this particular client.
        print("Hallo"+str(payload))

        return JobSubscription(event='Something has happened!', args=payload["args"])