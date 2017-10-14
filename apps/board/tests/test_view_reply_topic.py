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
            'reply_topic',
            kwargs={'pk': self.board.pk, 'board_pk': self.topic.pk}
        )


class LoginRequiredReplyTopicTests(ReplayTopicTestCase):
    pass


class ReplyTopicTests(ReplayTopicTestCase):
    pass


class SuccessfulReplyTopicTests(ReplayTopicTestCase):
    pass


class InvalidReplyTopicTests(ReplayTopicTestCase):
    pass
