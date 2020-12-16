from django.contrib import admin

# Register your models here.
from flow.models import Compiler, CompilerRoute, Graph

admin.site.register(CompilerRoute)
admin.site.register(Compiler)
admin.site.register(Graph)