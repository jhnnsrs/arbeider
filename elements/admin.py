from django.contrib import admin

# Register your models here.
from elements.models import Antibody, Sample, Experiment, ExperimentalGroup, Representation, Transformation
from guardian.admin import GuardedModelAdmin

class RepresentationInline(admin.TabularInline):
    model = Representation

class SampleAdmin(admin.ModelAdmin):
    inlines = [
        RepresentationInline,
    ]

class RepresentationAdmin(GuardedModelAdmin):
    pass

admin.site.register(Transformation)
admin.site.register(Antibody)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Experiment)
admin.site.register(Representation, RepresentationAdmin)
admin.site.register(ExperimentalGroup)