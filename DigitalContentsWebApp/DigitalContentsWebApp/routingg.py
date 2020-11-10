# Source: https://github.com/hackstarsj/simpleDjangoProject.git

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from .routingtwo import websocket_urlpatterns

application=ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})