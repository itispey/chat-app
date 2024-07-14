from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ChatListView.as_view()),
    path('<int:pk>/', views.MessageListView.as_view()),
]
