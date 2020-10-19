from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=250, null=True)
    gender = models.CharField(max_length=25, blank=True)
    birth_date = models.DateField(null=True)
    profile_picture = models.ImageField(default="profile_null.png", null=True, blank=True)
    email = models.CharField(max_length=250, null=True)
    phone_number = models.CharField(max_length=250, null=True)
    profession = models.CharField(max_length=250, null=True)
    videofile = models.FileField(default="video_null.mp4", null=True, blank=True)

    def __str__(self):
        if self.first_name and self.last_name:
            identity = (self.first_name + " " + self.last_name)
        else:
            identity = str(self.id)
        return identity


class File(models.Model):
    CATEGORY_CHOICES = [('Comedy', 'Comedy'), ('Fitness', 'Fitness'), ('Cooking', 'Cooking'),
                        ('Entertainment', 'Entertainment'), ('Technology', 'Technology'), ('Music', 'Music'),
                        ('Other', 'Other')]

    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, null=True)
    category = models.CharField(max_length=25, choices=CATEGORY_CHOICES, null=True, blank=True)
    upload_video = models.FileField(null=True, blank=True)
    upload_date_and_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.description
