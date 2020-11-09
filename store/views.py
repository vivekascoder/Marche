from django.shortcuts import render, HttpResponse, Http404, get_object_or_404
from store.models import (
    Category,
    Product
)


def home(request):
    context = {
        'categories': Category.objects.all()[:4]
    }
    return render(request, "index.html", context=context)

def cart(request):
    context = {

    }
    return render(request, "store/cart.html", context={})

def products(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    context = {
        'products': category.products.all()
    }
    return render(request, 'store/products.html', context=context)

def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product
    }
    return render(request, 'store/product.html', context=context)