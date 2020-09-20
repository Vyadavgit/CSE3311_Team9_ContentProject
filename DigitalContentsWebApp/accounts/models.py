from django.db import models


# Create your models here.
class Customer(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    first_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=250, null=True)
    gender = models.CharField(max_length=25, choices=GENDER_CHOICES, blank=True)

    def __str__(self):
        if self.first_Name and self.last_Name:
            identity = (self.first_Name + " " + self.last_Name)
        else:
            identity = str(self.id)
        return identity
