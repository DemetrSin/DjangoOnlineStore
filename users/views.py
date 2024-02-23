from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView
from django.views.generic.edit import UpdateView

from .forms import ClientCreateForm, UpdateProfileForm, UserRegisterForm, ClientUpdateForm, ReviewCreateForm
from .models import Client, Review


def index_redirect(request):
    return redirect('home')


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


class ProfileView(LoginRequiredMixin, View):
    template_name = 'users/profile.html'

    def get(self, request):
        try:
            client = Client.objects.get(user=request.user)
        except Client.DoesNotExist:
            client = None
        return render(request, self.template_name, {'client': client})


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


class ClientCreateView(LoginRequiredMixin, View):
    template_name = 'users/client.html'

    def get(self, request):
        form = ClientCreateForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ClientCreateForm(request.POST)
        if form.is_valid():
            Client.objects.get_or_create(
                user=request.user,
                first_name=form.instance.first_name,
                surname=form.instance.surname,
                email=request.user.email,
                phone=form.instance.phone,
                delivery_address=form.instance.delivery_address
            )

            return redirect(reverse('cart'))
        return render(request, self.template_name, {'form': form})


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientUpdateForm
    template_name = 'users/client_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return Client.objects.get(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewCreateView(View):
    template_name = 'users/review_create.html'

    def get(self, request):
        form = ReviewCreateForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ReviewCreateForm(request.POST)
        if form.is_valid():
            client = get_object_or_404(Client, user=request.user)
            Review.objects.create(
                client=client,
                grade=form.instance.grade,
                review_text=form.instance.review_text
            )
            return redirect('reviews_detail')
        return render(request, self.template_name, {'form': form})


class ReviewsDetailView(View):
    template_name = 'users/reviews_detail.html'

    def get(self, request):
        is_client = check_for_client_data(request.user.id)
        reviews = Review.objects.all()
        return render(request, self.template_name, {'reviews': reviews, 'is_client': is_client})


def check_for_client_data(user_id):
    user = User.objects.get(id=user_id)
    if hasattr(user, 'client_profile'):
        return True
