import graphene
from graphql import GraphQLError

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


class CommentInput(graphene.InputObjectType):
    post = graphene.ID()
    username = graphene.String()
    text = graphene.String()


class CreateComment(graphene.Mutation):
    class Arguments:
        input = CommentInput(required=True)

    comment = graphene.Field(CommentType)

    @classmethod
    def mutate(cls, root, info, input):
        comment = Comment()
        try:
            post = Post.objects.get(pk=input.post)
        except:
            raise GraphQLError('Post id not found')
        comment.post = post
        comment.username = input.username
        comment.text = input.text
        comment.save()
        return CreateComment(comment=comment)


class Mutation(graphene.ObjectType):
    create_suggestion = CreateSuggestion.Field()
    create_comment = CreateComment.Field()
