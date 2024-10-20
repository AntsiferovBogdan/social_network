from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse, reverse_lazy

from my_profile.forms import CustomAuthenticationForm, CustomUserChangeForm, CustomUserCreationForm
from my_profile.models import CustomUser as User


class RedirectAuthenticatedUserMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile', username=request.user.username)
        return super().dispatch(request, *args, **kwargs)


class LoginUserView(RedirectAuthenticatedUserMixin, LoginView):
    template_name = 'login.html'
    form_class = CustomAuthenticationForm

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user.username})


class RegisterUserView(RedirectAuthenticatedUserMixin, CreateView):
    template_name = 'registration.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'edit_profile.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user.username})


def index(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('profile', username=request.user.username)
    else:
        return redirect('login')


def show_profile(request: HttpRequest, username: str) -> HttpResponse:
    profile_user = get_object_or_404(User, username=username)
    return render(
        request,
        'profile.html',
        context={
            'profile_user': profile_user,
        }
    )
