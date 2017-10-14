from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.urls import resolve

from .. import forms, models, views


class BoardTopicsTests(TestCase):

    def setUp(self):
        models.Board.objects.create(name='Django', description='Django board')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func.view_class, views.TopicListView)

    def test_board_topics_view_contains_link_back_to_homepage(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        homepage_url = reverse('index')
        self.assertContains(response, f'href="{homepage_url}"')

    def test_board_topics_view_contains_navigation_link(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        homepage_url = reverse('index')
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
