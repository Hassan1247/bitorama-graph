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


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = "__all__"


class InfoType(DjangoObjectType):
    class Meta:
        model = Info
        fields = "__all__"


class SuggestionType(DjangoObjectType):
    class Meta:
        model = Suggestion
        fields = "__all__"
