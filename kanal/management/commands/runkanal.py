from kanal.registry import get_kanal_registry
import logging

from channels import DEFAULT_CHANNEL_LAYER
from channels.layers import get_channel_layer
from channels.routing import get_default_application
from channels.worker import Worker
from django.conf import settings
from django.core.management import BaseCommand, CommandError

from delt.discover import autodiscover_pods
from delt.orchestrator import get_orchestrator

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    leave_locale_alone = True
    worker_class = Worker

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            "--layer",
            action="store",
            dest="layer",
            default=DEFAULT_CHANNEL_LAYER,
            help="Channel layer alias to use, if not the default.",
        )


    def handle(self, *args, **options):
        # Get the backend to use
        self.verbosity = options.get("verbosity", 1)
        # Get the channel layer they asked for (or see if one isn't configured)
        if "layer" in options:
            self.channel_layer = get_channel_layer(options["layer"])
        else:
            self.channel_layer = get_channel_layer()
        if self.channel_layer is None:
            raise CommandError("You do not have any CHANNEL_LAYERS configured.")
        # Autodiscover all of the the worker
        print("Starting")
        autodiscover_pods(backend="kanal", register=True)
        print("Ending")
        allchannels = [key for key, _ in get_kanal_registry().getConsumersMap().items()]
        names = "\n".join([f'{consumer.konfig.name} at {key}' for key, consumer in get_kanal_registry().getConsumersMap().items()])
        logger.info("Running worker for channels %s", allchannels)
        worker = self.worker_class(
            application=get_default_application(),
            channels=allchannels,
            channel_layer=self.channel_layer,
        )
        print(f'''
_________________________________________________________________________________________

                 __  ___      ___      .__   __.      ___       __      
                |  |/  /     /   \     |  \ |  |     /   \     |  |     
                |  '  /     /  ^  \    |   \|  |    /  ^  \    |  |     
                |    <     /  /_\  \   |  . `  |   /  /_\  \   |  |     
                |  .  \   /  _____  \  |  |\   |  /  _____  \  |  `----.
                |__|\__\ /__/     \__\ |__| \__| /__/     \__\ |_______|

Connected to Channel Layer: {options["layer"]}
Kanal is running with the following workers:

{names}

Happy Debugging!                                                                                                                                         
                                                                        ''')
        worker.run()
