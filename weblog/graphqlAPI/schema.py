from graphene_django import DjangoObjectType
from graphene import Node, Int
from graphene_django.filter import DjangoFilterConnectionField
from django_filters import FilterSet, OrderingFilter, CharFilter, DateFilter
from django.db.models import Count

from bitorama.models import *


class CategoryFilter(FilterSet):
    title = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['title']


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (Node, )
        fields = "__all__"
        filterset_class = CategoryFilter

    number_of_posts = Int()

    def resolve_number_of_posts(self, info):
        return self.post_set.count()

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.annotate(number_of_posts=Count('post')).order_by('-number_of_posts')


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = "__all__"

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(verified=True)


class PostFilter(FilterSet):
    title = CharFilter(lookup_expr='icontains')
    description = CharFilter(lookup_expr='icontains')
    post = CharFilter(lookup_expr='icontains')
    author = CharFilter(lookup_expr='icontains')
    # categories = CharFilter(lookup_expr='icontains')
    date_from = DateFilter('date_created', lookup_expr='gte')
    date_to = DateFilter('date_created', lookup_expr='lte')

    class Meta:
        model = Category
        fields = ['title', 'description', 'post',
                  'author']


class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        interfaces = (Node, )
        fields = "__all__"
        filterset_class = PostFilter
        comments = {"comments": {"type": "CommentType"}}

    number_of_comments = Int()

    def resolve_number_of_comments(self, info):
        return self.comment_set.filter(verified=True).count()

    @classmethod
    def get_node(cls, info, id):
        post = Post.objects.get(id=id)
        post.number_of_views += 1
        post.save()
        return post


class InfoFilter(FilterSet):
    title = CharFilter(lookup_expr='icontains')
    text = CharFilter(lookup_expr='icontains')
    date_from = DateFilter('date_created', lookup_expr='gte')
    date_to = DateFilter('date_created', lookup_expr='lte')

    class Meta:
        model = Category
        fields = ['title', 'text', ]


class InfoNode(DjangoObjectType):
    class Meta:
        model = Info
        interfaces = (Node, )
        fields = "__all__"
        filterset_class = InfoFilter


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
