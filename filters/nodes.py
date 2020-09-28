from filters.konfigs.tests import TestConfig
from filters.konfigs.filters.sleep import SleepFilter
from konfig.backend import register_konfig_node


from .konfigs.filters.prewitt import PrewittFilterKonfig
from .konfigs.filters.blur import BlurFilterKonfig
from .konfigs.projections.maxisp import MaxISPConfig


@register_konfig_node(PrewittFilterKonfig)
class PrewittNode(object):
    pass

@register_konfig_node(BlurFilterKonfig)
class BlurNode(object):
    pass

@register_konfig_node(SleepFilter)
class SleepFilterNode(object):
    pass

@register_konfig_node(MaxISPConfig)
class MaxISPNode(object):
    pass

@register_konfig_node(TestConfig)
class TestNode(object):
    pass