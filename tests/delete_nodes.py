import os
import sys
import django


def main():
    from delt.models import Node
    
    Node.objects.all().delete()


if __name__ == "__main__":
    
    sys.path.insert(0, '/bergen')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbeid.settings")
    django.setup()

    main()