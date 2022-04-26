from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Customer

def customerProfile(sender, instance, created, **kwargs):
    if created:
        # This assigns customer group to the user during registration...
        group = Group.objects.get(name='Customer')
        instance.groups.add(group)

        Customer.objects.create(
            user  = instance,
            name  = instance.username,
        )
        print("profile created !")
    else:
        print("profile not created !")

post_save.connect(customerProfile, sender=User)