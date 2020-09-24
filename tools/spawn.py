import os
import sys
from pdb import run

import django
import docker

nodename = "fr"
reference = "sofinosincvdfvdfvfosidfdfneofisneofinsoeifnsoienf"

def spawn():
    
    from port.models import Flowly
    from delt.models import Provision
    from flow.models import FlowNode


    client = docker.from_env()
    print("Trying to spawn a docker")

    flow = FlowNode.objects.filter(name=nodename).first()
    
    print("Trying to Provision a Pod for" , flow)
    try:
        provision = Provision.objects.get(reference=reference)
        print("A provision already existed. Will not create a new one")
    except Provision.DoesNotExist as e:
        provision = Provision.objects.create(
            reference=reference,
            user_id=1,
            node=flow,
            provider="port",
            subselector="__all__"
        )
    
    print(provision)

    pod = provision.pod
    if pod is None:
        print("There was no Pod for this provision yet. Creating one!")
        container = client.containers.run("jhnnsrs/flowly", detach=True)
        print(container)
        pod = Flowly.objects.create(
            node=flow,
            provider="port",
            container_id= container.id
        )
        provision.pod = pod
        provision.save()

    print(pod)

    



if __name__ == "__main__":
    
    
    sys.path.insert(0, '/bergen')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbeid.settings")
    django.setup()

    spawn()
