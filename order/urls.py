from django.urls import path
from order.views import OrderList, OrderItemCreate, OrderItemUpdate, OrderItemDelete, OrderItemRead, order_forming_complete
app_name = 'order'

urlpatterns = [
    path('', OrderList.as_view(), name='orders'),
    path('read/<int:pk>/', OrderItemRead.as_view(), name='order_read'),
    path('update/<int:pk>/', OrderItemUpdate.as_view(), name='order_update'),
    path('delete/<int:pk>/', OrderItemDelete.as_view(), name='order_delete'),
    path('create/', OrderItemCreate.as_view(), name='order_create'),
    path('forming/complete/<int:pk>', order_forming_complete, name='order_forming_complete'),
]