# user_app/urls.py

from django.urls import path
from . import views
from .views import UserDataView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('api/user-data/', UserDataView.as_view(), name='user-data'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('logout/', views.logout_view, name='logout'),
]
