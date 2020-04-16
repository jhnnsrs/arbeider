import os
import sys
import django


def main():
    from delt.models import Node, BackendNode, FrontendNode
    nodes = Node.objects.all()
    
    print("###### ALL ######")
    for node in nodes:
        print(node.id,node)

    nodes = BackendNode.objects.all()
    print("###### BACKEND ######")
    for node in nodes:
        print(node.id,node)

    nodes = FrontendNode.objects.all()
    print("###### FRONTEND ######")
    for node in nodes:
        print(node.id,node)



if __name__ == "__main__":
    
    sys.path.insert(0, '/bergen')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbeid.settings")
    django.setup()

    main()