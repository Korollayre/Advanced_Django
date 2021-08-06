from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
# from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.conf import settings

from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, SocialUserProfileForm


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

        if self.request.method == 'POST':
            context['profile_form'] = SocialUserProfileForm(self.request.POST, instance=self.request.user.socialuser)
        else:
            context['profile_form'] = SocialUserProfileForm()

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


# class UserProfileView(UpdateView):
#     model = User
#     class_form = UserProfileForm
#     template_name = 'users/profile.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(UserProfileView, self).get_context_data(object_list=None, **kwargs)
#         context['title'] = 'GeekShop - Личный кабинет'
#         return context
#
#     def get_success_url(self):
#         return reverse('users:profile', kwargs={'pk': self.kwargs['pk']})
#
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super(UserProfileView, self).dispatch(request, *args, **kwargs)

@login_required
def user_profile(request, pk):
    selected_user = User.objects.get(id=pk)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=selected_user)
        social_form = SocialUserProfileForm(request.POST, instance=selected_user.socialuser)
        if profile_form.is_valid() and social_form.is_valid():
            profile_form.save()
    else:
        profile_form = UserProfileForm(instance=selected_user)
        social_form = SocialUserProfileForm(instance=selected_user.socialuser)

    context = {'title': 'GeekBrains - Профиль',
               'profile_form': profile_form,
               'social_form': social_form,
               }
    return render(request, 'users/profile.html', context)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')


def verify(request, email, activation_key):
    current_user = User.objects.filter(email=email).first()
    if current_user:
        if current_user.activation_key == activation_key and not current_user.is_activation_key_expired():
            current_user.is_active = True
            current_user.save()
            auth.login(request, current_user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'users/verify.html')
    return HttpResponseRedirect(reverse('index'))


def send_verify_mail(user):
    subject = 'Verify your account'
    link = reverse('users:verify', args=[user.email, user.activation_key])
    message = f'{settings.DOMAIN}{link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
