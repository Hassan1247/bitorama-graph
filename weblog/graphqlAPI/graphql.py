from graphene import Schema

from .query import Query
from .mutation import Mutation

schema = Schema(query=Query, mutation=Mutation)
