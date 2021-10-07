from django.core.management import BaseCommand
import os
import shutil

from bitorama.models import *


class Command(BaseCommand):
    # Show this when the user types help
    help = "Export Posts into files."

    def handle(self, *args, **options):
        print("This command will export all the posts in your database.")
        folder = './posts/'
        if not os.path.exists(folder):
            os.mkdir(folder)

        print("\nLoading Posts available in DataBase...", flush=True)
        posts = Post.objects.all()
        i = 1
        for post in posts:
            export_post(folder, post, str(i))
            i += 1
        print('Done.', flush=True)

        print("\nLoading Pictures available in DataBase...", flush=True)
        pictures = Picture.objects.all()
        i = 1
        for picture in pictures:
            shutil.copy2(picture.picture.path, folder + picture.picture.name)
            print(str(i) + '.\'' + picture.picture.name + '\' OK', flush=True)
            i += 1
        print('Done.', flush=True)


def export_post(folder, post, i):
    name, extension = os.path.splitext(post.picture.name)
    shutil.copy2(post.picture.path, folder + post.title + extension)
    with open(folder + post.title + '.post', 'w') as my_file:
        print('[TITLE]:\n' + post.title, file=my_file)
        print('[DESCRIPTION]:\n' + post.description, file=my_file)
        print('[PICTURE]:\n' + post.title + extension, file=my_file)
        print('[POST]:\n' + post.post, file=my_file)
        print('[AUTHOR]:\n' + post.author, file=my_file)
        list_of_categories = list(
            post.categories.values_list('title', flat=True))
        print('[CATEGORIES]:\n' + ','.join(list_of_categories), file=my_file)
        print('[NUMBER_OF_VIEWS]:\n' +
              str(post.number_of_views), file=my_file)
        print('[NUMBER_OF_LIKES]:\n' +
              str(post.number_of_likes), file=my_file)
        print('[NUMBER_OF_COMMENTS]:\n' +
              str(post.number_of_comments), file=my_file)
        print('[DATE_CREATED]:\n' + str(post.date_created), file=my_file)
    print(i + '.\'%s.post\'' % (post.title) + ' OK', flush=True)
