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


class TestUsersDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="aziza", first_name="Aziza")
        self.client = Client()

    def test_detail_endpoint(self):
        url = reverse("users-detail", kwargs={"pk": self.user.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/users_detail.html")


class TestUsersListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("users-list")

    def test_list_endpoint(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/users_list.html")


class TestUsersCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("users-create")

    def test_get_create_endpoint(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/users_update.html")

    def test_post_create_endpoint_success(self):
        data = {
            "username": "sfdsodfsf",
            "first_name": "Anna",
            "last_name": "Sabirova",
            "email": "anna@email.com",
            "is_active": True,
            "groups": [],
        }
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 302)

    def test_post_create_endpoint_unccorect_data(self):
        data = {
            "username": "",
            "first_name": "",
            "last_name": "",
        }
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/users_update.html")


class TestUsersUpdateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="aziza", first_name="Aziza")
        self.url = reverse("users-update", args=[self.user.pk])

    def test_get_endpoint(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/users_update.html")

    def test_post_endpoint_success(self):
        data = {
            "username": "aziza",
            "first_name": "Azizajon",
            "last_name": "Sabirova",
            "email": "anna@email.com",
            "is_active": True,
            "groups": [],
        }
        response = self.client.post(self.url, data)

        self.user.refresh_from_db()

        self.assertEqual(self.user.first_name, data["first_name"])

        self.assertEqual(response.status_code, 302)

    def test_post_endpoint_fail(self):
        data = {"username": "", "first_name": "Azizajon", "last_name": "", "email": ""}
        response = self.client.post(self.url, data)

        self.user.refresh_from_db()

        self.assertNotEqual(self.user.first_name, data["first_name"])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/users_update.html")

    def test_404_on_user_does_not_exist(self):
        response = self.client.get(reverse("users-update", args=[999999999]))

        self.assertEqual(response.status_code, 404)


class TestUsersDeleteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="aziza", first_name="Aziza")
        self.url = reverse("users-delete-confirmation", args=[self.user.pk])

    def test_get_endpoint(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/users_delete.html")

    def test_404_on_user_does_not_exist(self):
        response = self.client.get(
            reverse("users-delete-confirmation", args=[999999999])
        )

        self.assertEqual(response.status_code, 404)

    def test_post_endpoint_success(self):
        data = {}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        assert not User.objects.filter(pk=self.user.pk).first()
