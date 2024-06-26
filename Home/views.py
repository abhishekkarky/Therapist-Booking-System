from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from Auth.models import Testimonials
from Home.models import ContactList

def home(request):
    testimonials=Testimonials.objects.all()
    if request.user.is_authenticated:
        if request.user.is_admin:
            messages.error(request, 'You do not have access to this page.')
            return redirect('/admin-page')
        
    return render(request, 'home.html', {"testimonials": testimonials})
