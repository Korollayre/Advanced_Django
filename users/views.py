from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.conf import settings

from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserLoginView, self).get_context_data(object_list=None, **kwargs)
        context['title'] = 'GeekShop - Авторизация'
        return context


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserRegistrationView, self).get_context_data(object_list=None, **kwargs)
        context['title'] = 'GeekShop - Регистрация'
        return context

    def get_success_url(self):
        if self.request.method == 'POST':
            if self.get_form().is_valid:
                user = self.get_form().save()
                if send_verify_mail(user):
                    print('Сообщение подтверждения отправлено')
                    return reverse_lazy('users:login')
                else:
                    print('Ошибка отправки сообщения')
                    return reverse_lazy('users:login')


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserProfileView, self).get_context_data(object_list=None, **kwargs)
        context['title'] = 'GeekShop - Личный кабинет'

        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserProfileView, self).dispatch(request, *args, **kwargs)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')


def verify(request, email, activation_key):
    current_user = User.objects.filter(email=email).first()
    if current_user:
        if current_user.activation_key == activation_key and not current_user.is_activation_key_expired():
            current_user.is_active = True
            current_user.save()
            auth.login(request, current_user)
            return render(request, 'users/verify.html')
    return HttpResponseRedirect(reverse('index'))


def send_verify_mail(user):
    subject = 'Verify your account'
    link = reverse('users:verify', args=[user.email, user.activation_key])
    message = f'{settings.DOMAIN}{link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
