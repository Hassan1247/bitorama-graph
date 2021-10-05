from django.contrib import admin

from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'date_created']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'text', 'username', 'verified', 'date_created']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'date_created']


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ['username', 'subject', 'email', 'date_created']
