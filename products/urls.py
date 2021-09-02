from django.urls import path
from products.views import products
from django.views.decorators.cache import cache_page

app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
    path('<int:category_id>/', cache_page(3600)(products), name='product'),
    path('page/<int:page>/', products, name='page'),
]
