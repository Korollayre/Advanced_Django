from django.urls import path

from admins.views import index, UserListView, UserCreateView, UserUpdateView, UserDeleteView, \
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('users/create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='admin_users_update'),
    path('users/remove/<int:pk>/', UserDeleteView.as_view(), name='admin_users_remove'),
    path('categories/', CategoryListView.as_view(), name='admin_product_category'),
    path('categories/create/', CategoryCreateView.as_view(), name='admin_product_category_create'),
    path('categories/update/<int:pk>/', CategoryUpdateView.as_view(), name='admin_product_category_update'),
    path('categories/remove/<int:pk>/', CategoryDeleteView.as_view(), name='admin_product_category_remove'),
]
