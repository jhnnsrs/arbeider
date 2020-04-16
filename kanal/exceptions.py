
class BaseKanalException(Exception):
    pass

class BaseKanalConsumerException(BaseKanalException):
    pass

class BaseKanalHandlerException(BaseKanalException):
    pass

class KanalHandlerConfigException(BaseKanalHandlerException):
    pass

class KanalConsumerConfigException(BaseKanalConsumerException):
    pass



class KanalConsumerMinorException(BaseKanalConsumerException):
    pass