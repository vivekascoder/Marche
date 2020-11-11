from django.urls import path
from shipper import views as shipper_views

urlpatterns = [
    path('', shipper_views.shipper_home, name='shipper-home'),
    path('orders', shipper_views.all_orders, name='all-orders'),
    path('orders/select/<int:order_id>', shipper_views.select_order, name='select-order'),
    path('orders/pending', shipper_views.pending_orders, name='pending-orders'),
    path('orders/completed', shipper_views.completed_orders, name='completed-orders'),
    path('orders/change_status/<int:order_id>', shipper_views.change_status, name='change-status'),
]