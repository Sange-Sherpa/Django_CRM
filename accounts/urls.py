from django.urls import path
from .views import *

urlpatterns = [
    # MAIN PAGE
    path('', dashboard, name='dashboard'),

    # LOGIN RELATED

    # PAGES
    path('customer/<int:pk>/', customer, name='customers'),
    path('products/', product, name='products'),
    path('orders/', order, name='orders'),

    # FORMS
    path('create_order/', createOrder, name='create_order'),
    path('update_order/<int:pk>/', updateOrder, name='update_order'),
    path('delete_order/<int:pk>/', deleteOrder, name='delete_order'),

    path('create_customer/', createCustomer, name='create_customer'),
    path('update_customer/<int:pk>/', updateCustomer, name='update_customer'),
    path('delete_customer/<int:pk>/', deleteCustomer, name='delete_customer'),
]