from django.core.management import BaseCommand
import os
import shutil

from bitorama.models import *


class Command(BaseCommand):
    # Show this when the user types help
    help = "Export Posts into files."

    def handle(self, *args, **options):
        print("This command will export all the posts in your database.")
        folder = './posts'
        if not os.path.exists(folder):
            os.mkdir(folder)

        posts = Post.objects.all()
        for post in posts:
            with open(folder + '/' + '%s.post' % (post.title), 'w') as my_file:
                print('[TITLE]:\n' + post.title, file=my_file)
                print('\n[DESCRIPTION]:\n' + post.description, file=my_file)
                print('\n[POST]:\n' + post.post, file=my_file)
                print('\n[AUTHOR]:\n' + post.author, file=my_file)
                print('\n[NUMBER_OF_VIEWS]:\n' +
                      str(post.number_of_views), file=my_file)
                print('\n[NUMBER_OF_LIKES]:\n' +
                      str(post.number_of_likes), file=my_file)
                print('\n[NUMBER_OF_COMMENTS]:\n' +
                      str(post.number_of_comments), file=my_file)
                print('\n[DATE_CREATED]:\n' +
                      str(post.date_created), file=my_file)
            name, extension = os.path.splitext(post.picture.name)
            shutil.copy2(post.picture.path, './posts/%s%s' %
                         (post.title, extension))
            print('%s.post' % (post.title), ' OK.')
        print('Done.')
