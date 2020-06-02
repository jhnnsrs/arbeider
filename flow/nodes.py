from flow.konfigs.generics import IntInputKonfig, StrInputKonfig
from flow.konfigs.inputs import RepresentationInputKonfig
from flow.konfigs.outputs.generics import IntOutputKonfig, StrOutputKonfig
from flow.konfigs.outputs.models import RepresentationOutputKonfig
from konfig.backend import register_konfig_node


@register_konfig_node(RepresentationInputKonfig)
class Representation(object):
    pass

@register_konfig_node(IntInputKonfig)
class Int(object):
    pass

@register_konfig_node(StrInputKonfig)
class String(object):
    pass


# Outputs


@register_konfig_node(RepresentationOutputKonfig)
class Representation(object):
    pass

@register_konfig_node(IntOutputKonfig)
class Int(object):
    pass

@register_konfig_node(StrOutputKonfig)
class String(object):
    pass