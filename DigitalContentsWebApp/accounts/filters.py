import django_filters
from .models import *


class FileFilter(django_filters.FilterSet):
    class Meta:
        model = File
        fields = ['title']


class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = ['first_name']
