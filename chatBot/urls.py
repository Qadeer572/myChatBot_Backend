from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.chat,name="chat"),
    path('history/',views.get_chat_history,name="chat_history"),
]
