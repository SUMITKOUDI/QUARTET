from django.urls import path
from django.contrib import admin
from . import views


urlpatterns = [
    path('logout/', views.logout_user, name='logout_user'),
    path('login/', views.login_user, name='login_user'),
    path('special/', views.special_view, name='special_view'),
    path('register', views.register_user,name='register_user')
]