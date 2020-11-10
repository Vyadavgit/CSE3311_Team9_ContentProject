# Source: https://github.com/hackstarsj/simpleDjangoProject.git

from django.urls import re_path
from .Consumer import Consumer

websocket_urlpatterns=[
    re_path(r'ws/(?P<room_name>\w+)/(?P<person_name>\w+)/$',Consumer)
]