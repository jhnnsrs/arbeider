from django.db.models.manager import Manager
from django.db.models.query import QuerySet


class PodQuerySet(QuerySet):
    pass




class PodManager(Manager):
    queryset = None

    def get_queryset(self):
        if self.queryset is not None: return self.queryset(self.model, using=self._db)
        return PodQuerySet(self.model, using=self._db)

    def accessible(self, creator):

        #TODO: Implement correctly
        calculatated_policy = r'.*'




        return self.get_queryset().filter(policy__iregex=calculatated_policy)


        



