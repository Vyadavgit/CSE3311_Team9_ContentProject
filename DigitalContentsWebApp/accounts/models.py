from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import date


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
    video_poster = models.ImageField(default="poster_null.jpg", null=True, blank=True)
    saved_files = models.ManyToManyField('File', related_name='+')  # TODO research more about this relation

    def __str__(self):
        if self.first_name and self.last_name:
            identity = (self.first_name + " " + self.last_name)
        else:
            identity = str(self.id)
        return identity

    def set_paid_until(self, date_or_timestamp):
        if isinstance(date_or_timestamp, int):
            # if input is int date_or_timestamp
            paid_until = date.fromtimestamp(date_or_timestamp)
        elif isinstance(date_or_timestamp, str):
            # if input is string date_or_timestamp
            paid_until = date.fromtimestamp(int(date_or_timestamp))
        else:
            paid_until = date_or_timestamp

        self.paid_until = paid_until
        self.save()

    def has_paid(self, current_date=datetime.date.today()):
        if self.paid_until is None:
            return False

        return current_date < self.paid_until


class File(models.Model):
    CATEGORY_CHOICES = [('Comedy', 'Comedy'), ('Fitness', 'Fitness'), ('Cooking', 'Cooking'),
                        ('Entertainment', 'Entertainment'), ('Technology', 'Technology'), ('Music', 'Music'),
                        ('Other', 'Other')]

    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=True)
    category = models.CharField(max_length=25, choices=CATEGORY_CHOICES, null=True, blank=True)
    upload_video = models.FileField(null=True, blank=True)
    upload_date_and_time = models.DateTimeField(auto_now_add=True, null=True)
    premium = models.BooleanField(default=False, blank=True)
    content_viewers = models.ManyToManyField(User)

    def __str__(self):
        return self.title


class StripeCustomer(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    stripeCustomerId = models.CharField(max_length=255)
    stripeSubscriptionId = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
