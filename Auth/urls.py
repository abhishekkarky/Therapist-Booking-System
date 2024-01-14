from django.urls import path
from Auth import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('signup', views.register, name='register'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('faq', views.FAQ, name='faq'),
    path('contact', views.contect, name='contact'),
]