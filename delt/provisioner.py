from delt.job import JobContext
from delt.models import Job, Pod
from delt.pod import UNIQUESELECTOR, DummyPod, Selector
from delt.scopes import CAN_PROVISION_NODES


class BaseProvisionerError(Exception):
    pass

class NoPodProvisionedError(BaseProvisionerError):
    pass


class BaseProvisionerConfigError(BaseProvisionerError):
    pass


class BaseProvisioner(object):
    allow_auto_provision = False
    allow_dummy = True
    podClass = Pod

    def __init__(self):
        if not issubclass(self.podClass, Pod):
            raise BaseProvisionerConfigError("The podClass you specified does not inheirt from POD")
        super().__init__()


    
    def auto_provision_job(self, job: Job, context: JobContext):
        """ Should return the Job with a pod id set """
        raise NotImplementedError


    def get_pod_for_selector(self, job: Job, selector: Selector, context: JobContext):
        """ Get a Pod for this selector and job, 
        Arguments:
            selector {Selector} -- The Selector
        
        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError



    def get_pod(self, job: Job, context: JobContext):
        scopes = context.scopes
        selector = job.selector
        try: 
            pod = self.get_pod_for_selector(job, Selector(selector), context)
        except Pod.DoesNotExist as e:
            if self.allow_auto_provision and CAN_PROVISION_NODES in scopes:
                pod =  self.auto_provision_job(job, context)
            else:
                raise  NoPodProvisionedError("We couldnt Provision a Pod for this")

        if isinstance(pod, DummyPod) and not self.allow_dummy:
            raise BaseProvisionerConfigError("We provisioned a DummyPod, but Provisioner is not allowing dummys. Set allow_dummy")
        
        return pod
