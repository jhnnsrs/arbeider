import logging

import graphene
from graphene.types.generic import GenericScalar

from balder.mutations.base import BaseMutation
from flow.balder.types import FlowNodeType
from flow.models import FlowNode, Graph
from konfig.node import node_identifier


class ToFlowException(Exception):
    pass

logger = logging.getLogger(__name__)

def resolve_inputs(model):
    if model["package"] == "@flow/inputs/model":
         return { "type": "model", "identifier":  model["interface"]}
    if model["package"] == "@flow/inputs/generics":
        return { "type": model["interface"]}

def resolve_outputs(model):
    if model["package"] == "@flow/outputs/model":
         return { "type": "model", "identifier":  model["interface"]}
    if model["package"] == "@flow/outputs/generics":
        return { "type": model["interface"]}


class ToFlowMutation(BaseMutation):
    status = graphene.String()
    node = graphene.Field(FlowNodeType, description="The Generated FlowNode")

    class Arguments:
        graph = graphene.ID(required=True, description ="The graph that we want")

    @staticmethod
    def mutate(root, info, **kwargs):
        graphid = kwargs["graph"]
        user = info.context.user

        try:
            graph = Graph.objects.get(id=graphid)
            # TODO: Really parse a Flow node through this
            diagram = graph.diagram

            if "layers" in diagram:
                inputs = []
                outputs = []
                layers = diagram["layers"]

                for layer in layers:
                    if layer["type"] == "diagram-nodes":
                        models = layer["models"]
                        for key, model in models.items(): 
                            print(model)
                            if model["variety"] == "input":
                                extras = resolve_inputs(model)
                                if extras is not None:
                                    inputs.append({
                                        "name": model["name"],
                                        "key": key,
                                        "description": model.get("description", "NOT IMPLEMENTED YET"),
                                        "required": True, #If you create it as an input you should always think of it as required
                                        "default": None,
                                        **extras
                                    })
                            if model["variety"] == "output":
                                extras = resolve_outputs(model)
                                if extras is not None:
                                    outputs.append({
                                        "name": model["name"],
                                        "key": key,
                                        "description": model.get("description", "NOT IMPLEMENTED YET"),
                                        "required": True, #If you create it as an input you should always think of it as required
                                        "default": None,
                                        **extras
                                    })

                                
                                
                            

                package = f"@flow/{graph.creator}"
                interface = graph.name+graph.version

                identifier = node_identifier(package, interface)

                flowDict = {
                    "nodeclass": "flow",
                    "variety": "flow",
                    "inputs": inputs,
                    "outputs": outputs,
                    "package": package,
                    "interface": interface,
                    "graph": graph,
                    "name": graph.name,
                    "description": graph.description
                }
                
                try: 
                    node =  FlowNode.objects.get(identifier=identifier)
                    for key, value in flowDict.items():
                        setattr(node, key, value)
                    node.save()
                    logger.info(f"Updated {package}/{interface} on Identifier: {identifier}")

                    return ToFlowMutation(status="updated", node=node)
                except FlowNode.DoesNotExist as e:
                    combined = {"identifier": identifier, **flowDict}
                    node = FlowNode(**combined)
                    node.save()
                    logger.info(f"Created {package}/{interface} on Identifier: {identifier}")

                    return ToFlowMutation(status="created", node=node)

            else:
                return ToFlowException("We have no idea about how to deal with this particular. Graph: Version Mismatch")

        except Graph.DoesNotExist as e:
            raise e
