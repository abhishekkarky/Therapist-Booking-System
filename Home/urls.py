from django.urls import path
from Home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('/contact', views.contact, name='contact'),
    path('contact-list', views.contactList, name='contact-list')
]