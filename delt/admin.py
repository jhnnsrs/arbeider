from django.contrib import admin

# Register your models here.
from .models import Assignation, DataModel, DataPoint, Node, Provider, ProviderSettings, Provision, Repository, Route, Pod, Selector, Template

class RouteInline(admin.TabularInline):
    model = Route
    fields = ('name',)
    readonly_fields = ('name',)

class NodeAdmin(admin.ModelAdmin):
    model = Node
    inlines = (RouteInline,)

admin.site.register(Route)
admin.site.register(Node, NodeAdmin)
admin.site.register(Pod)
admin.site.register(Provision)
admin.site.register(Assignation)
admin.site.register(Repository)
admin.site.register(Provider)
admin.site.register(Template)
admin.site.register(ProviderSettings)
admin.site.register(Selector)
admin.site.register(DataPoint)
admin.site.register(DataModel)