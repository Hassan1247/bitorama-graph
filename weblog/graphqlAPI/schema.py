import graphene
from graphene_django import DjangoObjectType

from bitorama.models import *


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = "__all__"

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(verified=True)


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = "__all__"
        comments = {"comments": {"type": "CommentType"}}


class InfoType(DjangoObjectType):
    class Meta:
        model = Info
        fields = "__all__"


class SuggestionType(DjangoObjectType):
    class Meta:
        model = Suggestion
        fields = "__all__"
