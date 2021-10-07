import os
import shutil
from django.core.management import BaseCommand
from django.core.files.base import File

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

        print("\nLoading Posts available in ./posts/ ...", flush=True)
        set_of_files = set(os.listdir(folder))
        posts = set()
        for item in set_of_files:
            name, extension = os.path.splitext(item)
            if extension == '.post':
                posts.add(name)
        i = 1
        for post in posts:
            import_post(folder, post, str(i))
            i += 1
        print('Done.', flush=True)

        print("\nLoading Pictures available in ./posts/ ...", flush=True)
        pictures = set()
        for item in set_of_files:
            name, extension = os.path.splitext(item)
            if name not in posts:
                pictures.add(item)
        i = 1
        for picture in pictures:
            try:
                Picture.objects.get(picture=picture)
            except:
                pic = Picture()
                f = open(folder + picture, 'rb')
                name, extension = os.path.splitext(f.name)
                pic.picture.save(picture, File(f))
                f.close()
                pic.save()
            print(str(i) + '.\'' + picture + '\' OK', flush=True)
            i += 1
        print('Done.', flush=True)


def import_post(folder, title, i):
    with open(folder + title + '.post', 'r') as my_file:
        lines = my_file.readlines()
    for line in range(len(lines)):
        lines[line] = lines[line].strip()

    title_index = lines.index('[TITLE]:')
    description_index = lines.index('[DESCRIPTION]:')
    picture_index = lines.index('[PICTURE]:')
    post_index = lines.index('[POST]:')
    author_index = lines.index('[AUTHOR]:')
    categories_index = lines.index('[CATEGORIES]:')
    nov_index = lines.index('[NUMBER_OF_VIEWS]:')
    nol_index = lines.index('[NUMBER_OF_LIKES]:')
    noc_index = lines.index('[NUMBER_OF_COMMENTS]:')
    date_index = lines.index('[DATE_CREATED]:')

    title = '\n'.join(lines[title_index+1:description_index])
    description = '\n'.join(lines[description_index+1:picture_index])
    picture = lines[picture_index+1]
    post = '\n'.join(lines[post_index+1:author_index])
    author = '\n'.join(lines[author_index+1:categories_index])
    categories = lines[categories_index+1]
    number_of_views = lines[nov_index+1]
    number_of_likes = lines[nol_index+1]
    number_of_comments = lines[noc_index+1]
    date_created = lines[date_index+1]

    # import categories
    categories = categories.split(',')
    for item in categories:
        try:
            Category.objects.get(title=item)
        except:
            category = Category()
            category.title = item
            category.save()
    # import posts
    try:
        Post.objects.get(title=title)
    except:
        new_post = Post()
        new_post.title = title
        new_post.description = description
        f = open(folder + picture, 'rb')
        name, extension = os.path.splitext(f.name)
        new_post.picture.save(picture, File(f))
        f.close()
        new_post.post = post
        new_post.author = author
        new_post.number_of_views = number_of_views
        new_post.number_of_likes = number_of_likes
        new_post.number_of_comments = number_of_comments
        new_post.date_created = date_created
        new_post.save()
        for item in categories:
            new_post.categories.add(Category.objects.get(title=item))
    print(i + '.\'%s.post\'' % (title) + ' OK', flush=True)
