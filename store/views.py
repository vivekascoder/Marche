from django.shortcuts import (
    render, HttpResponse, Http404, get_object_or_404,
    redirect
)
from store.models import (
    Category,
    Product,
    Cart,
    Order
)
from instamojo_wrapper import Instamojo
from django.conf import settings


def home(request):
    context = {
        'categories': Category.objects.all()[:4]
    }
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.get_or_create(user=user)[0]
        context['cart_count'] = cart.products.count()

    return render(request, "index.html", context=context)

def cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.get_or_create(user=user)[0]
        products = cart.products.all()
        context = {
            'products': products,
            'total_price': cart.total_price(),
            'cart_total': cart.products.count()
        }
        return render(request, "store/cart.html", context=context)
    return Http404("Not for you.")

def products(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    context = {
        'products': category.products.all()
    }
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.get_or_create(user=user)[0]
        context['cart_total'] = cart.products.count()
    return render(request, 'store/products.html', context=context)

def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product
    }
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.get_or_create(user=user)[0]
        context['cart_total'] = cart.products.count()
    return render(request, 'store/product.html', context=context)


def add_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=product_id)
        user = request.user
        cart = Cart.objects.get_or_create(user=user)[0]
        cart.products.add(product)
        return redirect('cart')
    return HttpResponse("You're not logged In.")


def remove_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=product_id)
        user = request.user
        cart = Cart.objects.get_or_create(user=user)[0]
        cart.products.remove(product)
        return redirect('cart')
    return HttpResponse("You're not logged In.")


def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.get_or_create(user=user)[0]

        if cart.products.count() > 0:
            total_price = cart.total_price()
            api = Instamojo(
                api_key = settings.API_KEY, 
                auth_token = settings.AUTH_TOKEN, 
                endpoint='https://test.instamojo.com/api/1.1/'
            )
            response = api.payment_request_create(
                amount = str(total_price),
                purpose = "Buying Products from March Site.",
                redirect_url = "http://localhost:8000/success"
            )
            return redirect(response['payment_request']['longurl'])
    return HttpResponse("You're not logged In.")

def successful_payment(request):
    """
    payment_id=MOJO0b10N05A12374905
    payment_status=Credit
    payment_request_id=1fb41cbaae844a8b88c970c081f71ba1
    website.com/cart?product_id=1
    """
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.get_or_create(user=user)[0]

        # Verifying the payments.
        payment_request_id = request.GET['payment_request_id']
        api = Instamojo(
            api_key = settings.API_KEY, 
            auth_token = settings.AUTH_TOKEN, 
            endpoint='https://test.instamojo.com/api/1.1/'
        )
        response = api.payment_request_status(payment_request_id)

        if response['success']:
            order = Order.objects.create(
                payer = user,
                status = 'Accepted'
            )

            for product in cart.products.all():
                product.quantity -= 1
                order.cart.add(product)

            # Everything was successful now, clear the existing cart.
            cart.products.clear()
            context = {
                'cart_count': cart.products.count()
            }
            return render(request, "store/success.html", context=context)
        return HttpResponse("OH! Man This is not how it works.")
        return HttpResponse("You're not logged In.")