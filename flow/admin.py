from django.contrib import admin

# Register your models here.
from flow.models import Engine, FlowNode, Graph

admin.site.register(FlowNode)
admin.site.register(Graph)
admin.site.register(Engine)