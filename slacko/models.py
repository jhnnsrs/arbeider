from delt.models import Pod, ProviderSettings, Template
from django.db import models

# Create your models here.






class SlackoSettings(ProviderSettings):
    default_workspace = models.CharField(max_length=1000, help_text="The Default Workspace you want to publish to")
    app_id = models.CharField(max_length=400, help_text="The App_id in Slack")
    client_id = models.CharField(max_length=1000, help_text="The SlackAPP Oauth2 Client ID")
    client_secret = models.CharField(max_length=1000, help_text="The SlackAPP Oauth2 Client Secret")
    signing_secret = models.CharField(max_length=1000, help_text="The SlackAPP Oauth2 Client Signing Secret (used to verify authenticity of slack)")





class SlackChannel(models.Model):
    channel = models.CharField(max_length=1000, help_text="The channel this template will publish to!")
    slack_bot_token = models.CharField(max_length=1000, help_text="The Help token for slack")




class SlackoPublisherTemplate(Template):
    channel = models.ForeignKey(SlackChannel, on_delete=models.CASCADE, help_text="The channel we will use")


class SlackoPublisher(Pod):
    pass




