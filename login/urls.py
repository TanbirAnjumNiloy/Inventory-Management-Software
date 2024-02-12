from django.contrib import admin
from django.urls import path, include
from login import views

urlpatterns = [
    path('signup/',views.SignupPage,name='signup'),
    path('',views.LoginPage,name='login'),
    path('logout/',views.LogoutPage,name='logout'),
    
]
