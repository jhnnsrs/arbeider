from delt.discover import DiscoverMember, autodiscover


class BalderMember(DiscoverMember):
    type = "BALDER"
    field = "BALDER_SETTINGS"


def autodiscover_balder(*args, **kwargs):
    """ This function will be importing all Pods in the app directorys, if
     DELT_ENSURE_REGISTER env is set to True it will also try to register all nodes
     with the database"""
    return autodiscover(BalderMember, *args, **kwargs)