from django.contrib import admin
from django.urls import path

from users import views

urlpatterns = [
    path("", views.UserListView.as_view(), name="users-list"),
    path("create/", views.users_create, name="users-create"),
    path("<pk>", views.UserDetailView.as_view(), name="users-detail"),
    path("<pk>/update/", views.users_update, name="users-update"),
    path("<pk>/delete/", views.users_delete, name="users-delete-confirmation"),
]
