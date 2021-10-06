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


class LikePost(graphene.Mutation):
    class Arguments:
        # Mutation to Like or Dislike a post
        post = graphene.ID()
        like = graphene.Boolean()

    # Class attributes define the response of the mutation
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, post, like):
        try:
            post_from_db = Post.objects.get(pk=post)
        except:
            raise GraphQLError('Post id not found')
        if like:
            post_from_db.number_of_likes += 1
        else:
            post_from_db.number_of_likes -= 1
        post_from_db.save()
        message = str(like)
        return LikePost(message)


class LikeComment(graphene.Mutation):
    class Arguments:
        # Mutation to Like or Dislike a comment
        comment = graphene.ID()
        like = graphene.Boolean()

    # Class attributes define the response of the mutation
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, comment, like):
        try:
            comment_from_db = Comment.objects.get(pk=comment, verified=True)
        except:
            raise GraphQLError('Comment id not found')
        if like:
            comment_from_db.number_of_likes += 1
        else:
            comment_from_db.number_of_likes -= 1
        comment_from_db.save()
        message = str(like)
        return LikeComment(message)


class Mutation(graphene.ObjectType):
    create_suggestion = CreateSuggestion.Field()
    create_comment = CreateComment.Field()
    like_post = LikePost.Field()
    like_comment = LikeComment.Field()
