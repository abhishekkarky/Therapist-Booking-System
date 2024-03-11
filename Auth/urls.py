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
    path('admin-edit-therapist/<int:therapist_id>', views.editTherapist, name='admin-edit-therapist'),
    path('admin-delete-therapist/<int:therapist_id>', views.deleteTherapist, name='admin-delete-therapist'),
    path('bookinglist', views.bookinglist, name='bookinglist'),
    # path('delete-booking<int:id>', views.user_delete_booking, name='delete-booking'),
    # path('admin_delete-booking<int:id>', views.admin_delete_booking, name='admin-delete-booking'),
    path('booking', views.booking, name='booking'),
    path('logout', views.user_logout, name='logout'),
]