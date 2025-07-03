from django.shortcuts import render , redirect

# Create your views here.



def main_home_page_view (request):
    """
    Render the main home page of the Rising Youths Overseas Pvt. Ltd. website.
    """
    return render(request, 'index.html')




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