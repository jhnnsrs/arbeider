from delt.selectors.parser import parse_selector_to_kwargs
from delt.selectors.base import BaseSelector
from delt.registries.registry import BaseRegistry
from delt.models import Provider, Selector

selectorregistry = None

import logging

logger = logging.getLogger(__name__)


class SelectorRegistry(BaseRegistry):

    def __init__(self) -> None:
        self.providerBaseSelectorMap: dict[str, BaseSelector] = {}
        self.providerSelectorMap: dict[str, Selector] = {}

    def registerSelector(self,provider: str, selector: BaseSelector):

        selectormodel = None
        try:
            try:
                selectormodel = Selector.objects.get(provider__name=provider)
            except Selector.DoesNotExist:
                providermodel, created  = Provider.objects.get_or_create(name=provider)
                if created: logger.warn("Created Provider within Selector")
                selectormodel = Selector.objects.create(provider=providermodel, kwargs= parse_selector_to_kwargs(selector))
        except:
            logger.error("Please migrate database changes first!!!")


        assert provider not in self.providerSelectorMap, "At the moment we cant register diefferent Selectors for the Providers"
        self.providerBaseSelectorMap[provider] = selector
        self.providerSelectorMap[provider] = selectormodel

    def getBaseSelectorForProvider(self, provider):
        return self.providerBaseSelectorMap[provider]

    def getSelectorForProvider(self, provider):
        return self.providerSelectorMap[provider]

    def getSelectorsMap(self, identifier):
        return self.providerSelectorMap




def get_selector_registry() -> SelectorRegistry:
    global selectorregistry
    if selectorregistry is None:
        selectorregistry = SelectorRegistry()
    return selectorregistry



