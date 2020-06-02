import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from oauth2_provider.models import Application

AUTHORIZATION_TYPE = "password"
class Command(BaseCommand):
    help = "Creates an Consuming Application user non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument('--overwrite', help="The Client ID", default=False)

    def handle(self, *args, **options):

        if not Application.objects.filter(client_id=options['client_id']).exists():
            Application.objects.create(name="Client",
                                      user_id=1,
                                      client_type="public",
                                      redirect_uris=options['redirect'],
                                    client_id= options['client_id'],
                                 client_secret= options['client_secret'],
                                authorization_grant_type=AUTHORIZATION_TYPE)
            print("Application created")
        else:
            app = Application.objects.get(client_id= options['client_id'])
            app.redirect_uris = options['redirect']
            app.client_id= options['client_id']
            app.client_type="public"
            app.redirect_uris=options['redirect']
            app.client_secret= options['client_secret']
            app.authorization_grant_type=AUTHORIZATION_TYPE
            app.save()
            print("Application already exsisted. Updating")