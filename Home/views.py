from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from Home.models import ContactList


# Create your views here.
# @login_required
def home(request):
    return render(request, 'home.html')

# @login_required
def contact(request):
    if request.method == 'POST':
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        query = ContactList(firstName = firstName, lastName = lastName, email = email, phone = phone, message = message)
        try:
            query.save()
            message = "Received your message!! We will contact you shortly."
            messages.success(request, message)
            return redirect('/contact')
        except Exception as e:
            message = "Couldn't process your request!! Please try again later."
            messages.error(request, message)
            print(e)
    return render(request, 'contact.html')

def contactList(request):
    details = ContactList.objects.all()
    return render(request, 'admin/contact-list.html', {'details': details})

