from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .. import models, views


class PostUpdateViewTestCase(TestCase):

    def setUp(self):
        self.board = models.Board.objects.create(
            name='Django',
            description='Django board',
        )
        self.username = 'ronald'
        self.password = 'asdf1234'
        user = User.objects.create_user(
            username=self.username,
            email='ronald@theodoro.com',
            password=self.password
        )
        self.topic = models.Topic.objects.create(
            subject='Hello World',
            board=self.board,
            starter=user
        )
        self.post = models.Post.objects.create(
            message='Lorem ipsum dolor sit amet',
            topic=self.topic,
            created_by=user
        )
        self.url = reverse(
            'edit_posts',
            kwargs={
                'pk': self.board.pk,
                'topic_pk': self.topic.pk,
                'post_pk': self.post.pk
            }
        )


class LoginRequiredPostUpdateViewTests(PostUpdateViewTestCase):
    
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class UnauthorizedPostUpdateViewTests(PostUpdateViewTestCase):
    
    def setUp(self):
        super().setUp()
        username = 'ximira'
        password = 'xelo4569'
        user = User.objects.create_user(
            username=username,
            email='ximira@xelo.com',
            password=password
        )
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 404)


class PostUpdateViewTests(PostUpdateViewTestCase):
    pass


class PostUpdateViewTests(PostUpdateViewTestCase):
    pass


class PostUpdateViewTests(PostUpdateViewTestCase):
    pass