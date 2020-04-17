from delt.pod import DummyPod, Selector, UNIQUESELECTOR
from delt.job import JobContext
from delt.provisioner import BaseProvisioner
from delt.models import Pod, Job

class FremmedProvisioner(BaseProvisioner):
    allow_dummy = False
    allow_auto_provision = False

    def get_pod_for_selector(self, job: Job, selector: Selector, context: JobContext):
        if selector.type == UNIQUESELECTOR:
            print(selector.params)
            return Pod.objects.get(pk = selector.params)

        return DummyPod()

        
