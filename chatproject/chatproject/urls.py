from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('chats/', include('chat.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
