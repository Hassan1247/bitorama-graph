import graphene

from .schema import *


class CategoryInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()


class InfoInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    text = graphene.String()
    date_from = graphene.String()
    date_to = graphene.String()


class Query(graphene.ObjectType):
    categories = graphene.List(
        CategoryType, input=graphene.Argument(CategoryInput))
    posts = graphene.List(PostType)
    infos = graphene.List(InfoType, input=graphene.Argument(InfoInput))

    def resolve_categories(root, info, input=None):
        if input:
            if input.id:
                return Category.objects.filter(pk=input.id)
            elif input.title:
                return Category.objects.filter(title__contains=input.title)
        return Category.objects.all()

    def resolve_posts(root, info, **kwargs):
        return Post.objects.all()

    def resolve_infos(root, info, input=None):
        if input:
            if input.id:
                return Info.objects.filter(pk=input.id)
            elif input.title:
                return Info.objects.filter(title__contains=input.title)
            elif input.text:
                return Info.objects.filter(text__contains=input.text)
            elif input.date_from and input.date_to:
                return Info.objects.filter(date_created__gt=input.date_from, date_created__lt=input.date_to)
        return Info.objects.all()
