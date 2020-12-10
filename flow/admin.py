from django.contrib import admin

# Register your models here.
from flow.models import Compiler, CompilerRoute, Engine, FlowNode, Graph

admin.site.register(FlowNode)
admin.site.register(CompilerRoute)
admin.site.register(Compiler)
admin.site.register(Graph)
admin.site.register(Engine)