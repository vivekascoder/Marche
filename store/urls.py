from django.urls import path
from . import views as store_views

urlpatterns = [
    path('', store_views.home, name='home'),
    path('cart', store_views.cart, name='cart'),
    path('product/<int:product_id>', store_views.product, name='product'),
    path('category/<int:category_id>/products', store_views.products, name='products-by-category'),
]