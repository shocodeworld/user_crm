from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from users.forms import UserForm

User = get_user_model()


class UserListView(ListView):
    template_name = "users/users_list.html"
    queryset = User.objects.all()


class UserDetailView(DetailView):
    template_name = "users/users_detail.html"
    queryset = User.objects.all()


def users_create(request):
    form = UserForm()
    return render(request, "users/users_update.html", {"form": form})
