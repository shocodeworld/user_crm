from django.contrib.auth import get_user_model
from django.views.generic import DetailView, ListView

User = get_user_model()


class UserListView(ListView):
    template_name = "users/users_list.html"
    queryset = User.objects.all()


class UserDetailView(DetailView):
    template_name = "users/users_detail.html"
    queryset = User.objects.all()
