from django.urls import path
from django.contrib import admin
from . import views


from django.urls import path
from . import views


urlpatterns = [
     path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/<int:user_id>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('logout/', views.logout_user, name='logout_user'),
    path('login/', views.login_user, name='login_user'),
    path('special/', views.special_view, name='special_view'),
    path('register', views.register_user,name='register_user')
]