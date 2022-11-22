from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import Client, TestCase

User = get_user_model()


class TestUsersSearch(TestCase):
    def setUp(self):
        User.objects.create(username="aziza", first_name="Aziza")
        User.objects.create(username="kamila", first_name="Kamila")
        User.objects.create(username="manizha", first_name="Manizha")
        self.url = reverse("users-search")
        self.client = Client()

    def test_search_endpoint(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/users_list.html")

    def test_search_endpoint_response_users(self):
        query = "Kamila"
        url = self.url + "?search=" + query  # users/search/?search=Kamila

        response = self.client.get(url)
        self.assertEqual(response.context["object_list"].count(), 1)
