from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from Home.models import ContactList


def home(request):
    return render(request, 'home.html')