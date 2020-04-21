import channels_graphql_ws
import graphene
from graphene import Dynamic
from graphene.types import generic

from balder.types import JobQuery


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

class Query(graphene.ObjectType, JobQuery, Dynamic):
    """Root GraphQL query."""
    # Check Graphene docs to see how to define queries.
    pass

class Mutation(graphene.ObjectType):
    """Root GraphQL mutation."""
    # Check Graphene docs to see how to define mutations.
    pass

class Subscription(graphene.ObjectType):
    """Root GraphQL subscription."""
    job_subscription = JobSubscription.Field()

graphql_schema = graphene.Schema(
    query=Query,
    subscription=Subscription,
)