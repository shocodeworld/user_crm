from django.contrib import admin
from django.urls import path

from users import views

urlpatterns = [
    path("", views.UserListView.as_view(), name="users-list"),
    path("<pk>", views.UserDetailView.as_view(), name="users-detail"),
    path("create/", views.users_create, name="users-create"),
]
