from delt.pod import DummyPod
from delt.provisioner import BaseProvisioner


class KanalProvisioner(BaseProvisioner):
    allow_dummy = True

    def get_pod_for_selector(self, job, selector, context):
        return DummyPod()
