from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth.models import Group


def users_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='Viewer')
        instance.groups.add(group)

        Customer.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email
        )


post_save.connect(users_profile, sender=User)
