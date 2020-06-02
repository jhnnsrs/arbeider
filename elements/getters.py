from django.contrib.auth.models import Group


def get_all_access_group_names():
    return ["post-doc","pi","admin"]

all_access_groups = None

def get_all_access_groups():
    global all_access_groups
    if all_access_groups is None:
        all_access_groups = [Group.objects.get_or_create(name=el)[0] for el in get_all_access_group_names()]
    return all_access_groups