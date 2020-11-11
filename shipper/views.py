from django.shortcuts import render, HttpResponse, Http404, get_object_or_404, redirect
from store.models import User, Order
from django.contrib.auth.models import Group
from django import forms

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']


def shipper_home(request):
    if request.user.is_authenticated and request.user.groups.filter(name='shipper').exists():
        context = {

        }
        return render(request, "shipper/index.html", context=context)
    return HttpResponse("You're authorized.")


def all_orders(request):
    if request.user.is_authenticated and request.user.groups.filter(name='shipper').exists():
        context = {
            'orders': Order.objects.filter(shipper=None),
            'title': 'All Orders'
        }
        return render(request, "shipper/table.html", context=context)
    return Http404("Not Allowed.")

def select_order(request, order_id):
    if request.user.is_authenticated and request.user.groups.filter(name='shipper').exists():
        order = get_object_or_404(Order, pk=order_id)
        order.shipper = request.user
        order.save()
        return redirect('all-orders')
    return Http404("Not Allowed.")

def pending_orders(request):
    if request.user.is_authenticated and request.user.groups.filter(name='shipper').exists():
        orders = Order.objects.filter(shipper=request.user).exclude(status='Shipped')
        context = {
            'orders': orders,
        }
        return render(request, "shipper/pending_orders.html", context=context)
    return Http404("Not Allowed.")


def completed_orders(request):
    if request.user.is_authenticated and request.user.groups.filter(name='shipper').exists():
        orders = Order.objects.filter(shipper=request.user, status='Shipped')
        context = {
            'orders': orders,
            'title': 'Completed Orders'
        }
        return render(request, "shipper/completed_orders.html", context=context)
    return Http404("Not Allowed.")

def change_status(request, order_id):
    if request.user.is_authenticated and request.user.groups.filter(name='shipper').exists():
        order = get_object_or_404(Order, pk=order_id)
        if order.shipper == request.user and order.status != "Shipped":
            if request.method == 'POST': 
                form = OrderStatusForm(instance=order, data=request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("pending-orders")
            form = OrderStatusForm(instance=order)
            context = {
                'form': form,
                'title': 'Change Status'
            }
            return render(request, "shipper/change_status.html", context=context)
    return Http404("Not Allowed.")