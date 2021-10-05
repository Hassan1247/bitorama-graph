import graphene
from graphene_django import DjangoObjectType
from bitorama.models import *


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'title', 'number_of_posts')


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'description',
            'picture',
            'post',
            'author',
            'categories',
            'number_of_views',
            'number_of_likes',
            'number_of_comments',
            'date_created',
        )


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = (
            'id',
            'username',
            'post',
            'text',
            'verified',
            'number_of_views',
            'number_of_likes',
            'date_created',
        )


class InfoType(DjangoObjectType):
    class Meta:
        model = Info
        fields = (
            'id',
            'title',
            'text',
            'date_created',
        )


class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType)
    posts = graphene.List(PostType)
    comments = graphene.List(CommentType)
    infos = graphene.List(InfoType)

    def resolve_categories(root, info, **kwargs):
        # Querying a list
        return Category.objects.all()

    def resolve_posts(root, info, **kwargs):
        # Querying a list
        return Post.objects.all()

    def resolve_comments(root, info, **kwargs):
        # Querying a list
        return Comment.objects.all()

    def resolve_infos(root, info, **kwargs):
        # Querying a list
        return Info.objects.all()


schema = graphene.Schema(query=Query)
