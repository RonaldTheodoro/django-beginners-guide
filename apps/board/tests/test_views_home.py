from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.urls import resolve

from .. import forms, models, views


class HomeTest(TestCase):

    def setUp(self):
        self.board = models.Board.objects.create(
            name='Django',
            description='Django board'
        )
        self.response = self.client.get(reverse('index'))

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_board_topics_url_resolves_index_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, views.BoardListView)

    def test_home_view_contains_link_to_topics_view(self):
        board_topics_url = reverse(
            'board_topics',
            kwargs={'pk': self.board.pk}
        )
        self.assertContains(self.response, f'href="{board_topics_url}"')
