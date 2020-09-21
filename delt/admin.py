from django.contrib import admin

# Register your models here.
from .models import Assignation, Node, Provision, Route, Job, Pod

class RouteInline(admin.TabularInline):
    model = Route
    fields = ('name',)
    readonly_fields = ('name',)

class NodeAdmin(admin.ModelAdmin):
    model = Node
    inlines = (RouteInline,)

admin.site.register(Route)
admin.site.register(Job)
admin.site.register(Node, NodeAdmin)
admin.site.register(Pod)
admin.site.register(Provision)
admin.site.register(Assignation)