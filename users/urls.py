from django.contrib import admin
from django.urls import path

from users import views

urlpatterns = [
    path("", views.UserListView.as_view()),
    path("<pk>", views.UserDetailView.as_view()),
    path("create/", views.users_create),
]
