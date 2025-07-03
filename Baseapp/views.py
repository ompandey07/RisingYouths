from django.shortcuts import render , redirect
from Admin.models import BlogPost

# Create your views here.



def main_home_page_view (request):
    """
    Render the main home page of the Rising Youths Overseas Pvt. Ltd. website.
    """
    blogs = BlogPost.objects.all().order_by('-created_at')[:6]  # Fetch the latest 3 blog posts
    return render(request, 'index.html' , {'blogs': blogs})




def chairman_message_view(request):
    """
    Render the chairman's message page.
    """
    return render(request, 'Components/chairman_message.html')



def about_us_view(request):
    """
    Render the about us page.
    """
    return render(request, 'Components/about_us.html')



def our_team_view(request):
    """
    Render the our team page.
    """
    return render(request, 'Components/our_team.html')



def license_and_certificates_view(request):
    """
    Render the license and certificates page.
    """
    return render(request, 'Components/license_and_certificates.html')



def organizational_chart_view(request):
    """
    Render the organizational chart page.
    """
    return render(request, 'Components/organizational_chart.html')