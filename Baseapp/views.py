from django.shortcuts import render , redirect , get_object_or_404
from Admin.models import BlogPost , ManpowerGallery , YouthJob


# Create your views here.



def main_home_page_view(request):
    """
    Render the main home page of the Rising Youths Overseas Pvt. Ltd. website.
    """
    blogs = BlogPost.objects.all().order_by('-created_at')[:6]
    jobs = YouthJob.objects.all().order_by('-posted_at')[:6]  
    return render(request, 'index.html', {'blogs': blogs, 'jobs': jobs})  




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




def procedures_view(request):
    """
    Render the procedures page.
    """
    return render(request, 'Components/procedures.html')



def gallery_view(request):
    """
    Render the gallery page.
    """
    gallery_images = ManpowerGallery.objects.all().order_by('-created_at')
    return render(request, 'Components/gallery.html' , {'gallery_images': gallery_images})



def consulting_view(request):
    """
    Render the consulting page.
    """
    return render(request, 'Components/consulting.html')


def traning_and_orientation_view(request):
    """
    Render the training and orientation page.
    """
    return render(request, 'Components/training_and_orientation.html')




def travel_management_view(request):
    """
    Render the travel management page.
    """
    return render(request, 'Components/travel_management.html')



def human_resources_view(request):
    """
    Render the human resources page.
    """
    return render(request, 'Components/human_resources.html')





def job_detail_view(request, job_id):
    """
    Display detailed view of a specific job posting.
    """
    # Get the specific job or return 404 if not found
    job = get_object_or_404(YouthJob, id=job_id)
    
    # Get related jobs (same category, excluding current job)
    related_jobs = YouthJob.objects.filter(
        category=job.category
    ).exclude(id=job.id).order_by('-posted_at')[:3]
    
    # If no jobs in same category, get latest jobs from other categories
    if not related_jobs:
        related_jobs = YouthJob.objects.exclude(id=job.id).order_by('-posted_at')[:3]
    
    context = {
        'job': job,
        'related_jobs': related_jobs,
    }
    
    return render(request, 'Components/job_detail.html', context)