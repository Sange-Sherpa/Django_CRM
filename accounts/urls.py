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
]