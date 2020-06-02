from konfig.backend import register_konfig_node


from .configs.filters.prewitt import PrewittFilterConfig
from .configs.filters.blur import BlurFilterConfig
from .configs.projections.maxisp import MaxISPConfig


@register_konfig_node(PrewittFilterConfig)
class PrewittNode(object):
    pass

@register_konfig_node(BlurFilterConfig)
class BlurNode(object):
    pass

@register_konfig_node(MaxISPConfig)
class MaxISPNode(object):
    pass