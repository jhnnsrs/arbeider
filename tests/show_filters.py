import os
import sys
import django


def main():
    from filters.models import Filter
    nodes = Filter.objects.all()
    
    print("###### ALL ######")
    for node in nodes:
        print(node.id,node)




if __name__ == "__main__":
    
    sys.path.insert(0, '/bergen')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbeid.settings")
    django.setup()

    main()