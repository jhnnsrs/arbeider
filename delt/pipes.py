
from delt.models import Job, Pod, Node
from delt.settingsregistry import get_settings_registry
from delt.publishers.base import BasePublisher
from delt.job import JobContext
import logging

logger = logging.getLogger(__name__)


def new_job_pipe(job: Job, context: JobContext):

    publishers = job.node.publishers

    if "job" in publishers:
        for publisher in publishers["job"]:
            logger.info(f"Publishing Job to {publisher}")
            handler: BasePublisher = get_settings_registry().getPublisher(publisher)
            handler.on_job_created(job)

    logger.info("Done")