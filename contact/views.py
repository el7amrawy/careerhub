from django.shortcuts import render
from .models import Info
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def send_message(request):
    # Create or update Info object with new email
    info, created = Info.objects.get_or_create(
        defaults={
            'place': 'Your Location',
            'phone_number': 'Your Phone',
            'email': 'careerhub920@gmail.com'
        }
    )
    if not created:
        info.email = 'careerhub920@gmail.com'
        info.save()

    if request.method == 'POST':
        subject = request.POST['subject']
        email = request.POST['email']
        message = request.POST['message']
        message_body = f"From: {email}\n\n{message}"
        send_mail(
            subject,
            message_body,
            email,
            [settings.EMAIL_HOST_USER],
        )

    return render(request,'contact/contact.html',{'myinfo':info})