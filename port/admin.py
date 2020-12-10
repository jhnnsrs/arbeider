from django.contrib import admin

# Register your models here.
from port.models import Container, ContainerTemplate, PortPod, PortSettings

admin.site.register(PortSettings)
admin.site.register(PortPod)
admin.site.register(Container)
admin.site.register(ContainerTemplate)