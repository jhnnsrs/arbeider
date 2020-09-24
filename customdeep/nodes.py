from customdeep.konfigs import DeepLearningKonfig
from konfig.backend import register_konfig_node

@register_konfig_node(konfig=DeepLearningKonfig)
class DeepLearning(object):
    pass