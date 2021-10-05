import graphene

from .schema import *


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
