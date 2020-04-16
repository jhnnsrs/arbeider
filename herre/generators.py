import random
import string
from django.db import models

class ArnheimNameGenerator(object):
    group = None

    def __init__(self, instance: models.Model, group = None, overwrite = None, **kwargs):
        self.instance = instance
        self.group = group
        self.overwrite = overwrite if overwrite is not None else True #TODO: Set this from settings or storage?
        self._name = None
        self.kwargs = kwargs

        if self.group is None:
            raise NotImplementedError("Please specify a group")


    def _id_generator(self, size=6, chars= string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def build_name(self, **kwargs):
        return "test"

    @property
    def name(self):
        if self._name is None:
            if self.overwrite:
                self._name =  self.build_name(**self.kwargs)
            else:
                self._name =  self.build_name(**self.kwargs) + self._id_generator()
        return self._name

    @property
    def path(self):
        return f'{self.instance.sample.id}-sample.{self.group}.{self.name}'


