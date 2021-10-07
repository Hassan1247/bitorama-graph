from django.core.management import BaseCommand
import os
import shutil

from bitorama.models import *


class Command(BaseCommand):
    # Show this when the user types help
    help = "Import Posts into DataBase."

    def handle(self, *args, **options):
        print("This command will import all the posts in your ./posts/")
        folder = './posts/'
        if not os.path.exists(folder):
            print('No posts found!')
            return
        print("Loading data models available in ./posts/ ...", flush=True)

        set_of_posts = set(sorted(os.listdir(folder)))
        print(set_of_posts)
        # for

        # i = 1
        # for post in posts:
        #     import_post(folder, post, str(i))
        #     i += 1
        print('Done.')


def import_post(folder, post):
    pass
    # with open(folder + post.title + '.post', 'w') as my_file:
    #     print('[TITLE]:\n' + post.title, file=my_file)
    #     print('\n[DESCRIPTION]:\n' + post.description, file=my_file)
    #     print('\n[POST]:\n' + post.post, file=my_file)
    #     print('\n[AUTHOR]:\n' + post.author, file=my_file)
    #     lis_of_categories = list(
    #         post.categories.values_list('title', flat=True))
    #     print('\n[CATEGORIES]:\n' + ','.join(lis_of_categories), file=my_file)
    #     print('\n[NUMBER_OF_VIEWS]:\n' +
    #           str(post.number_of_views), file=my_file)
    #     print('\n[NUMBER_OF_LIKES]:\n' +
    #           str(post.number_of_likes), file=my_file)
    #     print('\n[NUMBER_OF_COMMENTS]:\n' +
    #           str(post.number_of_comments), file=my_file)
    #     print('\n[DATE_CREATED]:\n' + str(post.date_created), file=my_file)
    # name, extension = os.path.splitext(post.picture.name)
    # shutil.copy2(post.picture.path, folder + post.title + extension)
    # print('%s.post' % (post.title), ' OK.')
