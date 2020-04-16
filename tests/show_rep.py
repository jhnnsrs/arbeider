import os
import sys
import django


def main():
    from elements.models import Representation, Sample
    rep = Representation.objects.first()
    print(rep.array)



if __name__ == "__main__":
    
    sys.path.insert(0, '/bergen')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbeid.settings")
    django.setup()

    main()