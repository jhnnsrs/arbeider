from slacko.models import SlackChannel, SlackoPublisher, SlackoPublisherTemplate, SlackoSettings
from django.contrib import admin

# Register your models here.
admin.site.register(SlackoSettings)
admin.site.register(SlackChannel)
admin.site.register(SlackoPublisherTemplate)
admin.site.register(SlackoPublisher)