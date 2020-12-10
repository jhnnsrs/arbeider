from channels.consumer import SyncConsumer


class BaseConsumer(SyncConsumer):
    channel = None
    gateway = None

    def __init__(self) -> None:
        assert self.channel is not None, "Please instantiate with a proper ChannelMessenger"
        assert self.gateway is not None, "Please instantiate with a proper GatewayMessenger"
        super().__init__()

    def test_message(self, message):
        print(f"{self.channel} is Reachable with {message}")