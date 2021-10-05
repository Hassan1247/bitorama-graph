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
