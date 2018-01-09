from . import models
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView


# Create your views here.


class HomeIndexView(TemplateView):
    template_name = "profiles/index.html"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("index")


class UserProfileEditView(UpdateView):
    model = models.UserProfile
    slug_field = 'user__username'
    slug_url_kwarg = "username"
    fields = ['avatar', 'bio']
    template_name = "profiles/profile_update.html"


class UserProfileView(DetailView):
    slug_field = "user__username"  # Enables users to search by username
    slug_url_kwarg = "username"
    model = models.UserProfile
    template_name = "profiles/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_followed'] = models.Follow.objects.filter(followee=self.request.user,
                                                                   follower=self.get_object().user)
        context['user_is_following'] = models.Follow.objects.filter(followee=self.get_object().user,
                                                                    follower=self.request.user)
        context['mutual_follow'] = context['user_is_following'] and context['user_is_followed']
        return context


class UserSignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('index')
    template_name = "profiles/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully')
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response

@login_required()
def make_new_follow_view(request, *args, **kwargs):
    if request.method == "POST":
        to_user_username = request.POST.get("to_user_username")
        to_user_instance = User.objects.get(username=to_user_username)
        models.Follow.objects.create(followee=to_user_instance, follower=request.user)
        return HttpResponseRedirect(reverse_lazy("userprofile", kwargs={'username': to_user_username}))
    return HttpResponseRedirect(reverse_lazy("fail", kwargs={}))


@login_required()
def delete_follow_view(request, *args, **kwargs):
    if request.method == "POST":
        to_user_username = request.POST.get("to_user_username")
        to_user_instance = User.objects.get(username=to_user_username)
        instance_to_delete = models.Follow.objects.get(followee=to_user_instance, follower=request.user)
        instance_to_delete.delete()
        return HttpResponseRedirect(reverse_lazy("userprofile", kwargs={'username': to_user_username}))