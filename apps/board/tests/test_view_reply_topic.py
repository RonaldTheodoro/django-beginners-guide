import unittest

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .. import models, views


class ReplayTopicTestCase(TestCase):

    def setUp(self):
        self.username = 'ronald'
        self.password = 'asdf1234'
        user = User.objects.create_user(
            username=self.username,
            email='ronald@theodoro.com',
            password=self.password
        )
        self.board = models.Board.objects.create(
            name='Django',
            description='Django Board.'
        )
        self.topic = models.Topic.objects.create(
            subject='Hello World',
            board=self.board,
            starter=user
        )
        models.Post.objects.create(
            message='Lorem ipsum dolor sit amet',
            topic=self.topic,
            created_by=user
        )
        self.url = reverse(
            'topic_posts',
            kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk}
        )


class LoginRequiredReplyTopicTests(ReplayTopicTestCase):
    pass


class ReplyTopicTests(ReplayTopicTestCase):
    pass


class SuccessfulReplyTopicTests(ReplayTopicTestCase):

    @unittest.skip
    def test_redirection(self):
        url = reverse(
            'topic_posts',
            kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk}
        )
        topic_post_url = f'{url}?page=1#2'
        self.response = self.client.get(url)
        self.assertRedirects(self.response, topic_post_url)


class InvalidReplyTopicTests(ReplayTopicTestCase):
    pass
