import graphene

from .schema import *


class Sort(graphene.Enum):
    ASC = 1
    DESC = -1


class CategoryFilterInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()


class CategorySortInput(graphene.InputObjectType):
    title = Sort()
    number_of_posts = Sort()


class InfoFilterInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    text = graphene.String()
    date_from = graphene.String()
    date_to = graphene.String()


class PostFilterInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    description = graphene.String()
    post = graphene.String()
    category = graphene.String()
    date_from = graphene.String()
    date_to = graphene.String()


class Query(graphene.ObjectType):
    categories = graphene.List(
        CategoryType, filter=graphene.Argument(CategoryFilterInput), sort=graphene.Argument(CategorySortInput))
    posts = graphene.List(PostType, filter=graphene.Argument(PostFilterInput))
    infos = graphene.List(InfoType, filter=graphene.Argument(InfoFilterInput))

    def resolve_categories(root, info, filter=None, sort=None):
        if filter:
            if filter.id:
                return Category.objects.filter(pk=filter.id)
            elif filter.title:
                return Category.objects.filter(title__contains=filter.title)
        if sort:
            if sort.title:
                if sort.title == 1:
                    return Category.objects.all().order_by('title')
                else:
                    return Category.objects.all().order_by('-title')
            if sort.number_of_posts:
                if sort.number_of_posts == 1:
                    return Category.objects.all().order_by('number_of_posts')
                else:
                    return Category.objects.all().order_by('-number_of_posts')
        return Category.objects.all()

    def resolve_posts(root, info, filter=None):
        if filter:
            if filter.id:
                return Post.objects.filter(pk=filter.id)
            elif filter.title:
                return Post.objects.filter(title__contains=filter.title)
            elif filter.description:
                return Post.objects.filter(description__contains=filter.description)
            elif filter.post:
                return Post.objects.filter(post__contains=filter.post)
            elif filter.category:
                return Post.objects.filter(categories__title__contains=filter.category)
            elif filter.date_from and filter.date_to:
                return Post.objects.filter(date_created__gt=filter.date_from, date_created__lt=filter.date_to)
        return Post.objects.all()

    def resolve_infos(root, info, filter=None):
        if filter:
            if filter.id:
                return Info.objects.filter(pk=filter.id)
            elif filter.title:
                return Info.objects.filter(title__contains=filter.title)
            elif filter.text:
                return Info.objects.filter(text__contains=filter.text)
            elif filter.date_from and filter.date_to:
                return Info.objects.filter(date_created__gt=filter.date_from, date_created__lt=input.date_to)
        return Info.objects.all()
