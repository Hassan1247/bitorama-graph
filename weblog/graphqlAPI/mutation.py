import graphene

from .schema import *
from bitorama.models import *


class SuggestionInput(graphene.InputObjectType):
    username = graphene.String()
    subject = graphene.String()
    text = graphene.String()
    email = graphene.String()


class CreateSuggestion(graphene.Mutation):
    class Arguments:
        # Mutation to create a Suggestion
        input = SuggestionInput(required=True)

    # Class attributes define the response of the mutation
    suggestion = graphene.Field(SuggestionType)

    @classmethod
    def mutate(cls, root, info, input):
        suggestion = Suggestion()
        suggestion.username = input.username
        suggestion.subject = input.subject
        suggestion.text = input.text
        suggestion.email = input.email
        suggestion.save()

        return CreateSuggestion(suggestion=suggestion)


# class BookInput(graphene.InputObjectType):
#     title = graphene.String()
#     author = graphene.String()
#     pages = graphene.Int()
#     price = graphene.Int()
#     quantity = graphene.Int()
#     description = graphene.String()
#     status = graphene.String()


# class CreateBook(graphene.Mutation):
#     class Arguments:
#         input = BookInput(required=True)

#     book = graphene.Field(BookType)

#     @classmethod
#     def mutate(cls, root, info, input):
#         book = Book()
#         book.title = input.title
#         book.author = input.author
#         book.pages = input.pages
#         book.price = input.price
#         book.quantity = input.quantity
#         book.description = input.description
#         book.status = input.status
#         book.save()
#         return CreateBook(book=book)


class Mutation(graphene.ObjectType):
    create_suggestion = CreateSuggestion.Field()
