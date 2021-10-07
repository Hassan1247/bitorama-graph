from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=512)
    picture = models.FileField()
    post = models.TextField()
    author = models.CharField(max_length=256, default='Hassan Moosaabadi')
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
    picture = models.FileField()

    def __str__(self):
        return self.picture
