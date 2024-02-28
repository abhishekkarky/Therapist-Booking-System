from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate
from Auth.models import Therapist

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

# @login_required
def about(request):
    therapist = Therapist.objects.all()
    return render(request, 'about.html', {'therapist': therapist})

# @login_required
def services(request):
    return render(request, 'services.html')

# @login_required
def FAQ(request):
    return render(request, 'FAQ.html')

# @login_required
def contect(request):
    return render(request, 'contact.html')

# @login_required
def individual(request, id):
    details = get_object_or_404(Therapist, id=id)
    return render(request, 'individual_therapist.html', {'details': details})

def adminPage(request):
    return render(request, 'admin/admin-panel.html')

def bookingManagement(request):
    return render(request, 'admin/booking-management.html')

def teamsManagement(request):
    therapist = Therapist.objects.all()
    if request.method == 'POST':
        image = request.FILES.get("image")
        name = request.POST.get("name")
        price = request.POST.get("price")
        speciality = request.POST.get("speciality")
        description = request.POST.get("description")
        
        therapist = Therapist(
            image=image,
            name=name,
            price=price,
            speciality=speciality,
            description=description
        )

        try:
            therapist.save()
            message = "Therapist added successfully"
            messages.success(request, message)
            return redirect('/admin-teams-management') 
        except Exception as e:
            message = "Couldn't add therapist. Please try again later."
            messages.error(request, message)
            print(e) 

    return render(request, 'admin/teams-management.html', {'therapist': therapist})

def editTherapist(request, therapist_id):
    details = get_object_or_404(Therapist, id=therapist_id)
    
    if request.method == 'POST':
        # Retrieve existing property instance
        therapist = Therapist.objects.get(pk=therapist_id)
        
        # Update fields with new values
        therapist.image = request.FILES.get("image")
        therapist.name = request.POST.get("name")
        therapist.price = request.POST.get("price")
        therapist.speciality = request.POST.get("speciality")
        therapist.description = request.POST.get("description")
        
        try:
            # Save the updated property
            therapist.save()
            
            message = "Therapist edited successfully"
            messages.success(request, message)
            return redirect('/admin-teams-management') 
        except Exception as e:
            message = "Couldn't edit property. Please try again later."
            messages.error(request, message)
            print(e) 
    return render(request, 'admin/edit_therapist.html', {'details': details})


def deleteTherapist(request, therapist_id):
    therapist_obj = get_object_or_404(Therapist, pk=therapist_id)
    therapist_obj.delete()
    message = "Therapist deleted successfully"
    messages.success(request, message)
    return redirect('/admin-teams-management') 