from django.shortcuts import render
from .models import *

# Create your views here.
def dashboard(request):
    orders      =   Order.objects.all()
    customers   =   Customer.objects.all()

    total_orders    =   orders.count()
    total_customers =   customers.count()
    delivered       =   orders.filter(status='Delivered').count()
    pending         =   orders.filter(status='Pending').count()

    context =   {
        'orders': orders,
        'customers': customers,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'delivered': delivered,
        'pending': pending,
    }

    return render(request, 'dashboard.html', context)

def customer(request, pk):
    customer    =   Customer.objects.get(id=pk)
    orders      =   customer.order_set.all()
    total_orders = orders.count()

    context     =   {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
    }
    return render(request, 'pages/customer.html', context)

def product(request):
    products    =   Product.objects.all()
    return render(request, 'pages/product.html', {'products': products})

def order(request):
    return render(request, 'pages/order.html')