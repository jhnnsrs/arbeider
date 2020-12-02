from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import sys, os
import django

def main():

    layer = get_channel_layer()
    channel = "vart_gateway"
    type = "provision_succeeded"
    async_to_sync(layer.send)(channel, {"type": type, "data": {"empty": True}})

    pass




if __name__ == "__main__":
    
    sys.path.insert(0, '/bergen')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbeid.settings")
    django.setup()

    main()