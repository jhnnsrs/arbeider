from balder.register import  register_subscription
from balder.wrappers import NodeSubscriptionWrapper
from elements.types import RepresentationType, SampleType
from filters.configs.filters.blur import BlurFilterKonfig
from filters.configs.filters.prewitt import PrewittFilterKonfig
from filters.configs.projections.maxisp import MaxISPConfig

@register_subscription("maxisp", description="Make a Request to the MaxISP backend")
class JobWrapper(NodeSubscriptionWrapper):
    config = MaxISPConfig


@register_subscription("prewitt", description="Make a Request to the Prewitt backend")
class JobWrapper(NodeSubscriptionWrapper):
    config = PrewittFilterKonfig