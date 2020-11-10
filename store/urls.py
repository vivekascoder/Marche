from django.urls import path
from . import views as store_views

urlpatterns = [
    path('', store_views.home, name='home'),
    path('cart', store_views.cart, name='cart'),
    path('product/<int:product_id>', store_views.product, name='product'),
    path('category/<int:category_id>/products', store_views.products, name='products-by-category'),
    path('cart/add/<int:product_id>', store_views.add_cart, name='add-cart'),
    path('cart/remove/<int:product_id>', store_views.remove_cart, name='remove-cart'),
    path('checkout', store_views.checkout, name='checkout'),
]