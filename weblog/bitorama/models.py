from django.db import models

DEFAULT_USERNAME = 'Hassan Moosaabadi'


class Post(models.Model):
    title = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=512)
    picture = models.FileField()
    post = models.TextField()
    author = models.CharField(max_length=256, default=DEFAULT_USERNAME)
    categories = models.ManyToManyField('Category', blank=True)
    number_of_views = models.PositiveIntegerField(default=0)
    number_of_likes = models.PositiveIntegerField(default=0)
    number_of_comments = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title


class Comment(models.Model):
    username = models.CharField(max_length=256)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    verified = models.BooleanField(default=False)
    number_of_likes = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.text


class Category(models.Model):
    title = models.CharField(max_length=256, unique=True, db_index=True)
    number_of_posts = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Info(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Suggestion(models.Model):
    username = models.CharField(max_length=256)
    subject = models.CharField(max_length=256)
    text = models.TextField()
    email = models.EmailField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Picture(models.Model):
    picture = models.FileField(unique=True, db_index=True)

    def __str__(self):
        return self.picture.name


class Conversation(models.Model):
    username_guest = models.CharField(max_length=256)
    username_host = models.CharField(
        max_length=256, default=DEFAULT_USERNAME)
    subject = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    messages = models.ManyToManyField('Message', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Message(models.Model):
    username = models.CharField(max_length=256)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.text
