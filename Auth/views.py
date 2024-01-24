from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate

def user_login(request):
    if request.method == 'POST':
        number = request.POST['number']
        password = request.POST['password']

        user = authenticate(request, username=number, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('/')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        number = request.POST['number']
        password = request.POST['password']

        User = get_user_model()

        user = User.objects.create_user(username=number, email=email, password=password)
        user.name = name
        user.number = number
        user.save()

        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')

    return render(request, 'register.html')

@login_required
def about(request):
    return render(request, 'about.html')

@login_required
def services(request):
    return render(request, 'services.html')

@login_required
def FAQ(request):
    return render(request, 'FAQ.html')

@login_required
def contect(request):
    return render(request, 'contact.html')

def adminPage(request):
    return render(request, 'admin/admin-panel.html')

def adminProperty(request):
    return render(request, 'admin/property-management.html')

def enquiryProperty(request):
    return render(request, 'admin/enquiry-management.html')
def agentManagement(request):
    return render(request, 'admin/agent-management.html')
def teamsManagement(request):
    return render(request, 'admin/teams-management.html')
