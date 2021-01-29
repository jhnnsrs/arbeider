
from mister.wrapper import Wrapper
from delt.messages.assignation import AssignationMessage
from delt.messages.assignation_request import AssignationRequestMessage

assignationRequestWrapper = Wrapper(AssignationRequestMessage)
assignationWrapper = Wrapper(AssignationMessage)