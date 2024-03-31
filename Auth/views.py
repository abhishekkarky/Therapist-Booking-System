from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import (authenticate, get_user_model, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model, authenticate
from Auth.models import Therapist, Booking


def home(request):
    return render(request, 'home.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        number = request.POST['number']
        password = request.POST['password']

        user = authenticate(request, username=number, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            if user.is_admin:
                return redirect('/admin-page')
            else:
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

        user = User.objects.create_user(
            username=number, email=email, password=password)
        user.name = name
        user.number = number
        user.save()

        messages.success(
            request, 'Registration successful. You can now log in.')
        return redirect('login')

    return render(request, 'register.html')


def about(request):
    therapist = Therapist.objects.all()
    return render(request, 'about.html', {'therapist': therapist})


def services(request):
    return render(request, 'services.html')


def FAQ(request):
    return render(request, 'FAQ.html')


def contect(request):
    return render(request, 'contact.html')


def individual(request, id):
    details = get_object_or_404(Therapist, id=id)
    return render(request, 'individual_therapist.html', {'details': details})


def adminPage(request):
    if (request.user.is_authenticated and request.user.is_admin):
        return render(request, 'admin/admin-panel.html')
    else:
        messages.error(
            request, "You do not have permission to access this page.")
        return redirect('dashboard')


def bookingManagement(request):
    if (request.user.is_authenticated and request.user.is_admin):
        bookings = Booking.objects.all()
        context = {
            'bookings': bookings
        }
        return render(request, 'admin/booking-management.html', context)
    else:
        messages.error(
            request, "You do not have permission to access this page.")
        return redirect('dashboard')


def teamsManagement(request):
    if (request.user.is_authenticated and request.user.is_admin):
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
            print(image, name, price, speciality, description)

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
    else:
        messages.error(
            request, "You do not have permission to access this page.")
        return redirect('dashboard')


def editTherapist(request, therapist_id):
    if (request.user.is_authenticated and request.user.is_admin):
        details = get_object_or_404(Therapist, id=therapist_id)

        if request.method == 'POST':
            # Retrieve existing therapist instance
            therapist = Therapist.objects.get(pk=therapist_id)

            # Update fields with new values
            therapist.image = request.FILES.get("image")
            therapist.name = request.POST.get("name")
            therapist.price = request.POST.get("price")
            therapist.speciality = request.POST.get("speciality")
            therapist.description = request.POST.get("description")

            try:
                # Save the updated therapist
                therapist.save()

                message = "Therapist edited successfully"
                messages.success(request, message)
                return redirect('/admin-teams-management')
            except Exception as e:
                message = "Couldn't edit therapist. Please try again later."
                messages.error(request, message)
                print(e)
        return render(request, 'admin/edit_therapist.html', {'details': details})
    else:
        messages.error(
            request, "You do not have permission to access this page.")
        return redirect('dashboard')


def deleteTherapist(request, therapist_id):
    if (request.user.is_authenticated and request.user.is_admin):
        therapist_obj = get_object_or_404(Therapist, pk=therapist_id)
        therapist_obj.delete()
        message = "Therapist deleted successfully"
        messages.success(request, message)
        return redirect('/admin-teams-management')
    else:
        messages.error(
            request, "You do not have permission to access this page.")
        return redirect('dashboard')


def bookinglist(request):
    user = request.user.id
    user_bookings = Booking.objects.filter(user=user)
    context = {
        'bookings': user_bookings
    }
    return render(request, 'bookings.html', context)


@login_required
def booking(request):
    if request.method == 'POST':
        therapist_id = request.POST.get('therapist')
        date = request.POST.get('date')
        time = request.POST.get('time')
        appointmentType = request.POST.get('appointmentType')
        note = request.POST.get('note')

        try:
            if request.user.is_authenticated:
                therapist_instance = get_object_or_404(
                    Therapist, id=therapist_id)

                booking = Booking(
                    user=request.user, therapist=therapist_instance, date=date, appointmentType=appointmentType, note=note, time=time)
                booking.save()

                message = "Booking added successfully!!"
                messages.success(request, message)
                print(messages.success(request, message))
                return redirect('/about')
            else:
                message = "User is not authenticated"
                messages.error(request, message)
                return redirect('/login')
        except Exception as e:
            message = "Couldn't process your request!! Please try again later."
            messages.error(request, message)
            print(e)
            return redirect('/booking')
    else:
        return render(request, 'booking_page.html')


@login_required
def user_edit_booking(request, id):
    booking = get_object_or_404(Booking, pk=id)
    if booking.user != request.user:
        message = "You are not authorized to edit this booking."
        messages.error(request, message)
        return redirect('/bookinglist')

    if request.method == 'POST':
        try:
            therapist_id = request.POST.get('therapist')
            date = request.POST.get('date')
            time = request.POST.get('time')
            appointmentType = request.POST.get('appointmentType')
            note = request.POST.get('note')

            booking.date = date
            booking.time = time
            booking.appointmentType = appointmentType
            booking.note = note
            booking.therapist_id = therapist_id
            booking.user_id = request.user


            booking.save()

            message = "Booking updated successfully"
            messages.success(request, message)
            return redirect('/bookinglist')
        except Exception as e:
            message = "Couldn't process your request!! Please try again later."
            messages.error(request, message)
            print(e)
            return redirect('/bookinglist')
    else:
        return render(request, 'edit_booking.html', {'booking': booking})


def user_delete_booking(request, id):
    booking_delete = get_object_or_404(Booking, pk=id)
    booking_delete.delete()
    message = "Booking deleted successfully"
    messages.success(request, message)
    return redirect('/bookinglist')


def user_logout(request):
    logout(request)
    return redirect('/login')


def profile(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            name = request.POST.get('name')
            email = request.POST.get('email')
            number = request.POST.get('number')
            user.name = name
            user.email = email
            user.number = number
            if request.FILES.get("image"):
                user.image = request.FILES.get("image")
            user.save()
            messages.success(
                request, "Your Profile has been updated successfully")
            return redirect('/profile_page')
        else:
            messages.error(request, "Something went wrong")
            return redirect('/login')
    if request.user.is_authenticated:
        user = request.user
        image = user.image
        name = user.name
        email = user.email
        number = user.number
        context = {
            'image': image,
            'name': name,
            'email': email,
            'number': number
        }
        return render(request, 'profile.html', context)
    return render(request, 'profile.html', context)


def changepassword(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if not request.user.check_password(current_password):
                return render(request, 'changepassword.html', {'error_message': 'Current password is incorrect'})

            if new_password != confirm_password:
                return render(request, 'changepassword.html', {'error_message': 'New password and confirm password do not match'})

            request.user.set_password(new_password)
            request.user.save()

            update_session_auth_hash(request, request.user)

            return redirect('/profile_page')

    return render(request, 'changepassword.html')
