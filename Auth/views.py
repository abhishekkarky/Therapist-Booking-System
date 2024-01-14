from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def FAQ(request):
    return render(request, 'FAQ.html')
def contect(request):
    return render(request, 'contact.html')
