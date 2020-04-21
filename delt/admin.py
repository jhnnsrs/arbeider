from django.contrib import admin

# Register your models here.
from .models import Node, Route, Job, Pod

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