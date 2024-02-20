from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.views.generic.edit import UpdateView

from .forms import UpdateProfileForm, UserRegisterForm


def index_redirect(request):
    return redirect('home')


# class CustomUserRegisterView(View):
#     template_name = 'users/register.html'
#
#     def get(self, request, *args, **kwargs):
#         form = CustomUserRegisterView()
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = CustomUserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#         return render(request, self.template_name, {'form': form})


class CustomUserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class HomeView(View):
    template_name = 'users/home.html'

    def get(self, request):
        return render(request, self.template_name)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class CustomLogoutView(LogoutView):

    def get_success_url(self):
        return reverse_lazy('home')


class ProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request):
        return render(request, self.template_name)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateProfileForm
    template_name = 'users/update_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
