from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage  # ADD THIS

def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')

        # 1. Save to database (always works)
        contact = ContactMessage.objects.create(
            name=name,
            email=email,
            message=message_text
        )

        # 2. Try to send email
        try:
            send_mail(
                subject=f"Portfolio: New message from {name}",
                message=f"""
                Name: {name}
                Email: {email}
                Time: {contact.created_at.strftime('%Y-%m-%d %H:%M')}

                Message:
                {message_text}
                """,
                from_email=email,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            messages.success(request, "Message sent! I'll reply within 24 hours")
        except:
            messages.warning(request, "Message saved, but email failed. I'll still see it!")

        return redirect('/#contact')

    return render(request, 'index.html')