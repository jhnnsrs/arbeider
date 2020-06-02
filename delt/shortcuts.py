from rest_framework.request import Request
from django.db import models
from guardian.shortcuts import get_perms
import logging
import re
from delt.models import Pod, Node

logger = logging.getLogger(__name__)

def is_authorized(permission, scopes, request: Request= None, instance: models.Model=None, needscopes=False):
    if request is not None:
        app_authorization = True
        grant_scope = "SESSION"
        if request.auth is not None:
            for scope in request.auth.scopes:
                if scope in scopes:
                    app_authorization = True
                    grant_scope = scope
                    break
                else: 
                    app_authorization = False

        if app_authorization:
            if request.user is not None:
                if request.user.is_superuser:
                    logger.info(f"Authorized because of Super User Status and {grant_scope}-Scope")
                    return True
                if permission in get_perms(request.user, instance):
                    logger.info(f"Authorized because of Object Permission {permission} and {grant_scope}-Scope")
                    return True
                else:
                    return False






def get_pod_for_selector(selector: str, nodeid: int) -> Pod:

    m = backend_id_selector.match(selector)
    if m:
        return Pod.objects.get(provider=m.group('provider'), unique=m.group("unique"), node_id=nodeid)

    m = backend_selector.match(selector)
    if m:
        return Pod.objects.filter(provider=m.group('provider'), node_id=nodeid).first()

    raise NoPodForSelector(f"We couldnt find an Pod for Selector:{selector}")