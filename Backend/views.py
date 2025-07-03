from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage

def contact_us_view(request):
    if request.method == 'POST':
        try:
            ContactMessage.objects.create(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                subject=request.POST.get('subject'),
                message=request.POST.get('message')
            )
            messages.success(request, "Your message has been sent successfully! We'll contact you soon.")
        except Exception as e:
            messages.error(request, "Something went wrong. Please try again.")
        return redirect('contact_us_view')  # Replace with your URL name
    return render(request, 'Modelpages/contact_us.html')
