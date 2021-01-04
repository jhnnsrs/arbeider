from django.conf import settings
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from guardian.shortcuts import assign_perm
from elements.getters import get_all_access_groups
from .models import Representation
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Representation)
def rep_post_save(sender, **kwargs):
    """
    Assign Permission to the Representation
    """
    permissions = ["download_representation","view_representation"]
    representation, created = kwargs["instance"], kwargs["created"]
    if created:
        logger.info(f"Assigning Permissions {permissions} to Representation")
        for permission in permissions:
            assign_perm(permission, representation.sample.creator, representation)
            for group in get_all_access_groups():
                assign_perm(permission, group, representation)