from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views 

urlpatterns = [
    

    path('', views.main_home_page_view, name='main_home_page_view'),
    path('chairman/', views.chairman_message_view, name='chairman_message_view'),
    path('ceo/', views.messag_from_ceo_view, name='messag_from_ceo_view'),
    path('about-us/', views.about_us_view, name='about_us_view'),
    path('our-team/', views.our_team_view, name='our_team_view'),
    path('license-and-certificates/', views.license_and_certificates_view, name='license_and_certificates_view'),
    path('organizational-chart/', views.organizational_chart_view, name='organizational_chart_view'),
    path('procedures/', views.procedures_view, name='procedures_view'),    
    path('gallery/', views.gallery_view, name='gallery_view'),
    path('consulting/', views.consulting_view, name='consulting_view'),
    path('training/', views.traning_and_orientation_view, name='traning_and_orientation_view'),
    path('travel/', views.travel_management_view, name='travel_management_view'),
    path('human-resources/', views.human_resources_view, name='human_resources_view'),
    path('job/<int:job_id>/', views.job_detail_view, name='job_detail'),





    
]

# Serve static and media files during development (when DEBUG is True)
if settings.DEBUG:
    # Serve media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)