from django.contrib import admin
from .models import Questions, Comment, Answers, AnswersComment,QVote,AVote
from django.db import models


# Register your models here.


@admin.register(Questions)
class authorAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'slug', 'author')
    list_filter = ('author',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Comment)
admin.site.register(Answers)
admin.site.register(AnswersComment)
admin.site.register(QVote)
admin.site.register(AVote)
