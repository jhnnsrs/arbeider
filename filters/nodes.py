from delt.nodes.default import register_node, ConfigNode


from .configs.filters.prewitt import PrewittFilterConfig
from .configs.filters.blur import BlurFilterConfig
from .configs.projections.maxisp import MaxISPConfig


@register_node(PrewittFilterConfig)
class PrewittNode(ConfigNode):
    pass

@register_node(BlurFilterConfig)
class BlurNode(ConfigNode):
    pass

@register_node(MaxISPConfig)
class MaxISPNode(ConfigNode):
    pass