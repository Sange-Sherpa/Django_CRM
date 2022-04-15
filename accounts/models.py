from django.db import models

# Create your models here.
class Customer(models.Model):
    name            =   models.CharField(max_length=200, null=True)
    phone           =   models.CharField(max_length=200, null=True)
    email           =   models.CharField(max_length=200, null=True)
    date_created    =   models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name.capitalize()


class Tag(models.Model):
    name    =   models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name.capitalize()


class Product(models.Model):
    CAGTEGORY       = (
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Both', 'Both'),
    )

    name            =   models.CharField(max_length=200, null=True)
    price           =   models.FloatField()
    category        =   models.CharField(max_length=200, null=True, choices=CAGTEGORY)
    description     =   models.CharField(max_length=200, null=True, blank=True)
    date_created    =   models.DateTimeField(auto_now_add=True, null=True)
    tags            =   models.ManyToManyField(Tag)

    def __str__(self):
        return self.name.capitalize()



class Order(models.Model):
    STATUS          = (
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
    )

    customer        =   models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product         =   models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created    =   models.DateTimeField(auto_now_add=True, null=True)
    status         =   models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return self.product.name