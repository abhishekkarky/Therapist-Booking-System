from django.urls import path
from Auth import views

urlpatterns = [
    path('login', views.user_login, name='login'),
    path('signup', views.register, name='register'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('faq', views.FAQ, name='faq'),
    path('contact', views.contect, name='contact'),
        path('admin-page', views.adminPage, name='admin-page'),
    path('admin-property-management', views.adminProperty, name='admin-property-management'),
    path('admin-enquiry-management', views.enquiryProperty, name='admin-enquiry-management'),
    path('admin-agent-management', views.agentManagement, name='admin-agent-management'), 
    path('admin-teams-management', views.teamsManagement, name='admin-teams-management') 
]