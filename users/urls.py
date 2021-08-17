from django.urls import path
# from users.views import UserLoginView, UserRegistrationView, UserLogoutView, UserProfileView, verify
from users.views import UserLoginView, UserRegistrationView, UserLogoutView, user_profile, verify

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', user_profile, name='profile'),
    path('verify/<email>/<activation_key>', verify, name='verify'),

]
