from filters.konfigs.filters.prewitt import PrewittFilterKonfig
from filters.konfigs.projections.maxisp import MaxISPConfig




# @register_subscription("maxisp", description="Make a Request to the MaxISP backend")
class JobWrapper(object):
    config = MaxISPConfig

#@register_subscription("prewitt", description="Make a Request to the Prewitt backend")
class JobWrapper(object):
    config = PrewittFilterKonfig