from filters.configs.filters.sleep import SleepFilter
from konfig.backend import register_konfig_node


from .configs.filters.prewitt import PrewittFilterKonfig
from .configs.filters.blur import BlurFilterKonfig
from .configs.projections.maxisp import MaxISPConfig


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