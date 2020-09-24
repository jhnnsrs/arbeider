import os
import sys
import django


def main():
    from delt.models import Node, Pod, Route
    
    Node.objects.all().delete()
    Pod.objects.all().delete()
    Route.objects.all().delete()


if __name__ == "__main__":
    
    sys.path.insert(0, '/bergen')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbeid.settings")
    django.setup()

    main()