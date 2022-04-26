from django.contrib import messages
from django.shortcuts import redirect, render
from django.forms import inlineformset_factory # creates multiple forms inside a single form

from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .forms import *
from .models import *
from .decorators import *

# REGISTRATION RELATED ----------------------
@unauthenticated_user
def userRegister(request):
    form    =   CreateUserForm()

    if request.method == 'POST':
        form    =   CreateUserForm(request.POST)
        if form.is_valid():
            user     =  form.save()
            username =  form.cleaned_data.get('username')

            # This assigns customer group to the user during registration...
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name=user.username,
            )

            messages.success(request, f'{username}, your account has been successfully created.')
            return redirect('/')

    context = {'form': form}
    return render(request, 'registration/register.html', context)

@unauthenticated_user
def userLogin(request):
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
# @allowed_users(allowed_roles=['Admin'])
@admin_only
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def product(request):
    products    =   Product.objects.all()

    context     =   {'products': products}
    return render(request, 'pages/product.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer'])
def userPage(request):
    orders          =   request.user.customer.order_set.all()

    total_orders    =   orders.count()
    delivered       =   orders.filter(status='Delivered').count()
    pending         =   orders.filter(status='Pending').count()

    context =   {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
    }

    return render(request, 'pages/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer'])
def accountSettings(request):
    customer    =   request.user.customer
    form        =   CustomerForm(instance=customer)
    
    if request.method == 'POST':
        form    =   CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            # return redirect('/')

    context =   {'form': form}
    return render(request, 'pages/account_settings.html', context)



# ORDERS RELATED --------------
@allowed_users(allowed_roles=['Admin'])
def createOrder(request, pk):
    OrderFormSet    =   inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer        =   Customer.objects.get(id=pk)
    formset         =   OrderFormSet(instance=customer) # jasko lagi order place garne ho ... tesko name display huncha
    # form          =   OrderForm(initial={'customer': customer}) # jasko lagi order place garne ho ... tesko name display huncha

    if request.method == 'POST': 
        formset     =   OrderFormSet(request.POST, instance=customer)

        if formset.is_valid():
            formset.save()
            return redirect('/')

    context =   {'formset': formset}
    return render(request, 'forms/order_form.html', context)



@allowed_users(allowed_roles=['Admin'])
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



@allowed_users
def deleteOrder(request, pk):
    order   = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        messages.info(request, f'{order} was removed')
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



@allowed_users(allowed_roles=['Admin'])
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



@allowed_users(allowed_roles=['Admin'])
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



@allowed_users(allowed_roles=['Admin'])
def deleteCustomer(request, pk):
    customer   = Customer.objects.get(id=pk)

    if request.method == 'POST':
        customer.delete()
        messages.add_message(request, messages.SUCCESS, f'{customer} was removed.')
        return redirect('/')

    context = {'customer': customer}
    return render(request, 'forms/delete_customer.html', context)