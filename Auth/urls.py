from django.urls import path
from Auth import views

urlpatterns = [
    path('login', views.user_login, name='login'),
    path('signup', views.register, name='register'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('faq', views.FAQ, name='faq'),
    path('contact', views.contect, name='contact'),
    path('individual_therapist/<str:id>', views.individual, name='individual'),
    path('admin-page', views.adminPage, name='admin-page'),
    path('admin-booking-management', views.bookingManagement, name='admin-booking-management'),
    path('admin-teams-management', views.teamsManagement, name='admin-teams-management'),
]