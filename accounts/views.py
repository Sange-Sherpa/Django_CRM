from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import *
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


def product(request):
    products    =   Product.objects.all()
    return render(request, 'pages/product.html', {'products': products})




# -------------- ORDER RELATED --------------

def order(request):
    return render(request, 'pages/order.html')


def createOrder(request):
    form    =   OrderForm()

    if request.method == 'POST':
        # print(request.POST)
        form = OrderForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context =   {'form': form}
    return render(request, 'forms/order_form.html', context)


def updateOrder(request, pk):
    order   = Order.objects.get(id=pk)
    form    = OrderForm(instance=order) # this prefills the form with previous data

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'forms/order_form.html', context)


def deleteOrder(request, pk):
    order   = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        messages.add_message(request, messages.SUCCESS, f'{order}')
        return redirect('/')

    context = {'order': order}
    return render(request, 'forms/delete_form.html', context)




# -------------- CUSTOMER RELATED --------------

def customer(request, pk):
    customer        =   Customer.objects.get(id=pk)
    orders          =   customer.order_set.all()
    total_orders    = orders.count()

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
    }
    return render(request, 'pages/customer.html', context)


def createCustomer(request):
    form    =   CustomerForm()

    if request.method == 'POST':
        # print(request.POST)
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context =   {'form': form}
    return render(request, 'forms/customer_form.html', context)


def updateCustomer(request, pk):
    customer    =   Customer.objects.get(id=pk)
    form        =   CustomerForm(instance=customer)

    if request.method == 'POST':
        form    =   CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'forms/customer_form.html', context)


def deleteCustomer(request, pk):
    customer   = Customer.objects.get(id=pk)

    if request.method == 'POST':
        customer.delete()
        messages.add_message(request, messages.SUCCESS, f'{customer}')
        return redirect('/')

    context = {'customer': customer}
    return render(request, 'forms/delete_customer.html', context)