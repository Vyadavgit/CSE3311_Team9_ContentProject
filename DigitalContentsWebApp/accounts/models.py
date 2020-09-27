from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=250, null=True)
    gender = models.CharField(max_length=25, blank=True)
    birth_date = models.DateField(null=True)
    email = models.CharField(max_length=250, null=True)
    phone_number = models.CharField(max_length=250, null=True)
    profession = models.CharField(max_length=250, null=True)

    def __str__(self):
        if self.first_name and self.last_name:
            identity = (self.first_name + " " + self.last_name)
        else:
            identity = str(self.id)
        return identity
