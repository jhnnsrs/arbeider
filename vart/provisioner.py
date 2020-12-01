from delt.consumers.provisioner import ProvisionConsumer


class PortProvision(ProvisionConsumer):
    settings = PortHandlerSettings()
    provider = "port"

    def get_pod(self, provision):
        logger.info(f"Received {provision}")

        # Are we provisioning a Flow???
        flow = provision.node.flownode
        if flow is None: raise NotImplementedError("We are still only able to provision FLOWS")

        if selectors.all(provision.subselector):
            # Lets check if there is already a running instance of this Pod? Maybe we can use that template?
            pod = Flowly.objects.filter(node=provision.node).first()
            if not pod:
                logger.info("No Pod with this configuration yet found")
                templates = provision.node.templates.filter(provider="port")
                
                logger.info(f"Found {templates.count()} Templates")
                
                
                template = templates.first()


                if provision.user:
                    pod = Flowly.objects.create(
                        node = flow,
                        podclass = "flow",
                        status = POD_PENDING,
                        provider = self.provider,
                        persistent = False
                    )

                    provision.pod = pod

                    container = spawnContainerForProvision(provision)
                    pod.container_id = container.id
                    pod.save()
                else:
                   raise PortProvisionError("Only signed in users are allowed to create Pods")


        if selectors.new(provision.subselector):
            if provision.user:
                    pod = Flowly.objects.create(
                        node = flow,
                        podclass = "flow",
                        status = POD_PENDING,
                        provider = self.provider,
                        persistent = False
                    )
                    
                    provision.pod = pod

                    container = spawnContainerForProvision(provision)
                    pod.container_id = container.id
                    pod.save()
            else:
                raise PortProvisionError("Only signed in users are allowed to create Pods")

        logger.info(f"Created POD with ID: {pod.container_id}")
        logger.info(f"Created POD with FLOW: {pod.node_id}")
        logger.info(f"Created POD with PROVISION: {provision.id}")
        return pod


    def assign_inputs(self, assignation: Assignation):

        pod = assignation.pod
        assignation_channel= assignation_channel_from_id(pod.id)
        serialized = AssignationModelSerializer(assignation)
        logger.info(f"Sending Assignation: {assignation_channel}")
        async_to_sync(channel_layer.send)(assignation_channel,{"type": "assign", "data" : serialized.data})

        
