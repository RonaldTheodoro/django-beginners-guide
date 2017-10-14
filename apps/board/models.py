from django.contrib.auth.models import User
from django.db import models
from django.utils.text import Truncator


class Board(models.Model):
    name = models.CharField('name', max_length=30, unique=True)
    description = models.CharField('description', max_length=100)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(
            topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
    subject = models.CharField('subject', max_length=255)
    last_updated = models.DateTimeField('last update', auto_now_add=True)
    board = models.ForeignKey(
        'Board',
        verbose_name='board',
        related_name='topics'
    )
    starter = models.ForeignKey(
        User,
        verbose_name='starter',
        related_name='topics'
    )
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject


class Post(models.Model):
    message = models.TextField('message', max_length=4000)
    topic = models.ForeignKey(
        'Topic',
        verbose_name='topic',
        related_name='posts'
    )
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', null=True)
    created_by = models.ForeignKey(
        User,
        verbose_name='created by',
        related_name='posts'
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name='updated by',
        null=True,
        related_name='+'
    )

    def __str__(self):
        truncate_message = Truncator(self.message)
        return truncate_message.chars(30)
