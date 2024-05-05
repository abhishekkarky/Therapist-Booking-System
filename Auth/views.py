from .models import Booking, Testimonials
from django.shortcuts import render, redirect
from datetime import datetime
import time
import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (authenticate, get_user_model, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from Auth.models import Booking, Payment, Therapist, CustomUser
from Home.models import ContactList

from datetime import datetime, timedelta


def home(request):
    if request.user.is_authenticated:
        testimonials = Testimonials.objects.all()
        if request.user.is_admin:
            messages.error(request, 'You donot have access to this page.')
            return redirect('/admin-page', {"testimonials": testimonials})

    return render(request, 'home.html')


def user_login(request):
    if request.user.is_authenticated:
        messages.error(request, 'You are already logged In.')
        if request.user.is_admin:
            return redirect('/admin-page')
        else:
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
    if request.user.is_authenticated:
        messages.error(request, 'You are already logged In.')
        if request.user.is_admin:
            return redirect('/admin-page')
        else:
            return redirect('/')

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        number = request.POST['number']
        password = request.POST['password']

        User = get_user_model()
        if(User.objects.filter(username=number).exists()):
            messages.error(request, 'User already exists.')
            return redirect('register')

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
    if request.user.is_authenticated:
        if request.user.is_admin:
            messages.error(request, 'You donot have access to this page.')
            return redirect('/admin-page')

    therapist = Therapist.objects.all()
    return render(request, 'about.html', {'therapist': therapist})


def services(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            messages.error(request, 'You donot have access to this page.')
            return redirect('/admin-page')

    return render(request, 'services.html')


def FAQ(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            messages.error(request, 'You donot have access to this page.')
            return redirect('/admin-page')

    return render(request, 'FAQ.html')

# @login_required


def contact(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            messages.error(request, 'You donot have access to this page.')
            return redirect('/admin-page')

    if request.method == 'POST':
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        query = ContactList(firstName=firstName, lastName=lastName,
                            email=email, phone=phone, message=message)
        try:
            query.save()
            message = "Received your message!! We will contact you shortly."
            messages.success(request, message)
            return redirect('/contact')
        except Exception as e:
            message = "Couldn't process your request!! Please try again later."
            messages.error(request, message)
    return render(request, 'contact.html')


def contactList(request):
    details = ContactList.objects.all()
    return render(request, 'admin/contact-list.html', {'details': details})


def individual(request, id):
    if request.user.is_authenticated:
        if request.user.is_admin:
            messages.error(request, 'You donot have access to this page.')
            return redirect('/admin-page')

    details = get_object_or_404(Therapist, id=id)
    return render(request, 'individual_therapist.html', {'details': details})


def adminPage(request):
    if (request.user.is_authenticated and request.user.is_admin):

        therapist = Therapist.objects.all().count()
        userCount = CustomUser.objects.all().count()
        bookingCount = Booking.objects.all().count()
        contactCount = ContactList.objects.all().count()
        seven_days_ago = datetime.now() - timedelta(days=7)
        user_count_last_7_days = CustomUser.objects.filter(
            created_at=seven_days_ago).count()
        booking_count_last_7_days = Booking.objects.filter(created_at__gte=seven_days_ago).count()

        context = {
            'therapist': therapist,
            'userCount': userCount,
            'bookingCount': bookingCount,
            'contactCount': contactCount,
            'user_count_last_7_days': user_count_last_7_days,
            'booking_count_last_7_days':booking_count_last_7_days
        }
        return render(request, 'admin/admin-panel.html', context)
    else:
        messages.error(
            request, "You do not have permission to access this page.")
        return redirect('dashboard')


def bookingManagement(request):
    if request.user.is_authenticated and request.user.is_admin:
        bookings = Booking.objects.all()
        today = datetime.now().date()
        past_appointments = []
        today_appointments = []
        upcoming_appointments = []

        for booking in bookings:
            if booking.date < today:
                past_appointments.append(booking)
            elif booking.date == today:
                today_appointments.append(booking)
            else:
                upcoming_appointments.append(booking)

        sorted_bookings = upcoming_appointments + today_appointments + past_appointments

        context = {
            'bookings': sorted_bookings,
            'today': today,
        }

        return render(request, 'admin/booking-management.html', context)
    else:
        messages.error(request, "You do not have permission to access this page.")
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


stripe.api_key = 'sk_test_51P1lOZ06ho0W5mPfHhr4drqVtm8P1AwXs4vaJc5fuG5lJdCiZSPWusgTNVFBIVqpTOHXCX2zUAJe3rF4RBlcIPUY00kiP8S4oq'


@login_required
def booking(request):

    if request.method == 'POST':
        therapist_id = request.POST.get('therapist')
        date = request.POST.get('date')
        time = request.POST.get('time')
        appointmentType = request.POST.get('appointmentType')
        note = request.POST.get('note')

        # Check if there is already a booking for the same date, time, and therapist
        existing_booking = Booking.objects.filter(
            therapist_id=therapist_id,
            date=date,
            time=time
        ).exists()

        if existing_booking:
            messages.error(
                request, "This slot is already booked. Please choose another date or time.")
            return redirect('/individual_therapist/' + str(therapist_id))

        request.session['therapist'] = therapist_id
        request.session['date'] = date
        request.session['time'] = time
        request.session['appointmentType'] = appointmentType
        request.session['note'] = note

        try:
            therapist_instance = get_object_or_404(Therapist, id=therapist_id)
            price = stripe.Price.create(
                unit_amount=therapist_instance.price,
                currency='usd',
                product='prod_PrXMqQakxRxCcx',
                recurring=None,
            )

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': price.id,
                        'quantity': 1
                    }
                ],
                mode='payment',
                customer_creation='always',
                success_url='http://127.0.0.1:7000/payment_successful?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://127.0.0.1:7000/payment_cancelled?session_id={CHECKOUT_SESSION_ID}',
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            messages.error(
                request, "Couldn't process your request!! Please try again later.")
            print(e)
            return redirect('/booking')
    return render(request, 'booking_page.html')


def payment_successful(request):
    checkout_session_id = request.GET.get('session_id', None)
    therapist_id = request.session.get('therapist')
    date = request.session.get('date')
    time = request.session.get('time')
    appointmentType = request.session.get('appointmentType')
    note = request.session.get('note')

    try:
        session = stripe.checkout.Session.retrieve(checkout_session_id)
        customer = stripe.Customer.retrieve(session.customer)
        with transaction.atomic():
            user_payment = Payment.objects.create(
                user=request.user,
                payment_bool=True,
                stripe_checkout_id=checkout_session_id
            )
            user_payment.save()

            therapist_instance = get_object_or_404(Therapist, id=therapist_id)
            booking = Booking.objects.create(
                user=request.user,
                therapist=therapist_instance,
                date=date,
                appointmentType=appointmentType,
                note=note,
                time=time,
                isPaid=True
            )
            booking.save()
    except Exception as e:
        print(e)
        messages.error(
            request, "Payment unsuccessful. Please try again later.")
        return redirect('/bookinglist')

    messages.success(request, "Payment successful. Your booking is confirmed.")
    return redirect('/bookinglist')


def payment_cancelled(request):
    return render(request, 'individual_therapist.html')


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRECT_TEST
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
        user_payment = Payment.objects.get(stripe_checkout_id=session_id)
        line_items = stripe.checkout.Session.list_line_items(
            session_id, limit=1)
        user_payment.payment_bool = True
        user_payment.save()
        return HttpResponse(status=200)


@login_required
def user_edit_booking(request, id):
    booking = get_object_or_404(Booking, pk=id)
    today = datetime.now().date()
    context = {
        'today': today
    }
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
        return render(request, 'edit_booking.html', {'booking': booking, 'today': today})


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


def admin_testimonial(request):
    if (request.user.is_authenticated and request.user.is_admin):
        testimonials = Testimonials.objects.all()
        context = {
            'testimonials': testimonials,
        }
        if request.method == 'POST':
            image = request.FILES.get("image")
            name = request.POST.get("name")
            description = request.POST.get("description")
            intro = request.POST.get("intro")
            print(image, name, description, intro)

            test_obj = Testimonials(
                image=image,
                name=name,
                description=description,
                intro=intro
            )
            print(test_obj)

            try:
                test_obj.save()
                message = "Testimonial added successfully"
                messages.success(request, message)
                return redirect('/admin-testimonial')
            except Exception as e:
                message = "Couldn't add Testimonial. Please try again later."
                messages.error(request, message)
                print(e)

        return render(request, 'admin/admin-testimonial.html', context)
    else:
        messages.error(
            request, "You do not have permission to access this page.")
        return redirect('dashboard')


def admin_delete_test(request, id):
    if (request.user.is_authenticated and request.user.is_admin):
        delete_test = get_object_or_404(Testimonials, pk=id)
        delete_test.delete()
        message = "Testimonial deleted successfully"
        messages.success(request, message)
        return redirect('/admin-testimonial')
    else:
        messages.error(
            request, "You do not have permission to access this page.")
        return redirect('dashboard')


def edit_testimonial(request, id):
    if (request.user.is_authenticated and request.user.is_admin):
        details = get_object_or_404(Testimonials, id=id)

        if request.method == 'POST':
            image = request.FILES.get("image")
            name = request.POST.get("name")
            intro = request.POST.get("intro")
            description = request.POST.get("description")

            try:
                if image is None:
                    image = details.image

                editQuery = Testimonials(
                    id=id, image=image, name=name, intro=intro, description=description)
                editQuery.save()
                message = "Testimonial edited successfully"
                messages.success(request, message)
                return redirect('/admin-testimonial')
            except Exception as e:
                message = "Couldn't edit property. Please try again later."
                messages.error(request, message)
                print(e)

        return render(request, 'admin/testimonial-edit.html', {'testi': details})
    else:
        messages.error(
            request, "You do not have permission to access this page.")
        return redirect('dashboard')


# def payment_successful(request):
#     checkout_session_id = request.GET.get('session_id', None)
#     therapist_id = request.session.get('therapist')
#     date = request.session.get('date')
#     time = request.session.get('time')
#     appointmentType = request.session.get('appointmentType')
#     note = request.session.get('note')

#     try:
#         # Retrieve Stripe session and customer
#         session = stripe.checkout.Session.retrieve(checkout_session_id)
#         customer = stripe.Customer.retrieve(session.customer)

#         # Save payment
#         with transaction.atomic():
#             user_instance = get_object_or_404(CustomUser, id=request.user.id)
#             user_payment = Payment.objects.create(
#                 user=user_instance,
#                 payment_bool=True,
#                 stripe_checkout_id=checkout_session_id
#             )
#             user_payment.save()

#             # Save booking
#             therapist_instance = get_object_or_404(Therapist, id=therapist_id)
#             booking = Booking.objects.create(
#                 user=request.user,
#                 therapist=therapist_instance,
#                 date=date,
#                 appointmentType=appointmentType,
#                 note=note,
#                 time=time,
#                 isPaid=True
#             )
#             booking.save()
#     except Exception as e:
#         # Log the error
#         print(e)
#         # Provide feedback to the user
#         messages.error(request, "Payment unsuccessful. Please try again later.")
#         return redirect('/bookinglist')

#     # Provide feedback to the user
#     messages.success(request, "Payment successful. Your booking is confirmed.")
#     return redirect('/bookinglist')
