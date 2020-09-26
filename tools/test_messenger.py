import os
import sys
import django


def main():
    from delt.models import Assignation
    from delt.messenger import packAssignation, unpackAssignation
    assignation = Assignation.objects.first()

    serialized = packAssignation(assignation)
    print(serialized)

    print(unpackAssignation(serialized))





if __name__ == "__main__":
    
    sys.path.insert(0, '/bergen')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbeid.settings")
    django.setup()

    main()