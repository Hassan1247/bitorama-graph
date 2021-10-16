from graphene_django import DjangoObjectType
from graphene import Node, Int
from graphene_django.filter import DjangoFilterConnectionField
from django_filters import FilterSet, OrderingFilter, CharFilter

from bitorama.models import *


class CategoryFilter(FilterSet):
    title = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['title']
        order_by = OrderingFilter(
            fields=(
                ('number_of_posts'),
            )
        )


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (Node, )
        fields = "__all__"
        filterset_class = CategoryFilter

    number_of_posts = Int()

    def resolve_number_of_posts(self, info):
        return self.post_set.count()


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

    number_of_comments = Int()

    def resolve_number_of_comments(self, info):
        return self.comment_set.filter(verified=True).count()


class InfoType(DjangoObjectType):
    class Meta:
        model = Info
        fields = "__all__"


class SuggestionType(DjangoObjectType):
    class Meta:
        model = Suggestion
        fields = "__all__"


class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = "__all__"


class ConversationType(DjangoObjectType):
    class Meta:
        model = Conversation
        fields = "__all__"
        messages = {"messages": {"type": "MessageType"}}
