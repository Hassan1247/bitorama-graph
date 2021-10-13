import graphene
from graphql import GraphQLError
import randomname

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
        post = graphene.ID(required=True)
        like = graphene.Boolean(required=True)

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
        comment = graphene.ID(required=True)
        like = graphene.Boolean(required=True)

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


class ConversationInput(graphene.InputObjectType):
    username = graphene.String()
    subject = graphene.String()


class CreateConversation(graphene.Mutation):
    class Arguments:
        # Mutation to create a Conversation
        input = ConversationInput(required=True)

    # Class attributes define the response of the mutation
    conversation = graphene.Field(ConversationType)

    @classmethod
    def mutate(cls, root, info, input):
        conversation = Conversation()
        conversation.username_guest = input.username
        conversation.subject = input.subject
        password = ''
        while(True):
            password = randomname.get_name(adj=(
                'speed', 'shape', 'sound', 'physics',  'corporate_prefixes', 'complexity', 'colors', 'algorithms', 'geometry', 'materials',  'music_theory', 'emotions', 'character',
            ), noun=(
                'typography', 'spirits', 'chemistry', 'seasonings', 'gaming',  'wine', 'music_production', 'sports',  'physics', 'physics_waves',  'web_development', 'physics_units', 'astronomy', 'startups', 'algorithms', 'geometry', 'set_theory', 'ghosts',  'music_instruments', 'filmmaking', 'music_theory', 'linear_algebra',  'coding',  'machine_learning', 'data_structures',
            ))
            chat = Conversation.objects.filter(password=password)
            if not chat:
                break
        conversation.password = password
        conversation.save()

        return CreateConversation(conversation=conversation)


class SendMessage(graphene.Mutation):
    class Arguments:
        # Mutation to Send message to a conversation
        password = graphene.String(required=True)
        text = graphene.String(required=True)

    # Class attributes define the response of the mutation
    output = graphene.String()

    @classmethod
    def mutate(cls, root, info, password, text):
        try:
            conversation = Conversation.objects.get(password=password)
        except:
            raise GraphQLError('Conversation not found')
        message = Message()
        message.username = conversation.username_guest
        message.text = text
        message.conversation = conversation
        message.save()
        output = 'OK'
        return SendMessage(output)


class Mutation(graphene.ObjectType):
    create_suggestion = CreateSuggestion.Field()
    create_comment = CreateComment.Field()
    like_post = LikePost.Field()
    like_comment = LikeComment.Field()
    create_conversation = CreateConversation.Field()
    send_message = SendMessage.Field()
