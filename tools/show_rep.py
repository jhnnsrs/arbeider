import os
import sys
import django


def main():
    from elements.models import Representation, Sample
    rep = Representation.objects.first()
    import matrise.extenders
    print(rep.array.biometa.planes.compute().to_dict(orient="records"))



if __name__ == "__main__":
    
    sys.path.insert(0, '/bergen')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbeid.settings")
    django.setup()

    main()