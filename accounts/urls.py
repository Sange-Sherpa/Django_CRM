from django.urls import path
from .views import *

urlpatterns = [
    # MAIN PAGE
    path('', dashboard, name='dashboard'),

    # LOGIN RELATED
    path('register/', userRegister, name='register'),
    path('login/', userLogin, name='login'),
    path('logout/', userLogout, name='logout'),

    # PAGES
    path('user/', userPage, name='user'),
    path('products/', product, name='products'),
    # path('orders/', order, name='orders'), # deleted page
    path('account/', accountSettings, name='account'),
    path('customer/<int:pk>/', customer, name='customers'),

    # FORMS
    path('create_order/<int:pk>/', createOrder, name='create_order'),
    path('update_order/<int:pk>/', updateOrder, name='update_order'),
    path('delete_order/<int:pk>/', deleteOrder, name='delete_order'),
    # path('delete_product/<int:pk>/', deleteProduct, name='delete_product'),

    path('create_customer/', createCustomer, name='create_customer'),
    path('update_customer/<int:pk>/', updateCustomer, name='update_customer'),
    path('delete_customer/<int:pk>/', deleteCustomer, name='delete_customer'),
]