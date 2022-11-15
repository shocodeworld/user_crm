from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from users.forms import UserForm

User = get_user_model()


class UserListView(ListView):
    template_name = "users/users_list.html"
    queryset = User.objects.all()


class UserDetailView(DetailView):
    template_name = "users/users_detail.html"
    queryset = User.objects.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["object"] = model_to_dict(ctx["object"], exclude=["password"])
        return ctx


def users_create(request):
    form = UserForm()

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users-list")

    return render(request, "users/users_update.html", {"form": form})


def users_update(request, pk):
    user = get_object_or_404(User, pk=pk)

    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("users-list")

    return render(request, "users/users_update.html", {"form": form})


def users_delete(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        user.delete()
        return redirect("users-list")

    return render(
        request,
        "users/users_delete.html",
        {"object": model_to_dict(user, exclude=["password"])},
    )


# Ниже примеры получения того же, что сделано выше, но с искользованием CBV (class based views)
# ниже примеры использования дженериков (встроенных вьюх джанго)

# class UserCreateView(CreateView):


# тоже самое, но с использованием TemplateView
class UserListTemplateView(TemplateView):
    #
    template_name = "users/users_list.html"
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["object_list"] = self.queryset
        return self.render_to_response(context)


class UserCreateTemplateView(TemplateView):
    template_name = "users/users_update.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["form"] = UserForm()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users-list")

        context["form"] = form
        return self.render_to_response(context)


class UserUpdateTemplateView(TemplateView):
    template_name = "users/users_update.html"

    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        context = self.get_context_data(**kwargs)
        context["form"] = UserForm(instance=user)
        return self.render_to_response(context)

    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("users-list")

        context = self.get_context_data(**kwargs)
        context["form"] = form
        return self.render_to_response(context)


class UserDeleteTemplateView(TemplateView):
    template_name = "users/users_delete.html"

    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        context = self.get_context_data(**kwargs)
        context["object"] = model_to_dict(user, exclude=["password"])
        return self.render_to_response(context)

    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect("users-list")
