from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserListView.as_view(), name='user-view'),
    path('login/', views.LoginView.as_view(), name='user-login'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile')
]
