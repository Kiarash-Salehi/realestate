from django.shortcuts import render, redirect
from .models import Contacts
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contact = Contacts.objects.all().filter(user_id=user_id, listing_id=listing_id)
            if has_contact:
                messages.error(request, 'You have already submitted an inquiry for this listing.')
                return redirect('/listings/'+listing_id)

        contact = Contacts(listing_id=listing_id, listing=listing, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()

        try:
            send_mail(
                'Property Listing Inquiry',
                'There has been an inquiry sent for ' + listing + '. Sign in to admin pannel for more details.',
                'skiarash57@gmail.com',
                [realtor_email],
                fail_silently=False
            )
        except Exception as error:
            messages.error(request, error)
            return redirect('/listings/'+listing_id)

        messages.success(request, 'Your request has been submitted! a reltor will get back to you soon.')
        return redirect('/listings/'+listing_id)
