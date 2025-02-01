from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
     path('',views.user_profile,name='user_profile'),
     path('register/',views.register_user,name='register_user'),
     path('login/',views.login_user,name='Login-user'),
]