import re

from balder.builders.utils import (generate_grapheneargs_from_serializer,
                                   generate_graphenefields_from_serializer,
                                   generateArgumentsFromGrapheneFields)
from balder.mutations.serializer import BaseSerializerMutation


def genericSerializerMutationBuilder(wrapper, path, serializer_class, arguments=None): 

    name = re.sub(r"[^A-Za-z]+", '', path.capitalize())

    mutationFields = generate_graphenefields_from_serializer(serializer_class())
    if arguments is None:
        argFields = generate_grapheneargs_from_serializer(serializer_class())
    else:
        #TODO: Failure check here
        argFields = arguments

    arguments = generateArgumentsFromGrapheneFields(name, argFields, description="Serializer Arguments")
    #Arguments will have the same instances as the Serializer, so you call them with the real Arguments

    return type(name+"Mutation", (BaseSerializerMutation,), {**mutationFields, "Arguments" : arguments, "wrapper": wrapper})