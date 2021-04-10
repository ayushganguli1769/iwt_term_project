from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('test/',views.test,name='test'),
    path('login/',views.login,name='login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('bot_input/<str:text>',views.chat_input,name='chat_input'),
    path('',views.chat_box,name="chat_box")
]
