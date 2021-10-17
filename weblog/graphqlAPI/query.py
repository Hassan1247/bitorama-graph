import graphene
from graphql import GraphQLError
from graphene_django.filter import DjangoFilterConnectionField
from graphene.utils.str_converters import to_snake_case

from .schema import *


class OrderedDjangoFilterConnectionField(DjangoFilterConnectionField):

    @classmethod
    def resolve_queryset(
        cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(data=filter_kwargs,
                             queryset=qs, request=info.context).qs

        order = args.get('orderBy', None)
        if order:
            if type(order) is str:
                snake_order = to_snake_case(order)
            else:
                snake_order = [to_snake_case(o) for o in order]
            qs = qs.order_by(*snake_order)
        return qs


class Sort(graphene.Enum):
    ASC = 1
    DESC = -1


class PaginationInput(graphene.InputObjectType):
    offset = graphene.Int()
    limit = graphene.Int()


class InfoFilterInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    text = graphene.String()
    date_from = graphene.String()
    date_to = graphene.String()


class InfoSortInput(graphene.InputObjectType):
    title = Sort()
    date_created = Sort()


class PostFilterInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    description = graphene.String()
    post = graphene.String()
    category = graphene.String()
    date_from = graphene.String()
    date_to = graphene.String()


class PostSortInput(graphene.InputObjectType):
    title = Sort()
    number_of_views = Sort()
    number_of_likes = Sort()
    number_of_comments = Sort()
    date_created = Sort()


class Query(graphene.ObjectType):
    category = graphene.Node.Field(CategoryNode)
    categories = OrderedDjangoFilterConnectionField(CategoryNode,
                                                    orderBy=graphene.List(of_type=graphene.String))

    post = graphene.Node.Field(PostNode)
    posts = OrderedDjangoFilterConnectionField(PostNode,
                                               orderBy=graphene.List(of_type=graphene.String))

    infos = graphene.List(InfoType, filter=graphene.Argument(
        InfoFilterInput), sort=graphene.Argument(InfoSortInput), pagination=graphene.Argument(PaginationInput))
    conversation = graphene.Field(
        ConversationType, password=graphene.String(required=True))

    def resolve_infos(root, info, filter=None, sort=None, pagination=PaginationInput()):
        if type(pagination.offset) != int:
            pagination.offset = 0
        if type(pagination.limit) != int:
            pagination.limit = 100
        if filter:
            if filter.id:
                return Info.objects.filter(pk=filter.id)[pagination.offset:pagination.limit+pagination.offset]
            elif filter.title:
                return Info.objects.filter(title__contains=filter.title)[pagination.offset:pagination.limit+pagination.offset]
            elif filter.text:
                return Info.objects.filter(text__contains=filter.text)[pagination.offset:pagination.limit+pagination.offset]
            elif filter.date_from and filter.date_to:
                return Info.objects.filter(date_created__gt=filter.date_from, date_created__lt=input.date_to)[pagination.offset:pagination.limit+pagination.offset]
        if sort:
            if sort.title:
                if sort.title == 1:
                    return Info.objects.all().order_by('title')[pagination.offset:pagination.limit+pagination.offset]
                else:
                    return Info.objects.all().order_by('-title')[pagination.offset:pagination.limit+pagination.offset]
            if sort.date_created:
                if sort.date_created == 1:
                    return Info.objects.all().order_by('date_created')[pagination.offset:pagination.limit+pagination.offset]
                else:
                    return Info.objects.all().order_by('-date_created')[pagination.offset:pagination.limit+pagination.offset]
        return Info.objects.all()[pagination.offset:pagination.limit+pagination.offset]

    def resolve_conversation(root, info, password):
        try:
            return Conversation.objects.get(password=password)
        except:
            raise GraphQLError('Password is not correct!')

    # def resolve_posts(self, info, **kwargs):
    #     print('hi')
    #     # post.number_of_views += 1
    #     # post.save()
    #     return PostFilter(kwargs).qs

    # def resolve_categories(self, info, **kwargs):
    #     return CategoryFilter(kwargs).qs.order_by('-number_of_posts')
