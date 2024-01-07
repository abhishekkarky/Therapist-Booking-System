from django.urls import path
from Auth import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('signup', views.register, name='register')
]