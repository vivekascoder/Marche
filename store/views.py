from django.shortcuts import render, HttpResponse, Http404

def home(request):
    return render(request, "index.html", context={})

def cart(request):
    return render(request, "store/cart.html", context={})