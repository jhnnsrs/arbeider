

class ProvisionException(Exception):
    pass


class NoMatchablePod(ProvisionException):
    pass