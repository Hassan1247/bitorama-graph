import graphene

from .schema import *


class CategoryInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()


class Query(graphene.ObjectType):
    categories = graphene.List(
        CategoryType, input=graphene.Argument(CategoryInput))
    posts = graphene.List(PostType)
    comments = graphene.List(CommentType)
    infos = graphene.List(InfoType)

    def resolve_categories(root, info, input=None):
        if input:
            if input.id:
                return Category.objects.filter(pk=input.id)
            elif input.title:
                return Category.objects.filter(title__contains=input.title)
        return Category.objects.all()

    def resolve_posts(root, info, **kwargs):
        # Querying a list
        return Post.objects.all()

    def resolve_comments(root, info, **kwargs):
        # Querying a list
        return Comment.objects.filter(verified=True)

    def resolve_infos(root, info, **kwargs):
        # Querying a list
        return Info.objects.all()
