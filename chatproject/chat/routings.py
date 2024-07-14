from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path(r"ws/open_chat/<int:id>/", consumers.JoinAndLeave.as_asgi())
]