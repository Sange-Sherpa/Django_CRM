from cmath import log
from django.contrib import messages
from django.shortcuts import redirect, render
from django.forms import inlineformset_factory # creates multiple forms inside a single form

from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

# REGISTRATION RELATED ----------------------
def userRegister(request):

    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form    =   CreateUserForm()

        if request.method == 'POST':
            form    =   CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, f'User Created Successfully.')
                return redirect('/')

        context = {'form': form}
        return render(request, 'registration/register.html', context)


def userLogin(request):

    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form    =   CreateUserForm()

        if request.method == 'POST':
            username    =   request.POST['username']
            password    =   request.POST['password1']
            user        =   authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {username}')
                return redirect('/')
            else:
                messages.info(request, 'username or password is incorrect.')

        context = {'form': form}
        return render(request, 'registration/login.html', context)


def userLogout(request):
    logout(request)
    return redirect('login')



# PAGES RELATED ----------------------
@login_required(login_url='login')
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


def userPage(request):
    context = {}
    return render(request, 'pages/user.html', context)



# ORDERS RELATED --------------

def order(request):
    return render(request, 'pages/order.html')


def createOrder(request, pk):
    OrderFormSet    =   inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer        =   Customer.objects.get(id=pk)
    formset         =   OrderFormSet(instance=customer) # jasko lagi order place garne ho ... tesko name display huncha
    # form          =   OrderForm(initial={'customer': customer}) # jasko lagi order place garne ho ... tesko name display huncha

    if request.method == 'POST': 
        # form = OrderForm(request.POST)
        formset     =   OrderFormSet(request.POST, instance=customer)

        if formset.is_valid():
            formset.save()
            return redirect('/')

    context =   {'formset': formset}
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
        messages.add_message(request, messages.SUCCESS, f'{order} was removed')
        return redirect('/')

    context = {'order': order}
    return render(request, 'forms/delete_form.html', context)




# CUSTOMER RELATED -------------------

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
        messages.add_message(request, messages.SUCCESS, f'{customer} was removed.')
        return redirect('/')

    context = {'customer': customer}
    return render(request, 'forms/delete_customer.html', context)