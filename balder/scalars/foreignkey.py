
import graphene
from graphql.language.ast import IntValue, StringValue


class ForeignKey(graphene.ID):
    queryset = None

    def __init__(self, queryset = None, *args, **kwargs):
        self.queryset = queryset
        super().__init__(*args, **kwargs)

    def serialize(self, model):
        return str(model.id)

    @classmethod
    def parse_value(cls, value):
        return cls.queryset.get(id=value)

    @classmethod
    def parse_literal(cls, ast):
        if isinstance(ast, (StringValue, IntValue)):
            return cls.queryset.get(id=ast.value)
