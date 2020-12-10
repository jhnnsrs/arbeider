from delt.models import Template
from django.db import models
from flow.models import Compiler, ExecutionGraph
# Create your models here.


class SkilleCompiler(Compiler):
    pass

class SkilleGraph(ExecutionGraph):
    pass

class SkilleTemplate(Template):
    skill_identifier = models.CharField(max_length=100)