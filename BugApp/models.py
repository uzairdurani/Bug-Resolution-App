from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinLengthValidator
from taggit.managers import TaggableManager
from django_quill.fields import QuillField


# Create your models here.


class Questions(models.Model):
    title = models.CharField(max_length=150, blank=False,)
    body = QuillField(blank=False)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    thumbsup = models.IntegerField(default='0')
    thumbsdown = models.IntegerField(default='0')
    thumbs = models.ManyToManyField(
        User, related_name='Qthumbs', default=None, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    views_count = models.BigIntegerField(default='0')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='questions_user')
    tags = TaggableManager()
    like_count = models.BigIntegerField(default='0')

    def get_absolute_url(self):
        return reverse("BugApp:single_question", args=[self.slug])

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ('-publish',)


class Answers(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='questions')
    question = models.ForeignKey(
        Questions, on_delete=models.CASCADE, related_name='question_answer')

    body = QuillField(blank=False)
    thumbsup = models.IntegerField(default='0')
    thumbsdown = models.IntegerField(default='0')
    thumbs = models.ManyToManyField(
        User, related_name='Athumbs', default=None, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    like_count = models.BigIntegerField(default='0')

    class Meta:
        ordering = ['publish']

    def __str__(self) -> str:
        return f'Question : {self.question.id}'


class Comment(models.Model):
    author = models.ForeignKey(
        User, related_name='author', on_delete=models.CASCADE, default=None, blank=False)
    question = models.ForeignKey(
        Questions, on_delete=models.CASCADE, related_name='question_comment')
    content = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-publish']


class AnswersComment(models.Model):
    author = models.ForeignKey(
        User, related_name='answer_author', on_delete=models.CASCADE, default=None, blank=False)
    answers = models.ForeignKey(
        Answers, on_delete=models.CASCADE, related_name='answers_comment')
    content = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-publish']

    def __str__(self) -> str:
        return f'answer : {self.answers.id}'


class QVote(models.Model):
    question = models.ForeignKey(Questions, related_name='questionid',
                                 on_delete=models.CASCADE, default=None, blank=False)

    user = models.ForeignKey(User, related_name='userid',
                             on_delete=models.CASCADE, default=None, blank=False)
    vote = models.BooleanField(default=True)


class AVote(models.Model):
    answer = models.ForeignKey(Answers, related_name='answerid',
                               on_delete=models.CASCADE, default=None, blank=False)
    user = models.ForeignKey(User, related_name='userid2',
                             on_delete=models.CASCADE, default=None, blank=False)
    vote = models.BooleanField(default=True)


class QuestionView(models.Model):
    question = models.ForeignKey(
        Questions, related_name='questionviews',  on_delete=models.CASCADE)
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now())
